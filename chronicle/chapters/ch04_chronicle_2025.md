# 第 4 章 2025 年度编年史：可验证强化学习（RLVR）与测试时推理超级周期

> **[LEARNING OBJECTIVES · 本章学习目标]**
> 1. 深入理解 2025 年“DeepSeek-R1 冲击波”如何引爆全年 6,466 篇论文的强化学习与推理超级周期（Reasoning 主领域占比跃居全库第一）。
> 2. 掌握 2025 年围绕长思维链（Long CoT）展开的正反双向科学求证：从 LIMO“认知模板假说”、强化预训练（RPT）、群组序列策略优化（GSPO）、集体 RL 经验共享，到《思考的幻觉》与思维链镜像质疑。
> 3. 追踪推理范式向多模态（InternVL3、GLM-4.1V-Thinking、Thinking with Video）、超小递归网络（Tiny Recursive Models）与代码安全基准（A.S.E）的全方位扩散。

---

## 4.1 时代背景：当纯强化学习自发涌现“顿悟时刻（Aha Moment）”

如果要在 2023–2026 四年人工智能编年史中选出最具戏剧性的单一分水岭事件，那无疑是 **2025 年 1 月**。在此之前，尽管理论界已知增加推理期算力（Test-Time Compute）能够提升复杂问题求解率，但主流方案仍严重依赖昂贵的人工步骤标注、复杂蒙特卡洛树搜索（MCTS）或独立过程奖励模型（PRM），且核心配方封闭于商业黑盒之内。

2025 年全年归档论文再度暴增 **89.0%** 达到 **6,466 篇**，附带 GitHub 开源代码的比例创下四年最高纪录 **69.66%**。在十大主领域中，**推理与测试时计算（Reasoning & TTC）**从 2024 年的 240 篇猛增近 **5 倍**至 **1,156 篇**，历史性地超越视觉生成与多模态，登顶年度第一大赛道！

<!-- AUTO-SYNC:START:year_2025_table -->

### 表 4.1 2025 年度归档核心统计与 Top 12 社区最高影响力论文榜

- **年度收录总量**：**6,466 篇**（季度分布：`2025-Q1`: 1,382 篇 · `2025-Q2`: 1,778 篇 · `2025-Q3`: 1,338 篇 · `2025-Q4`: 1,968 篇）
- **平均社区热度**：**24.71 Upvotes** ｜ **代码仓库开源率**：**69.7%**

| 排名 | 日期 | ArXiv ID | 论文标题 | 机构 | 主领域 | Upvotes |
| ---: | :--- | :--- | :--- | :--- | :--- | ---: |
| 1 | `2025-09-10` | [2509.08721](https://arxiv.org/abs/2509.08721) | [Sharing is Caring: Efficient LM Post-Training with Colle...](https://huggingface.co/papers/2509.08721) | Gensyn | 训练与强化学习 | **662** |
| 2 | `2025-10-01` | [2509.26507](https://arxiv.org/abs/2509.26507) | [The Dragon Hatchling: The Missing Link between the Trans...](https://huggingface.co/papers/2509.26507) | Pathway | 模型架构与序列建模 | **547** |
| 3 | `2025-10-08` | [2510.04871](https://arxiv.org/abs/2510.04871) | [Less is More: Recursive Reasoning with Tiny Networks](https://huggingface.co/papers/2510.04871) | Samsung  AI Lab (SAI.. | 推理与测试时计算 | **509** |
| 4 | `2025-01-23` | [2501.12948](https://arxiv.org/abs/2501.12948) | [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs ...](https://huggingface.co/papers/2501.12948) | DeepSeek | 推理与测试时计算 | **442** |
| 5 | `2025-09-01` | [2508.18106](https://arxiv.org/abs/2508.18106) | [A.S.E: A Repository-Level Benchmark for Evaluating Secur...](https://huggingface.co/papers/2508.18106) | — | 智能体与代码工程 | **349** |
| 6 | `2025-05-19` | [2505.09388](https://arxiv.org/abs/2505.09388) | [Qwen3 Technical Report](https://huggingface.co/papers/2505.09388) | Qwen | 推理与测试时计算 | **338** |
| 7 | `2025-07-25` | [2507.18071](https://arxiv.org/abs/2507.18071) | [Group Sequence Policy Optimization](https://huggingface.co/papers/2507.18071) | Qwen | 训练与强化学习 | **319** |
| 8 | `2025-04-15` | [2504.10479](https://arxiv.org/abs/2504.10479) | [InternVL3: Exploring Advanced Training and Test-Time Rec...](https://huggingface.co/papers/2504.10479) | — | 多模态与统一基座 | **306** |
| 9 | `2025-04-04` | [2504.01990](https://arxiv.org/abs/2504.01990) | [Advances and Challenges in Foundation Agents: From Brain...](https://huggingface.co/papers/2504.01990) | — | 智能体与代码工程 | **303** |
| 10 | `2025-12-02` | [2511.18538](https://arxiv.org/abs/2511.18538) | [From Code Foundation Models to Agents and Applications: ...](https://huggingface.co/papers/2511.18538) | Beihang University | 训练与强化学习 | **301** |
| 11 | `2025-01-15` | [2501.08313](https://arxiv.org/abs/2501.08313) | [MiniMax-01: Scaling Foundation Models with Lightning Att...](https://huggingface.co/papers/2501.08313) | — | 模型架构与序列建模 | **300** |
| 12 | `2025-08-18` | [2508.10104](https://arxiv.org/abs/2508.10104) | [DINOv3](https://huggingface.co/papers/2508.10104) | AI at Meta | 训练与强化学习 | **299** |

<!-- AUTO-SYNC:END:year_2025_table -->

---

## 4.2 季度演进脉络：2025 年四季度深度复盘

### 2025 Q1（1–3 月）：DeepSeek-R1 震源、rStar-Math 与 LIMO“少即是多推理假说”

2025 年开年短短数周，推理研究的底层逻辑被彻底改写：

- **纯 RL 激励推理涌现**：1 月 23 日归档的 **DeepSeek-R1**（`2501.12948`，442 赞）证明：无需任何监督微调（SFT）冷启动示范，直接在大规模基座模型（DeepSeek-V3-Base）上施加基于规则可验证奖励（数学答案匹配 + 代码编译测试）的 GRPO 强化学习（即 DeepSeek-R1-Zero），模型便会自发拉长思维链，并涌现出自我验算、回溯纠错（Backtracking）与策略切换的**“顿悟时刻（Aha Moment）”**！同时，将大推理模型的轨迹蒸馏至 1.5B–70B 稠密小模型，效果显著优于直接在小基座上从零跑 RL。
- **小模型自博弈与极简激发假说**：几乎同一时期，**rStar-Math**（`2501.04519`，288 赞）通过代码增强思维链合成与自演化过程偏好模型，让 7B 小模型在 AIME 数学竞赛上追平甚至超越 o1-preview；2 月发表的 **LIMO（Less is More for Reasoning）**（`2502.02737` 同月归档，高热）更是抛出震撼发现——仅用 **817 条**精心编排的长推理样本对强预训练基座做监督微调，即可在 AIME 上从 6.5% 飙升至 **57.1%**、MATH 达 **94.8%**，由此提出著名的“少即是多推理假说”：复杂推理的知识早已编码在预训练基座中，后训练仅需极少量高质量“认知模板”即可解锁。
- **长上下文线性闪电注意力与端侧过训练**：**MiniMax-01**（`2501.08313`，300 赞）以闪电注意力（Lightning Attention）混合架构将生产级上下文推向 400 万词元；Hugging Face 推出 **SmolLM2**（`2502.02737`，256 赞），公开 1.7B 参数在 11 万亿词元上多阶段数据中心化过训练的完整开源配方。

> **[LANDMARK STUDY · 里程碑论文精读]** **DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL (ArXiv: 2501.12948 · DeepSeek · 2025-01 · 442 Upvotes)**
> - **核心观点**：复杂逻辑推理与自我反思并非必须通过模仿人类书写的步骤级标注习得；在强大基座上仅凭结果级确定性可验证奖励（RLVR），强化学习即可自主探索并涌现结构化高级认知行为。
> - **方法与实验**：先在无 SFT 条件下训练 DeepSeek-R1-Zero 验证纯 RL 涌现现象；随后设计“千条可读性冷启动数据 → 面向推理的 GRPO → 拒绝采样合成全任务 SFT → 全场景对齐 RL”四阶段流水线训练完整版 DeepSeek-R1，并向 Qwen/Llama 1.5B–70B 蒸馏。
> - **实验结论**：DeepSeek-R1 在 AIME 2024 取得 **79.8%** pass@1、MATH-500 达 **97.3%**、Codeforces 达 96.3 百分位，正面匹敌 OpenAI o1-1217，且开源全部权重与蒸馏模型族。
> - **核心启示**：将“可验证奖励强化学习（RLVR）+ 推理轨迹蒸馏”确立为 2025–2026 年全行业标准后训练流水线。

### 2025 Q2（4–6 月）：双模切换 Qwen3、强化预训练与“思考的幻觉”大辩论

第二季度论文数冲高至 **1,778 篇**，研究呈现“全线扩容”与“冷静祛魅”交锋：

- **开源双模基座与多模态推理**：5 月 **Qwen3 Technical Report**（`2505.09388`，338 赞）率先在单一统一框架内原生融合“思考模式（Thinking Mode）”与“非思考快答模式（Non-Thinking Mode）”，引入思考预算动态控制机制；4 月 **InternVL3**（`2504.10479`，306 赞）采用原生多模态预训练（Native Multimodal Pre-Training）打破先训纯文本再绑视觉编码器的传统，确立开源多模态新标杆；**MiniMax-M1**（`2506.13585`，273 赞）验证线性注意力在超长测试时计算扩展上的显存与吞吐巨大优势。
- **RL 前移至预训练**：6 月 **Reinforcement Pre-Training（强化预训练）**（`2506.08007`，263 赞）大胆将“预测下一个词元”重构为可验证推理强化学习任务——每猜对一个真实下词即获精确奖励，把原本仅限于后训练的 RL 扩展性直接注入海量无标注预训练语料！
- **对长思维链的犀利解剖**：6 月两篇关键分析论文引发广泛反思——苹果团队在 *The Illusion of Thinking* 中通过汉诺塔等可精确控制复杂度的规划谜题证明：当问题规模越过特定阈值，前沿推理模型的准确率并非平缓下降，而是连同有效思考长度一起发生断崖式崩溃；同期 *Skip the Wait* 发现强行截断或跳过相当比例的“嗯、等等、让我再检查一下”等戏剧化反思词元，最终准确率几乎不受影响，直接引出了下半年对**过度思考（Overthinking）**的治理浪潮。

### 2025 Q3（7–9 月）：集体 RL 经验共享登顶全年、序列级策略优化与代码安全警钟

第三季度诞生了 **2025 全年最高赞论文（662 赞）** 与多项算法基石：

- **去中心化群体强化学习**：Gensyn 团队于 9 月发表 **Sharing is Caring**（`2509.08721`，**662 赞**，2023–2026 全库单篇最高热度！），提出去中心化群体后训练范式——让异构节点上的多个语言模型在本地生成推理轨迹并通过点对点网络共享经验与群体评判反馈（Swarm RL），无需中心化巨型算力集群即可高效提升复杂推理性能。
- **从词元级到序列级重要性采样**：Qwen 团队在 7 月发表 **GSPO（Group Sequence Policy Optimization）**（`2507.18071`，319 赞），指出 GRPO 在词元级别施加重要性比率裁剪会导致长序列与 MoE 模型训练中的高方差与崩溃，改为基于整条序列似然几何均值定义序列级重要性权重，彻底稳住了千亿级 MoE 大规模 RL 训练。
- **视觉自监督基石与 AI 代码安全红灯**：Meta 推出 **DINOv3**（`2508.10104`，299 赞）刷新通用密集视觉表征；而 **A.S.E**（`2508.18106`，349 赞）构建首个真实仓库级 AI 生成代码安全评测集，揭示即便在功能测试高分通过的领先编码智能体补丁中，仍潜伏着高比例可被利用的安全漏洞。

### 2025 Q4（10–12 月）：脑启发架构、微型递归网络击败大模型与视频思维涌现

年末第四季度创下单季 **1,968 篇** 的历史最高产量纪录，异端思想大放异彩：

- **连接大脑与 Transformer 的缺失一环**：Pathway 团队发表 **The Dragon Hatchling (BDH)**（`2509.26507`，10 月 1 日归档，**547 赞**，全年热度第二），提出基于局部交互神经元粒子图的无标度生物启发网络，兼具 Transformer 的尺度定律表现、原生无损可组合性与类脑突触可塑性推理状态。
- **700 万参数微型递归网络逆袭千亿大模型**：三星 SAIL 蒙特利尔实验室发表 *Less is More: Recursive Reasoning with Tiny Networks*（`2510.04871`，**509 赞**，全年热度第三），证明仅 **7M 参数**的双层微型网络通过在隐状态上反复递归迭代更新答案草稿（Tiny Recursive Model，TRM），在 ARC-AGI-1（45%）、Sudoku-Extreme 与复杂迷宫求解上大幅击败参数量大数万倍的主流大语言模型！同期字节 Seed 提出 *Scaling Latent Reasoning via Looped Language Models*（`2510.25741`，229 赞），将隐空间循环推理推向规模化。
- **视频即推理媒介与智能体先验学习**：OpenMOSS 提出 **Thinking with Video**（`2511.04570`，241 赞），展示视频生成模型可以通过生成连续视觉演化帧来求解迷宫、几何与物理推理问题，打通视觉生成与多模态推理；Meta 提出 *Agent Learning via Early Experience*（`2510.08558`，273 赞），探索无外部奖励条件下智能体从自身早期交互状态转移中自监督学习环境动力学；年底 **DeepSeek-V3.2**（`2512.02556`，261 赞）与代码智能体全景指南（`2511.18538`，301 赞）为 2025 画上圆满句号。

---

## 4.3 本章小结（Chapter Summary）

- 2025 年是人工智能从“统计续写与静态对齐”跃入“强化学习自主探索与测试时深度思考”的超级周期，推理与强化学习双轮驱动全年近 6,500 篇高密度创新。
- 技术纵深上，训练算法完成了从 GRPO 到序列级 GSPO、强化预训练（RPT）与去中心化群体经验共享（Sharing is Caring）的全面进化；架构上涌现出微型递归网络（TRM）、循环隐式推理与生物启发 BDH 等颠覆“唯参数规模论”的新物种。
- 对“过度思考”与“思考幻觉”的批判性审视，以及“视频即推理”、“代码仓库级智能体”的兴起，直接为 2026 年智能体脚手架与物理世界模型的全面接棒铺平了道路。

---

## 4.4 思考与前沿研讨问题（Review & Research Questions）

1. **SFT 与 RL 的角色再定位**：结合 DeepSeek-R1、LIMO 与 *Demystifying Long CoT* 的实验结论，辨析预训练基座、少量认知模板 SFT 与大规模可验证奖励强化学习（RLVR）各自在构建复杂推理能力时承担的不可替代职能。
2. **递归深度 vs 参数宽度**：为什么仅 7M 参数的微型递归模型（TRM）能在 ARC-AGI 等抽象规则推理基准上超越千亿级单遍自回归大模型？这种隐空间迭代计算对传统计算图设计有何启发？
3. **重要性采样粒度**：从数学方差控制与 MoE 专家路由抖动的角度，解释为什么 GSPO 的序列级似然比率比词元级裁剪更适合长思维链强化学习？
