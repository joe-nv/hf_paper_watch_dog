# 第 12 章 视觉生成、三维世界模型与具身物理代理：从像素合成美学走向牛顿定律与真机全身控制

> **[LEARNING OBJECTIVES · 本章学习目标]**
> 1. 追踪视觉生成赛道从 2023 年“生成好看的二维静态图”向 2025–2026 年“生成遵循物理定律、可实时交互的三维与四维世界模型（World Models）”的深刻转型。
> 2. 掌握流匹配（Flow Matching）、单流扩散（Single-Stream Diffusion）、扩散强化学习（DiffusionART）以及三维高斯泼溅（3DGS）与智能体骨骼绑定（Agentic Rigging）的技术脉络。
> 3. 系统理解具身智能（Embodied AI）在 2026 年的全面爆发：跨本体视觉-语言-动作基座（Being-H0.5 / Green-VLA）、实时状态空间扩散人形控制（Motion Mamba 2.0）、前沿模型即策略脚手架（Embo-Harness）与物理主体性评测（WorldLeague）。

---

## 12.1 两条曲线的交汇：当“视觉想象引擎”装上“机器人身体”

在第 1 章的全景桑基图（图 1.2）中，我们观察到了一个极具启示性的现象：**视觉生成与世界模型**（`Vision & World`）与**具身智能与物理代理**（`Embodied & VLA`）正在经历深刻的职能重塑与合流。2023 年，扩散模型几乎等同于数字艺术与 AIGC 娱乐工具；而到了 2026 年，视频扩散主干已被公认为构建**通用物理模拟器与世界模型**的最佳候选底座，其下游最核心的消费者正是需要在物理空间中预测动作后果的具身机器人与自动驾驶系统（见图 11.1 右面板）。

<!-- AUTO-SYNC:START:domain_stats_Vision_World -->

### 实证数据切片：视觉生成、3D与世界模型（跨年度演化指标与代表作）

| 统计维度 | 2023 | 2024 | 2025 | 2026 | 全周期开源率 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **主领域归档篇数** | 423 篇 | 778 篇 | 861 篇 | 691 篇 | 60.7% |
| **跨领域多标签渗透率** | 31.8% | 28.9% | 20.7% | 18.0% | — |

| 年份 | ArXiv | 本赛道高影响力里程碑论文 | 机构 | Upvotes |
| :--- | :--- | :--- | :--- | ---: |
| `2025-08-05` | [2508.02324](https://arxiv.org/abs/2508.02324) | [Qwen-Image Technical Report](https://huggingface.co/papers/2508.02324) | — | **272** |
| `2025-12-01` | [2511.22699](https://arxiv.org/abs/2511.22699) | [Z-Image: An Efficient Image Generation Foundation Model with...](https://huggingface.co/papers/2511.22699) | Tongyi-MAI | **244** |
| `2025-11-07` | [2511.04570](https://arxiv.org/abs/2511.04570) | [Thinking with Video: Video Generation as a Promising Multimo...](https://huggingface.co/papers/2511.04570) | OpenMOSS | **241** |
| `2025-11-20` | [2511.14993](https://arxiv.org/abs/2511.14993) | [Kandinsky 5.0: A Family of Foundation Models for Image and V...](https://huggingface.co/papers/2511.14993) | — | **233** |
| `2026-10-30` | [2610.39633](https://arxiv.org/abs/2610.39633) | [Intrinsic Distribution Matching](https://huggingface.co/papers/2610.39633) | inclusionAI | **233** |
| `2025-02-04` | [2502.01061](https://arxiv.org/abs/2502.01061) | [OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditio...](https://huggingface.co/papers/2502.01061) | — | **223** |

<!-- AUTO-SYNC:END:domain_stats_Vision_World -->

---

## 12.2 视觉与三维生成的范式升级：从去噪采样到物理内嵌世界模型

1. **生成主干的效率与可控性跃迁**：
   二维与视频生成主干经历了从 U-Net 噪声预测向扩散 Transformer（DiT）与**流匹配（Flow Matching）**的全面换代。2025 年底的 **Z-Image**（`2511.22699`，244 赞，单流扩散架构）、**Qwen-Image**（`2508.02324`，272 赞）与 **Kandinsky 5.0**（`2511.14993`）大幅提升了复杂文本渲染与多主体指令遵循精度；2026 年的 **Vidu S2**（`2609.11638`，213 赞）实现实时可交互、可编辑的空间视频生成，**DiffusionART**（`2610.12572`，217 赞）与 **Intrinsic Distribution Matching**（`2610.39633`，233 赞）则进一步解决了扩散模型强化学习微调与少步分布蒸馏的稳定性难题。
2. **三维表征与可动画资产工业化**：
   继 2023 年 **3D Gaussian Splatting** 实现实时辐射场渲染革命后，2024 年 **Depth Anything V2** 攻克通用单目深度估计，**LLaMA-Mesh** 探索用纯文本词元直接生成三维网格；到了 2026 年，研究重心转向复杂异构三维资产的骨骼绑定与精确多阶段运动控制——如北大 **3AGameFactory-Motion**（`2611.30013`）提出 DivDynBench 基准，并通过“智能体编写紧凑参数化骨骼运动程序 + 确定性运动学求解器”精准驱动六大形态类别的三维资产。
3. **从“视觉逼真”到“物理守恒”的世界模型**：
   早期视频生成模型常出现物体凭空穿模、重力失效等反物理破绽。2024 年 **GameNGen** 首开交互式神经游戏模拟先河；2026 年马克斯·普朗克研究所发表 **Physical Simulator In-the-Loop Video Generation**（`2603.06408`），将真实刚体/流体物理引擎实时嵌入视频去噪循环；NAVER **Seoul World Model**（`2603.15583`）与阿里 **ABot-Earth 0.5**（`2606.09967`）将世界模型锚定至真实特大城市与全球三维地理尺度；MMLab@NTU 的 **ViDecide**（`2611.26389`）更直接训练视频扩散模型进行因果状态转移预测与分步决策规划（严格规划成功率从标准视频模型的 23.3% 跃升至 **83.8%**）！

---

## 12.3 具身智能与物理 AI 的 2026 奇点：VLA、人形控制与闭环脚手架

本库数据显示，**具身智能与物理代理**主领域论文从 2023 年的 66 篇一路飙升至 2026 年的 **424 篇**（增长 **6.4 倍**，多标签占比达 **12.9%**），在 2026 年形成了完整的四层技术体系：

<!-- AUTO-SYNC:START:domain_stats_Embodied -->

### 实证数据切片：具身智能与物理代理（跨年度演化指标与代表作）

| 统计维度 | 2023 | 2024 | 2025 | 2026 | 全周期开源率 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **主领域归档篇数** | 66 篇 | 98 篇 | 244 篇 | 434 篇 | 62.5% |
| **跨领域多标签渗透率** | 6.3% | 4.9% | 6.7% | 10.1% | — |

| 年份 | ArXiv | 本赛道高影响力里程碑论文 | 机构 | Upvotes |
| :--- | :--- | :--- | :--- | ---: |
| `2026-02-03` | [2602.00919](https://arxiv.org/abs/2602.00919) | [Green-VLA: Staged Vision-Language-Action Model for Generalis...](https://huggingface.co/papers/2602.00919) | Sber Robotics Center | **315** |
| `2025-09-12` | [2509.09372](https://arxiv.org/abs/2509.09372) | [VLA-Adapter: An Effective Paradigm for Tiny-Scale Vision-Lan...](https://huggingface.co/papers/2509.09372) | — | **249** |
| `2026-09-02` | [2609.00111](https://arxiv.org/abs/2609.00111) | [Qwen-Drive-1.0: An Initial Step towards a Vision-Language Fo...](https://huggingface.co/papers/2609.00111) | Qwen | **229** |
| `2026-10-13` | [2609.39601](https://arxiv.org/abs/2609.39601) | [GroundingPI: A Grounding Foundation Model towards Physical I...](https://huggingface.co/papers/2609.39601) | XPENG AI | **192** |

<!-- AUTO-SYNC:END:domain_stats_Embodied -->

- **第一层：跨本体视觉-语言-动作基座（Cross-Embodiment VLA）**
  针对不同机器人自由度、夹爪形态与控制频率各异导致的“数据孤岛”，2026 年 1 月 **Being-H0.5**（`2601.12993` 等系）将超过 35,000 小时人类手部交互轨迹作为物理交互的“通用母语”，结合 Mixture-of-Flow 架构跨 30 种机器人本体实现通用预训练（LIBERO 达 **98.9%**）；**Green-VLA**（`2602.00919`，315 赞）确立分阶段通才机器人 VLA 训练范式；**VLA-Adapter**（`2509.09372`，249 赞）探索极小规模高效适配；清华 **nanoAstra-9B**（`2611.29338`）则在训成操作策略的同时完整保留 VLM 原有通用视觉认知能力。
- **第二层：前沿多模态模型即策略脚手架（Frontier-Model-as-Policy Harness）**
  **Embo-Harness**（`2611.31201`）通过严密消融实验揭示了一个重磅结论：前沿多模态大模型直接闭环控制机器人时，成败的关键不在于手工编写繁琐技能原语或强求模型直接吐出底层关节角，而在于**准确的空间目标点估计（Spatial Target Estimation）+ 短窗口多步动作分块（Action Chunking）+ 原生视觉工具调用**——仅凭正确脚手架配方即可在 RoboLab-120 上暴涨 **+26.2 个百分点**并实现 15/20 真实世界零样本操作成功。
- **第三层：长程低延迟全身人形运动控制（Humanoid Control）**
  **Motion Mamba 2.0**（`2611.29897`，171 赞）将 Mamba 可恢复递归状态、持久内容记忆（PCM）与自回归根体扩散结合，辅以 CUDA Graph 算子融合实现 **6.14× 加速（276ms 延迟）**，在 Unitree G1 真机上完成长达近 40 秒的连续指令切换全身行走与表现力动作合成。
- **第四层：物理主体性统一标尺（WorldLeague）**
  NUS 推出的 **WorldLeague**（`2611.30989`）构建横跨探索搜证（WorldSeek）、物体重排（WorldShape）与动态适应（WorldShift）60 项仿真机器人任务的统一评测场，同时兼容 VLM、VLA 与 WAM 原生控制接口，以过程进展分（Interactive Score）与物理完成率精准刻画系统的**物理主体性画像（Physical Agency Profile）**。

---

## 12.4 本章小结（Chapter Summary）

- 视觉生成已完成从“像素美学拟合”向“三维几何一致、物理规律内嵌、因果决策可控的世界模拟器”的战略转身。
- 2026 年具身智能通过“人类手部母语大规模预训练（VLA）+ 空间目标导向闭环脚手架 + Mamba-扩散实时控制”，正在跨越困扰机器人学数十年的泛化与实时性鸿沟。

---

## 12.5 思考与前沿研讨问题（Review & Research Questions）

1. **像素预测 vs 物理守恒**：比较“纯数据驱动扩大视频模型规模以隐式拟合重力碰撞”与“如 *Physical Simulator In-the-Loop* 显式在去噪环路耦合可微/经典物理引擎”两条路线在罕见刚体交互场景下的外推可靠性与工程代价。
2. **空间目标 vs 底层轨迹**：为什么 *Embo-Harness* 受控干预实验表明前沿多模态基座更擅长空间目标定位而非直接生成底层关节轨迹？这一发现如何指导“高层语义视觉规划 + 底层高频全身控制器”的分层频率解耦设计？
3. **跨本体动作词元对齐**：面对双足人形机器人、轮式双臂与单机械臂截然不同的动作维度与延迟特性，*Being-H0.5* 的统一动作槽（Unified Action Space）与异步动作分块是如何避免负迁移的？
