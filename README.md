# AI-for-Optimization-Repository
Repository on the application of artificial intelligence technology in the field of optimization

# LLM4OPT

## Survey

[github](https://github.com/BeinuoYang/Awesome-LLM4Opt)

## Multi-Agent
- CoE
    > ICLR2024. Chain-of-Experts: When LLMs Meet Complex Operations Research Problems, openreview [link](https://openreview.net/forum?id=HobyL1B9CZ), [Ziyang Xiao](https://openreview.net/profile?id=~Ziyang_Xiao2), [Dongxiang Zhang](https://openreview.net/profile?id=~Dongxiang_Zhang2), [Yangjun Wu](https://openreview.net/profile?id=~Yangjun_Wu1), [Lilin Xu](https://openreview.net/profile?id=~Lilin_Xu2), [Yuan Jessica Wang](https://openreview.net/profile?id=~Yuan_Jessica_Wang1), [Xiongwei Han](https://openreview.net/profile?id=~Xiongwei_Han1), [Xiaojin Fu](https://openreview.net/profile?id=~Xiaojin_Fu1), [Tao Zhong](https://openreview.net/profile?id=~Tao_Zhong2), [Jia Zeng](https://openreview.net/profile?id=~Jia_Zeng1), [Mingli Song](https://openreview.net/profile?id=~Mingli_Song1), [Gang Chen](https://openreview.net/profile?id=~Gang_Chen6) (ZJU, huawei, PolyUHK)
- OptiMUS
    > ICML2024. OptiMUS: Scalable Optimization Modeling with (MI)LP Solvers and Large Language Models. openreview [link](https://openreview.net/forum?id=YT1dtdLvSN), [Ali AhmadiTeshnizi](https://openreview.net/profile?id=~Ali_AhmadiTeshnizi1), [Wenzhi Gao](https://openreview.net/profile?id=~Wenzhi_Gao1), [Madeleine Udell](https://openreview.net/profile?id=~Madeleine_Udell1) (Stanford)
- LEAN-LLM-OPT
    > arXiv 2026: LLM for Large-Scale Optimization Model Auto-Formulation: Bridging Flexibility and Standardization via Agentic Workflow. Kuo Liang, Yuhang Lu, Jianming Mao, Shuyi Sun, Chunwei Yang, Congcong Zeng, Xiao Jin, Hanzhang Qin, Ruihao Zhu, Chung-Piaw Teo. arXiv [link](https://arxiv.org/abs/2601.09635)
    > SSRN 2025: LLM for Large-Scale Optimization Model Auto-Formulation: A Lightweight Few-Shot Learning Approach. ssrn [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5329027), Github [link](https://github.com/CoraLiang01/LEAN-LLM-OPT)
- ICLR2025 Planning Anything with Rigor: General-Purpose Zero-Shot Planning with LLM-based Formalized Programming. [arXiv link](https://arxiv.org/abs/2410.12112). Github: [link1](https://github.com/yih301/LLMFP), [link2](https://github.com/Rmcrow/LLMFP-llm-planning). Blog: [link](https://news.mit.edu/2025/researchers-teach-llms-to-solve-complex-planning-challenges-0402)
- OptiVer
    > [OptiVer: Unleashing the Power of LLMs for Optimization Modeling](https://openreview.net/forum?id=w696Vhv5B2)
- OR-LLM-Agent
    > OR-LLM-Agent: Automating Modeling and Solving of Operations Research Optimization Problems with Reasoning LLM. Bowen Zhang, Pengcheng Luo, Genke Yang (SJTU.edu.cn), Boon-Hee Soong, Chau Yuen (NTU.sg). arXiv [link](https://arxiv.org/abs/2503.10009), openreview [link](https://openreview.net/forum?id=G2yRrFdEmK).
    > [Github Code](https://github.com/bwz96sco/or_llm_agent). [Huggingface Datasets](https://huggingface.co/datasets/SJTU/BWOR)

## SFT
- CAFA
    > CAFA: Coding as Auto-Formulation Can Boost Large Language Models in Solving Linear Programming Problem, , openreview [link](https://openreview.net/forum?id=xC2xtBLmri), [Haoxuan Deng](https://openreview.net/profile?id=~Haoxuan_Deng2), [Bohao Zheng](https://openreview.net/profile?email=bohao.zheng%40cranfield.ac.uk), [Yirui Jiang](https://openreview.net/profile?email=yirui.jiang%40cranfield.ac.uk), [Trung Hieu Tran](https://openreview.net/profile?email=t.h.tran%40cranfield.ac.uk)
- ORLM
    > OR2025 [ORLM: Training Large Language Models for Optimization Modeling]()
- LLMOPT
    > ICLR 2025 [LLMOPT: Learning to Define and Solve General Optimization Problems from Scratch]()
- OptMATH
- StepORLM
    > ICLR2026 Solver-Informed RL: Grounding Large Language Models for Authentic Optimization Modeling, Openreview [link](https://openreview.net/forum?id=80L235oVBe). [Yitian Chen](https://openreview.net/profile?id=~Yitian_Chen3), [Jingfan Xia](https://openreview.net/profile?id=~Jingfan_Xia1), [Siyu Shao](https://openreview.net/profile?id=~Siyu_Shao1), [Dongdong Ge](https://openreview.net/profile?id=~Dongdong_Ge2), [Yinyu Ye](https://openreview.net/profile?id=~Yinyu_Ye1). NISP [link](https://neurips.cc/virtual/2025/loc/san-diego/poster/119660).
- Step-OPT
    > EMNLP2025 Training LLMs for Optimization Modeling via Iterative Data Synthesis and Structured Validation. Yang Wu, [Yifan Zhang](https://openreview.net/profile?id=~Yifan_Zhang2), Yurong Wu, Yuran Wang, Junkai Zhang, [Jian Cheng](https://openreview.net/profile?id=~Jian_Cheng1). ACL [link](https://aclanthology.org/2025.findings-emnlp.691/)
    > arXiv version: Step-Opt: Boosting Optimization Modeling in LLMs through Iterative Data Synthesis and Structured Validation. Yang Wu, Yifan Zhang, Yurong Wu, Yuran Wang, Junkai Zhang, Jian Cheng. arXiv [link](https://arxiv.org/abs/2506.17637), Github [link](https://github.com/samwu-learn/Step)
    > iclr 2025 reject? Evo-Step: Evolutionary Generation and Stepwise Validation for Optimizing LLMs in OR [openreview link](https://openreview.net/forum?id=aapUBU9U0D)
- LLaMoCo   
    > [LLaMoCo: Instruction Tuning of Large Language Models for Optimization Code Generation]()
- PaMOP
    > IJCAI2025 Guiding Large Language Models in Modeling Optimization Problems via Question Partitioning. [ACL link](https://dl.acm.org/doi/10.24963/ijcai.2025/296), [ijcai pdf link](https://www.ijcai.org/proceedings/2025/0296.pdf), Xiaotian Pan, Junhao Fang, Feng Wu*, Sijia Zhang, Yi-Xiang Hu, Shaoang Li, Xiang-Yang Li∗. USTC.
- LinearizeLLM: An Agent-Based Framework for LLM-Driven Exact Linear Reformulation of Nonlinear Optimization Problems[](https://arxiv.org/abs/2510.15969), Paul-Niklas Ken Kandora, Simon Caspar Zeller, Aaron Jeremias Elsing, Elena Kuss, Steffen Rebennack. Germany.

## RL
- SIRL
    > NIPS2025 Solver-Informed RL: Grounding Large Language Models for Authentic Optimization Modeling, Openreview [link](https://openreview.net/forum?id=80L235oVBe) .[Yitian Chen](https://openreview.net/profile?id=~Yitian_Chen3), [Jingfan Xia](https://openreview.net/profile?id=~Jingfan_Xia1), [Siyu Shao](https://openreview.net/profile?id=~Siyu_Shao1), [Dongdong Ge](https://openreview.net/profile?id=~Dongdong_Ge2), [Yinyu Ye](https://openreview.net/profile?id=~Yinyu_Ye1)
- OR-R1
    > AAAI2026 OR-R1: Automating Modeling and Solving of Operations Research Optimization Problem via Test-Time Reinforcement Learning. [ZhenTan](https://openreview.net/profile?id=~Zhen_Tan2), [Jiheng Zhang](https://openreview.net/profile?id=~Jiheng_Zhang1), [Tianlong Chen](https://openreview.net/profile?id=~Tianlong_Chen1). arXiv [link](https://arxiv.org/abs/2511.09092), Github [link](https://github.com/SCUTE-ZZ/OR-R1)
- MiniOPT

## RAG
- AlphaOPT
    > AlphaOPT: Formulating Optimization Programs with Self-Improving LLM Experience Library. [Openreview link](https://openreview.net/forum?id=aWzHdUUaT8)

## Datasets
- OptMATH-Train
    > ICML2025. OptMATH: A Scalable Bidirectional Data Synthesis Framework for Optimization Modeling. icml [link](https://icml.cc/virtual/2025/poster/46227). openreview [link](https://openreview.net/forum?id=9P5e6iE4WK). [Hongliang Lu](https://openreview.net/profile?id=~Hongliang_Lu3), [Zhonglin Xie](https://openreview.net/profile?id=~Zhonglin_Xie1), [Yaoyu Wu](https://openreview.net/profile?id=~Yaoyu_Wu1), [Can Ren](https://openreview.net/profile?id=~Can_Ren1), [Yuxuan Chen](https://openreview.net/profile?id=~Yuxuan_Chen22), [Zaiwen Wen](https://openreview.net/profile?id=~Zaiwen_Wen1)
- ReSocratic
    > ICLR 2025 OptiBench Meets ReSocratic: Measure and Improve LLMs for Optimization Modeling, openreview [link](https://openreview.net/forum?id=fsDZwS49uY), Github: [link1](https://github.com/yangzhch6/ReSocratic), Github [link2](https://github.com/HoshinoAkua/OptiBench), [Zhicheng Yang](https://openreview.net/profile?id=~Zhicheng_Yang4), [Yiwei Wang](https://openreview.net/profile?id=~Yiwei_Wang2), [Yinya Huang](https://openreview.net/profile?id=~Yinya_Huang1), [Zhijiang Guo](https://openreview.net/profile?id=~Zhijiang_Guo2), [Wei Shi](https://openreview.net/profile?id=~Wei_Shi15), [Xiongwei Han](https://openreview.net/profile?id=~Xiongwei_Han1), [Liang Feng](https://openreview.net/profile?id=~Liang_Feng3), [Linqi Song](https://openreview.net/profile?id=~Linqi_Song1), [Xiaodan Liang](https://openreview.net/profile?id=~Xiaodan_Liang2), [Jing Tang](https://openreview.net/profile?id=~Jing_Tang5).
- Large-Scale-OR (LEAN-LLM-OPT)

- OptiTrust 
    > Toward a Trustworthy Optimization Modeling Agent via Verifiable Synthetic Data Generation, Vinicius Lima, Dzung T. Phan, Jayant Kalagnanam, Dhaval Patel, Nianjun Zhou (us.IBM.com) [arXiv link](https://arxiv.org/abs/2508.03117)


### Benchmarks
- NL4OPT
- Mamo
    > Github: [link](https://github.com/FreedomIntelligence/Mamo)
- ComplexOR (CoE)
- NLP4LP (OptiMUS)
- OptMATH-Bench
- IndustryOR (ORLM)
- ICML.C
- OptiBench
- CO-BENCH
- LogiOR
- IndusCP (ConstraintLLM)


## DeepLearning for Optimization
- BPP-Search
    > ACL2025 [BPP-Search: Enhancing Tree of Thought Reasoning for Mathematical Modeling Problem Solving]()
- Towards Imitation Learning to Branch for MIP: A Hybrid Reinforcement Learning based Sample Augmentation Approach. openreview [link](https://openreview.net/forum?id=NdcQQ82mfy). [Changwen Zhang](https://openreview.net/profile?id=~Changwen_Zhang1), [Wenli Ouyang](https://openreview.net/profile?id=~Wenli_Ouyang1), [Hao Yuan](https://openreview.net/profile?id=~Hao_Yuan5), [Liming Gong](https://openreview.net/profile?id=~Liming_Gong1), [Yong Sun](https://openreview.net/profile?id=~Yong_Sun1), [Ziao Guo](https://openreview.net/profile?id=~Ziao_Guo1), [Zhichen Dong](https://openreview.net/profile?id=~Zhichen_Dong1), [Junchi Yan](https://openreview.net/profile?id=~Junchi_Yan2)

## LLMs for Heuristics
- AlphaEvolve
- EoH
    > GitHub: [link](https://github.com/FeiLiu36/EoH)
- ReEvo
- FM-Agent
    > Github: [link](https://github.com/baidubce/FM-Agent)
- ARS+RouteBench
    > [ARS Automatic Routing Solver with Large Language Models]()
- Efficient Heuristics Generation for Solving Combinatorial Optimization Problems Using Large Language Models. [ACM KDD link](https://dl.acm.org/doi/10.1145/3711896.3736923).
## modeling language
- OR-Tools
    > Document [link](https://developers.google.cn/optimization/introduction?hl=zh-cn). Github [link](https://github.com/google/or-tools).
- pyomo
- PuLP
- Gurobi
- COPT
    > Github [link](https://github.com/COPT-Public/COPT-Release)
- PYCSP3
- CVXPY
- PYSCIOPT

## solvers
- glpk
    > Download [source link](https://www.gnu.org/software/glpk/), [sourceforge link](https://winglpk.sourceforge.net/). Download [winglpk](https://sourceforge.net/projects/winglpk/)
- scip
- ipopt
    > Github [link](https://github.com/coin-or/Ipopt), [documentation](https://coin-or.github.io/Ipopt/). Download the md.zip and set the env path.
- cbc

## Other
- [ORGEval: Graph-Theoretic Evaluation of LLMs in Optimization Modeling](https://arxiv.org/abs/2510.27610v1)
- [Code Retrieval for MILP Instance Generation](https://arxiv.org/abs/2505.11526)
- [Targeted MILP Instance Generation via Formulation Code Retrieval](https://openreview.net/forum?id=09FE8nv4sV)


## MathModel
- MM-Agent

# LLMs for Complex Real word Math Problem
Focusing on AI for Research / AI for Science



# Optimization for LLMs
How to apply optimization model to enhance the LLMs?

[It's Morphing Time: Unleashing the Potential of Multiple LLMs via Multi-objective Optimization](https://arxiv.org/abs/2407.00487)


# Neural CO
- Rethinking Neural Multi-Objective Combinatorial Optimization via Neat Weight Embedding. Jinbiao Chen, [Zhiguang Cao](https://openreview.net/profile?id=~Zhiguang_Cao1), Jiahai Wang, Yaoxin Wu, [Hanzhang Qin](https://openreview.net/profile?id=~Hanzhang_Qin1), Zizhen Zhang, [Yue-Jiao Gong](https://openreview.net/profile?id=~Yue-Jiao_Gong1). openreview [link](https://openreview.net/forum?id=GM7cmQfk2F)
- Light-MILPopt: Solving Large-scale Mixed Integer Linear Programs with Lightweight Optimizer and Small-scale Training Dataset. [Huigen Ye](https://openreview.net/profile?id=~Huigen_Ye1), Hua Xu, Hongyan Wang. openreview [link](https://openreview.net/forum?id=2oWRumm67L)
- HGCN2SP: Hierarchical Graph Convolutional Network for Two-Stage Stochastic Programming. openreview[ link](https://openreview.net/forum?id=8onaVSFTEj), [Yang Wu](https://openreview.net/profile?id=~Yang_Wu8), [Yifan Zhang](https://openreview.net/profile?id=~Yifan_Zhang2), [Zhenxing Liang](https://openreview.net/profile?id=~Zhenxing_Liang1), [Jian Cheng](https://openreview.net/profile?id=~Jian_Cheng7)


Extract Script for openreview page
```javascript
// 提取标题
const titleEl = document.querySelector('h2.citation_title');
const title = titleEl ? titleEl.textContent.trim().replace(/"/g, '') : 'null';

// 提取作者信息
const authorLinks = document.querySelectorAll('.forum-authors a[title]');
const authors = Array.from(authorLinks).map(link => {
  const name = link.textContent.trim();
  const href = link.href || 'null';
  return `[${name}](${href})`;
}).join(', ');

// 构造最终输出字符串
const output = `${title}, ${authors}, openreview [link](null)`;

// 打印结果
console.log(output);
```