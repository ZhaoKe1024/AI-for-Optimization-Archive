
# Rubrics Research
- Autorubric: A Unified Framework for Rubric-Based LLM Evaluation
> https://arxiv.org/abs/2603.00077v1

- RubricEval: A Scalable Human-LLM Evaluation Framework for Open-Ended Tasks
> https://web.stanford.edu/class/cs224n/final-reports/256846781.pdf
> - 关于Rubrics的评估，RubricEval提出需要有：开放性、绝对性、多样评估、可变性、反馈。
> - RubricEval是针对每一个 instruction 生成对应的 Rubric，可谓更极端。

- PaperBench: Evaluating AI's Ability to Replicate AI Research
> - https://www.emergentmind.com/papers/2504.01848
> - https://arxiv.org/pdf/2504.01848
> - 每一篇论文有一个对应的Rubric，这个Rubric是由作者和原论文作者一同完成的，每一个都制定的很惊喜。
> - 这么说它也无法避免这个Rubric太专一，不够开放性的问题。
> 如何评估的？

- Learning to Judge: LLMs Designing and Applying Evaluation Rubrics
> https://arxiv.org/abs/2602.08672
> https://aclanthology.org/2026.findings-eacl.335/
> 关于Rubrics生成的工作一定要看这一篇


# Rubrics Evolve
- RLCER
> Reinforcing Chain-of-Thought Reasoning with Self-Evolving Rubrics. [arXiv link](https://arxiv.org/abs/2602.10885v1)

- RL with Rubrics
> Dr tulu: Reinforcement learning with evolving rubrics for deep research. [arXiv link](https://arxiv.org/abs/2511.19399)
> - 定位：里程碑式工作，首次将"演化"思想引入rubric设计，揭示了静态评价标准必然落后于被评价系统的根本矛盾，并给出动态协同的解决方案。
> - 方法	提出Reinforcement Learning with Evolving Rubrics (RLER)，rubric与策略模型在训练过程中协同演化（co-evolve）
> - 关键创新	Rubric动态吸收模型新探索的信息，提供有区分度的on-policy反馈——即rubric随策略能力提升而"升级"，避免评价标准僵化

# Rubrics-based Learning
- Reinforcement learning with rubric anchors.
> [arXiv link](https://arxiv.org/abs/2508.12790)
> - 方法	构建超10,000条rubric的奖励体系，来源包括人类专家、LLM生成及人机协作；提出以rubric为"锚点"的细粒度风格控制
> - 关键创新	将rubric视为风格与质量的锚定器（anchor），通过锚定特定评价维度来抑制"AI腔调"，增强表达的人性化
> - 核心发现	仅用5K+样本，Qwen-30B-A3B在开放式基准（尤其人文领域）提升5.2%，超越671B参数的DeepSeek-V3达2.4%，且保持通用推理能力

- Breaking the exploration bottleneck: Rubric-scaffolded reinforcement learning for general LLM reasoning.
> [arXiv link](https://arxiv.org/abs/2508.16949)

- Rubrics as rewards: Reinforcement learning beyond verifiable domains.
> [arXiv link](https://arxiv.org/abs/2507.17746)
> - 首次证明rubric可作为有效的训练时奖励信号，打通了"评测标准→训练目标"的闭环。
> - 核心问题	RLVR无法直接应用于医疗、科学等无自动验证器的开放式域
> - 方法	提出RaR框架，将instance-specific rubric的逐项反馈聚合为标量奖励，用于on-policy强化学习
> - 关键创新	系统比较了多种rubric反馈聚合策略（如逐项加权、层次聚合等），发现结构化rubric奖励相比直接Likert打分，能显著降低评价方差

- Chasing the tail: Effective rubric-based reward modeling for large language model post-training.
> [arXiv link](https://arxiv.org/abs/2509.21500)
> - 理论分析证明奖励误设集中在分布尾部；提出利用rubric区分"优秀但多样"的响应，捕获高奖励尾部的精细结构
> - 从理论层面揭示了rubric的抗hack机制——通过多维结构化分解替代单维标量压缩，保留了奖励空间的拓扑结构。
> - 关键创新	Rubric-by-design对off-policy样本的伪影不敏感——可利用强模型生成的改写样本构建rubric，而不直接将其作为训练目标，避免分布偏移
> - 核心发现	Rubric-based rewards显著缓解奖励过度优化，实现更有效的后训练提升

- Healthbench: Evaluating large language models towards improved human health.
> [arXiv link](https://arxiv.org/abs/2505.08775)
> - 构建5000轮多轮对话，由262名医生撰写对话特定的评分标准（rubric），共48562条独立评价维度
> - o3得分60%，GPT-4.1 nano以1/25成本超越GPT-4o，显示小模型在细粒度rubric引导下可大幅跃升

