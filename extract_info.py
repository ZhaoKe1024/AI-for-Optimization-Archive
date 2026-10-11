# -*- coding: utf-8 -*-
"""
extract_info.py
===============
为 ./src/ 下每一篇论文的顶层 json 元数据文件（title/authors/abstract）补充
基于论文 LaTeX 源码的五个中文分析字段：

    研究对象 / 解决的问题目标 / 本文提出的核心思想和方法 / 本问的研究意义 / 本问的优点和局限性

用法：
    python extract_info.py                 # 处理全部（自动跳过已完成的论文）
    python extract_info.py --limit 5       # 只处理前 5 篇（调试）
    python extract_info.py --only ORLM     # 只处理路径包含 ORLM 的论文
    python extract_info.py --force         # 覆盖已有字段
    python extract_info.py --workers 8     # 并发调用数
    python extract_info.py --dry-run       # 只打印将处理哪些论文，不调用 LLM
"""

import argparse
import json
import os
import re
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI

# ---------------------------------------------------------------------------
# 路径与配置
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
CFG_PATH = BASE_DIR / "private" / "llm_config.json"
LOG_PATH = BASE_DIR / "private" / "cc_history" / "extract_info.log"
BACKUP_DIR = BASE_DIR / "private" / "cc_history" / "src_json_backup"

FIELDS = [
    "研究对象",
    "解决的问题目标",
    "本文提出的核心思想和方法",
    "本问的研究意义",
    "本问的优点和局限性",
]

SYSTEM_PROMPT = (
    "你是一位运筹优化（Operations Research）与大语言模型交叉领域的资深研究者与审稿人，"
    "擅长从学术论文中提炼研究问题、方法、意义与优缺点。"
    "你的输出必须是严格合法的 JSON，不得包含任何解释、前言、markdown 代码块标记或多余文字。"
)

EXTRACT_PROMPT_TEMPLATE = """请精读下面提供的论文信息（标题、作者、摘要）与论文正文源码（LaTeX，可能被截断），\
并站在"基于大语言模型的优化问题自动建模与求解"这一调研主题的视角，\
提炼出这篇论文的五个维度的分析信息。

要求：
1. 五个字段全部必须给出，内容用简体中文撰写；
2. 每个字段 80～300 字，观点必须严格基于论文原文，不要编造论文中没有的内容；
3. "优点和局限性"要具体：优点写方法新颖性、效果、规模、开源等；局限性写数据集规模、问题类型覆盖、理论保障、可扩展性、真实场景差距等论文中暴露或可推知的短板；
4. 只输出一个 JSON 对象，键名与下面完全一致，值必须是字符串；
5. 不要输出 markdown 代码块围栏（```）、不要输出任何 JSON 之外的文字。

JSON 格式：
{{
  "研究对象": "",
  "解决的问题目标": "",
  "本文提出的核心思想和方法": "",
  "本问的研究意义": "",
  "本问的优点和局限性": ""
}}

=== 论文信息 ===
标题：{title}
作者：{authors}
摘要：{abstract}

=== 论文正文（LaTeX 截断片段） ===
{body}
"""


# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------
def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# LLM 调用
# ---------------------------------------------------------------------------
class LLMClient:
    def __init__(self, model_name: str = "deepseek", user_name: str = "zk"):
        self.model_name = model_name
        self.user_name = user_name
        api_config = json.load(open(CFG_PATH, encoding="utf-8"))
        if model_name not in api_config:
            raise KeyError(f"llm_config.json 中不存在模型 '{model_name}'，可用：{list(api_config)}")
        self.cfg = api_config[model_name]
        self.client = OpenAI(api_key=self.cfg["api_key"], base_url=self.cfg["base_url"])

    def chat(self, prompt: str, max_tokens: int = 3000, temperature: float = 0.2) -> str:
        print(f"calling {self.model_name} of {self.user_name}", flush=True)
        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model=self.cfg["model"],
            stream=False,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content


def parse_json_response(text: str) -> dict:
    """从 LLM 回复中鲁棒地解析 JSON 对象。"""
    if not text:
        raise ValueError("LLM 返回空内容")
    t = text.strip()
    # 去掉 ```json ... ``` 围栏
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", t, flags=re.S)
    if fence:
        t = fence.group(1).strip()
    # 取第一个 { 到最后一个 }
    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"未找到 JSON 对象：{text[:300]!r}")
    return json.loads(t[start : end + 1])


# ---------------------------------------------------------------------------
# LaTeX 收集与压缩
# ---------------------------------------------------------------------------
def strip_latex_comments(text: str) -> str:
    # 去掉行注释（不在命令参数内，保守处理：只处理行首/空白后的 %）
    out = []
    for line in text.splitlines():
        # 找第一个未转义的 %
        idx = -1
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                idx = i
                break
            i += 1
        if idx >= 0:
            line = line[:idx]
        out.append(line.rstrip())
    return "\n".join(out)


_PRIORITY_PATTERNS = [
    (10, re.compile(r"(abstract|0[-_]?abs|abs)", re.I)),
    (9, re.compile(r"(intro)", re.I)),
    (8, re.compile(r"(method|approach|model|framework|algorithm|preliminar|motivation)", re.I)),
    (7, re.compile(r"(experiment|evaluation|result|benchmark)", re.I)),
    (6, re.compile(r"(conclusion|discussion|related|background)", re.I)),
]


def tex_priority(name: str) -> int:
    for score, pat in _PRIORITY_PATTERNS:
        if pat.search(name):
            return score
    return 3


def collect_paper_body(paper_dir: Path, total_budget: int = 52000) -> str:
    """按优先级拼接论文 tex 源码，返回压缩后的正文文本。"""
    tex_files = sorted(paper_dir.rglob("*.tex"))
    if not tex_files:
        return "(未找到 LaTeX 源文件)"

    # 排除明显的纯表格/数据文件与 .sty/.cls 生成的残留
    tex_files = [
        p
        for p in tex_files
        if not re.search(r"(\.sty|\.cls|solver-result|prompt|dataset|license|_table|\\Tables)", str(p).replace("\\", "/"), re.I)
    ]
    tex_files.sort(key=lambda p: (-tex_priority(p.name), len(p.name), str(p)))

    chunks = []
    used = 0
    for p in tex_files:
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        text = strip_latex_comments(raw)
        text = re.sub(r"\n{3,}", "\n\n", text)
        room = total_budget - used
        if room <= 500:
            break
        if len(text) > room:
            # 保留开头（摘要/引言通常在前）
            text = text[:room] + "\n...[正文截断]..."
        chunks.append(f"--- 文件 {p.name} ---\n{text}")
        used += len(text)
    return "\n\n".join(chunks)


# ---------------------------------------------------------------------------
# 单篇论文处理
# ---------------------------------------------------------------------------
def process_one(json_path: Path, llm: LLMClient, force: bool, dry_run: bool) -> str:
    stem = json_path.name[:-5]  # 去掉 .json
    folder = SRC_DIR / stem
    try:
        data = json.load(open(json_path, encoding="utf-8"))
    except Exception as e:
        return f"SKIP_BADJSON {json_path.name}: {e}"

    if not isinstance(data, dict):
        return f"SKIP_NOTDICT {json_path.name}"

    if not force and all(str(data.get(k, "")).strip() for k in FIELDS):
        return f"SKIP_DONE {json_path.name}"

    if dry_run:
        return f"TODO {json_path.name}"

    title = str(data.get("title", "")).strip()
    authors = str(data.get("authors", "")).strip()
    abstract = str(data.get("abstract", "")).strip()
    body = collect_paper_body(folder) if folder.is_dir() else "(未找到论文源码目录)"

    prompt = EXTRACT_PROMPT_TEMPLATE.format(title=title, authors=authors, abstract=abstract, body=body)

    last_err = None
    for attempt in range(1, 4):
        try:
            reply = llm.chat(prompt)
            info = parse_json_response(reply)
            missing = [k for k in FIELDS if not str(info.get(k, "")).strip()]
            if missing:
                raise ValueError(f"字段缺失或为空：{missing}")
            # 只写入目标字段，保留原有 title/authors/abstract 等
            for k in FIELDS:
                data[k] = str(info[k]).strip()
            # 备份原文件（每篇只备份一次）
            try:
                BACKUP_DIR.mkdir(parents=True, exist_ok=True)
                backup = BACKUP_DIR / json_path.name
                if not backup.exists():
                    json.dump(json.load(open(json_path, encoding="utf-8")), open(backup, "w", encoding="utf-8"),
                              ensure_ascii=False, indent=2)
            except Exception as e:
                log(f"  backup failed {json_path.name}: {e}")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            return f"OK {json_path.name}"
        except Exception as e:
            last_err = e
            log(f"  attempt {attempt} failed for {json_path.name}: {str(e)[:200]}")
            time.sleep(2.0 * attempt)
    return f"FAIL {json_path.name}: {str(last_err)[:300]}"


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="为 ./src 论文 json 补充五个分析字段")
    parser.add_argument("--limit", type=int, default=0, help="最多处理 N 篇（0=全部）")
    parser.add_argument("--only", type=str, default="", help="只处理文件名包含该子串的论文")
    parser.add_argument("--force", action="store_true", help="覆盖已有字段")
    parser.add_argument("--workers", type=int, default=4, help="并发线程数")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不调用 LLM")
    parser.add_argument("--model", default="deepseek")
    parser.add_argument("--user", default="zk")
    args = parser.parse_args()

    json_paths = sorted(SRC_DIR.glob("*.json"))
    if not json_paths:
        print("src/ 下未找到顶层 json 文件", file=sys.stderr)
        sys.exit(1)
    if args.only:
        json_paths = [p for p in json_paths if args.only.lower() in p.name.lower()]
    if args.limit > 0:
        json_paths = json_paths[: args.limit]

    log(f"共发现 {len(json_paths)} 篇论文待处理（workers={args.workers}, force={args.force}, dry_run={args.dry_run}）")

    llm = None if args.dry_run else LLMClient(args.model, args.user)

    results = []
    if args.workers <= 1 or args.dry_run:
        for p in json_paths:
            r = process_one(p, llm, args.force, args.dry_run)
            results.append(r)
            log(r)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(process_one, p, llm, args.force, args.dry_run): p.name for p in json_paths}
            for fut in as_completed(futs):
                r = fut.result()
                results.append(r)
                log(r)

    ok = sum(1 for r in results if r.startswith("OK"))
    todo = sum(1 for r in results if r.startswith("TODO"))
    skip = sum(1 for r in results if r.startswith("SKIP"))
    fail = sum(1 for r in results if r.startswith("FAIL"))
    log(f"完成：OK={ok}, SKIP={skip}, TODO={todo}, FAIL={fail}")
    if fail:
        log("失败论文见上方 FAIL 行；可重新运行脚本自动重试（已成功的会自动跳过）。")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
