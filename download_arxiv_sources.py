# -*- coding: utf-8 -*-
"""
Download arXiv source packages for every paper listed in arxiv_papers.csv.

For each arXiv paper:
  1. GET  https://arxiv.org/abs/<arxiv_id>          -> extract full title /
       authors / abstract, save <name>.json next to the archive.
  2. GET  https://arxiv.org/src/<arxiv_id>          -> save the downloaded
       source archive as {sanitized_title[:16]}_{arxiv_id}.zip
       (sanitize keeps only [a-zA-Z0-9_-] and spaces; everything else is
       removed).

Rate limit: at least SLEEP_SECONDS (6 s) between two consecutive HTTP requests,
in order to avoid tripping arXiv anti-bot protection.  Files that already exist
are skipped, so the script can be re-run to resume an interrupted download.

The final arxiv_papers.csv is refreshed with the official title / authors /
abstract returned by arXiv, plus the per-paper download status.
"""
import csv
import html
import json
import re
import sys
import time
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "arxiv_papers.csv"
SRC_DIR = BASE / "src"
SLEEP_SECONDS = 6
ABS_URL = "https://arxiv.org/abs/{}"
SRC_URL = "https://arxiv.org/src/{}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
        "(research-script; batch-download; 6s-per-request)"
    )
}


def sanitize_title(title: str) -> str:
    """Keep only ASCII letters, digits, '_', '-' and spaces; drop everything else."""
    out = "".join(
        ch
        for ch in (title or "")
        if ch.isascii() and (ch.isalnum() or ch in "_- ")
    )
    return out[:16] if out.strip() else "paper"


def file_paths(title: str, arxiv_id: str):
    stem = f"{sanitize_title(title)}_{arxiv_id}"
    return SRC_DIR / f"{stem}.zip", SRC_DIR / f"{stem}.json"


def strip_tags(raw: str) -> str:
    return html.unescape(re.sub(r"<[^>]*>", " ", raw))


def extract_info_from_html(page_text: str):
    """
    Extract title, author list and abstract from one arXiv abs-page HTML.
    (stdlib implementation of the BeautifulSoup version supplied in the task.)
    """
    # Title: <h1 class="title mathjax">...</h1>
    title = None
    m = re.search(
        r'<h1[^>]*class=["\'][^"\']*title[^"\']*["\'][^>]*>(.*?)</h1>',
        page_text,
        re.S | re.I,
    )
    if m:
        title = strip_tags(m.group(1)).strip()
        title = re.sub(r"^\s*Title\s*:\s*", "", title, flags=re.I).strip() or None

    # Authors: <div class="authors"> ... <a>Name</a> ... </div>
    authors = []
    m = re.search(r'<div[^>]*class=["\'][^"\']*authors[^"\']*["\'][^>]*>(.*?)</div>', page_text, re.S | re.I)
    if m:
        block = m.group(1)
        for a in re.finditer(r"<a\b[^>]*>(.*?)</a>", block, re.S | re.I):
            name = strip_tags(a.group(1)).strip()
            if name:
                authors.append(name)

    # Abstract: <blockquote class="abstract mathjax">...</blockquote>
    abstract = None
    m = re.search(
        r'<blockquote[^>]*class=["\'][^"\']*abstract[^"\']*["\'][^>]*>(.*?)</blockquote>',
        page_text,
        re.S | re.I,
    )
    if m:
        abstract = strip_tags(m.group(1)).strip()
        abstract = re.sub(r"^\s*Abstract\s*:\s*", "", abstract, flags=re.I).strip() or None

    return title, ", ".join(authors), abstract


def do_request(url: str, timeout: int):
    """One HTTP request, followed by the mandatory inter-request sleep."""
    try:
        print(f"  -> GET {url}", flush=True)
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        print(f"     HTTP {resp.status_code} {resp.headers.get('Content-Type', '')}",
              flush=True)
        return resp
    finally:
        # every request (success or failure) is followed by a 6 s pause
        print(f"     sleeping {SLEEP_SECONDS}s ...", flush=True)
        time.sleep(SLEEP_SECONDS)


FIELD_NAMES = [
    "arxiv_id",
    "arxiv_url",
    "title",
    "title_readme",
    "authors",
    "abstract",
    "section",
    "source_line",
    "status",
    "zip_file",
    "json_file",
]


def load_rows():
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row.setdefault("title_readme", row.get("title", ""))
    return rows


def save_rows(rows):
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    total = len(rows)
    print(f"papers to process: {total}", flush=True)

    ok = 0
    metadata_only = 0
    skipped = 0
    failed = []

    for i, row in enumerate(rows, 1):
        arxiv_id = (row.get("arxiv_id") or "").strip()
        readme_title = (row.get("title_readme") or row.get("title") or "").strip()
        if not arxiv_id:
            failed.append({"arxiv_id": "", "error": "missing arxiv_id"})
            continue

        print(f"\n[{i}/{total}] {arxiv_id}  README-title: {readme_title[:80]}", flush=True)

        # ------------------------------------------------------------------
        # Skip papers that already have a zip+json pair from a previous run
        # (recognized regardless of the filename convention used before).
        # ------------------------------------------------------------------
        existing_zips = sorted(SRC_DIR.glob(f"*_{arxiv_id}.zip"))
        existing_jsons = sorted(SRC_DIR.glob(f"*_{arxiv_id}.json"))
        already_done = (
            any(z.exists() and z.stat().st_size > 0 for z in existing_zips)
            and any(j.exists() for j in existing_jsons)
        )
        if already_done:
            print("     existing zip+json pair found -> skip (previous run)", flush=True)
            skipped += 1
            ok += 1
            row["status"] = "skipped(existing)"
            row["zip_file"] = existing_zips[0].name
            row["json_file"] = existing_jsons[0].name
            save_rows(rows)
            continue

        # ------------------------------------------------------------------
        # Step 1: fetch metadata from the abs page
        # ------------------------------------------------------------------
        meta = None
        metadata_error = None
        zip_path, json_path = file_paths(readme_title, arxiv_id)

        try:
            resp = do_request(ABS_URL.format(arxiv_id), timeout=30)
            resp.raise_for_status()
            title, authors, abstract = extract_info_from_html(resp.text)
            if not title:
                raise ValueError("could not parse title from abs page")
            meta = {"title": title, "authors": authors, "abstract": abstract}
            print(f"     title: {title}", flush=True)
            print(f"     authors: {authors[:120]}", flush=True)
        except Exception as e:  # noqa: BLE001 - keep going on any error
            metadata_error = f"{type(e).__name__}: {e}"
            print(f"     metadata FAILED: {metadata_error}", flush=True)

        # ------------------------------------------------------------------
        # Save the metadata JSON next to the archive (when available)
        # ------------------------------------------------------------------
        if meta is not None:
            name_title = meta["title"] or readme_title
            zip_path, json_path = file_paths(name_title, arxiv_id)
            with json_path.open("w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            print(f"     JSON saved: {json_path.name}", flush=True)
            row["title"] = meta["title"]
            row["authors"] = meta["authors"]
            row["abstract"] = meta["abstract"]
        else:
            row["title"] = readme_title
            row["authors"] = ""
            row["abstract"] = ""

        # ------------------------------------------------------------------
        # Step 2: download the source archive
        # ------------------------------------------------------------------
        zip_error = None
        if zip_path.exists() and zip_path.stat().st_size > 0:
            print(f"     zip already exists: {zip_path.name} -> keep", flush=True)
        else:
            try:
                resp = do_request(SRC_URL.format(arxiv_id), timeout=90)
                resp.raise_for_status()
                ctype = resp.headers.get("Content-Type", "")
                if ctype.startswith("text/html"):
                    raise ValueError(
                        f"src endpoint returned an HTML page ({ctype}); "
                        f"source may not be available for {arxiv_id}"
                    )
                data = resp.content
                if not data:
                    raise ValueError("src endpoint returned an empty body")
                zip_path.write_bytes(data)
                print(f"     zip saved: {zip_path.name} ({len(data)} bytes, {ctype})", flush=True)
            except Exception as e:  # noqa: BLE001
                zip_error = f"{type(e).__name__}: {e}"
                print(f"     src download FAILED: {zip_error}", flush=True)

        # ------------------------------------------------------------------
        # Bookkeeping
        # ------------------------------------------------------------------
        if zip_error is None:
            ok += 1
            row["status"] = "ok" if meta is not None else "src_ok(metadata_missing)"
            row["zip_file"] = zip_path.name if zip_path.exists() else ""
            row["json_file"] = json_path.name if json_path.exists() else ""
        elif meta is not None:
            metadata_only += 1
            row["status"] = f"metadata_only; src failed: {zip_error}"
            row["zip_file"] = ""
            row["json_file"] = json_path.name
            failed.append({"arxiv_id": arxiv_id, "error": zip_error})
        else:
            row["status"] = (
                f"failed; metadata: {metadata_error}; src: {zip_error}"
            )
            row["zip_file"] = ""
            row["json_file"] = ""
            failed.append(
                {
                    "arxiv_id": arxiv_id,
                    "error": (zip_error or metadata_error or "unknown"),
                }
            )

        save_rows(rows)

    print("\n" + "=" * 70, flush=True)
    print(f"DONE  ok={ok}  metadata_only={metadata_only}  skipped={skipped}  "
          f"failed={len(failed)}", flush=True)
    if failed:
        print("failed papers:", flush=True)
        for item in failed:
            print(f"  {item['arxiv_id']}: {item['error']}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user", file=sys.stderr)
        sys.exit(130)
