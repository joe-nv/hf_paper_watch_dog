# 附录 C 人工智能前沿双向术语一致性对照表（Bilingual Technical Glossary）

为确保全书各章节及 `summaries/` 逐篇精读库在跨年度、跨赛道叙述中的概念严密性，本表严格按照“一概念一锁定主译名、近义异词分立建档、首次出现括注英文原词与标准缩写、备选译法仅入附表不在正文混用”的术语管控规范编制。

<!-- AUTO-SYNC:START:appendix_glossary -->

| 方向 | 源语言术语 (English Term) | 目标语主译名 (锁定) | 常见别名 / 备选译法 | 语境与定名说明 |
| :--- | :--- | :--- | :--- | :--- |
| EN→ZH | `Large Language Model (LLM)` | **大语言模型** | 大型语言模型 | 基础文本与通用生成基座统称 |
| EN→ZH | `Multimodal Large Language Model (MLLM)` | **多模态大语言模型** | 多模态大模型 | 融合图文音视频理解或生成的语言基座 |
| EN→ZH | `Vision-Language Model (VLM)` | **视觉-语言模型** | 图文大模型 | 面向视觉与自然语言联合表征的模型 |
| EN→ZH | `Vision-Language-Action Model (VLA)` | **视觉-语言-动作模型** | 具身动作大模型 | 直接输出机器人控制动作轨迹的多模态策略基座 |
| EN→ZH | `World Model` | **世界模型** | 环境动力学模型 | 对物理或交互环境状态转移进行预测与模拟的生成模型 |
| EN→ZH | `World-Action Model (WAM)` | **世界-动作模型** | 世界预测控制模型 | 联合建模环境演化预测与动作生成的具身架构 |
| EN→ZH | `State Space Model (SSM)` | **状态空间模型** | 状态空间序列模型 | 以线性复杂度处理长序列的递归/卷积对偶架构（如 Mamba） |
| EN→ZH | `Mixture-of-Experts (MoE)` | **混合专家架构** | 专家混合模型 | 按输入动态激活稀疏子网络参数的扩容架构 |
| EN→ZH | `Mixture-of-Depths (MoD)` | **混合深度路由** | 动态层跳过机制 | 按词元难度动态分配计算层深度的自适应机制 |
| EN→ZH | `Manifold-Constrained Hyper-Connections (mHC)` | **流形约束超连接** | 超连接残差替代架构 | 突破传统残差跨层连接瓶颈的流形受限多路连接机制 |
| EN→ZH | `Diffusion Language Model (DLM)` | **扩散语言模型** | 离散扩散大模型 | 以并行迭代去噪替代自回归逐词生成的语言模型（如 LLaDA） |
| EN→ZH | `Linear Attention` | **线性注意力** | 亚二次复杂度注意力 | 消除标准 Softmax 注意力二次序列长度复杂度的核近似或门控注意力 |
| EN→ZH | `Rotary Position Embedding (RoPE)` | **旋转位置编码** | 旋转式位置嵌入 | 通过复平面旋转矩阵注入相对位置信息的编码机制 |
| EN→ZH | `Supervised Fine-Tuning (SFT)` | **监督微调** | 有监督精调 | 利用示范输入-输出对进行最大似然指令适配的后训练阶段 |
| EN→ZH | `Low-Rank Adaptation (LoRA)` | **低秩适配** | 低秩微调 | 冻结主干权重、仅训练低秩分解矩阵的参数高效微调方法 |
| EN→ZH | `Quantized LoRA (QLoRA)` | **量化低秩适配** | 4比特LoRA微调 | 在4比特量化基座上挂载高精度低秩适配器的单卡微调方案 |
| EN→ZH | `Reinforcement Learning from Human Feedback (RLHF)` | **基于人类反馈的强化学习** | 人类反馈强化学习 | 通过人类偏好奖励模型对齐大模型输出的经典后训练范式 |
| EN→ZH | `Direct Preference Optimization (DPO)` | **直接偏好优化** | 无奖励模型偏好对齐 | 将奖励建模隐式重参数化为分类损失的离线对齐算法 |
| EN→ZH | `Group Relative Policy Optimization (GRPO)` | **群组相对策略优化** | 组内相对策略优化 | 省去独立价值网络、利用同提示采样组内相对奖励计算优势的强化学习算法 |
| EN→ZH | `Reinforcement Learning with Verifiable Rewards (RLVR)` | **可验证奖励强化学习** | 基于规则奖励的强化学习 | 使用数学答案、编译器或单元测试等确定性验证器提供奖励信号的训练范式 |
| EN→ZH | `Reinforcement Pre-Training (RPT)` | **强化预训练** | 预训练阶段强化学习 | 将强化学习奖励信号前移至预训练词元预测阶段的范式 |
| EN→ZH | `On-Policy Distillation` | **同策略蒸馏** | 在线策略知识蒸馏 | 在学生模型自身采样轨迹上接受教师分布监督以消除分布偏移的蒸馏方法 |
| EN→ZH | `Data Curation` | **数据精选与治理** | 数据筛选、数据配比优化 | 面向预训练或后训练的数据质量评估、去重、配比与课程编排 |
| EN→ZH | `Synthetic Data` | **合成数据** | 模型生成训练数据 | 由模型自动构造、过滤并验证的高质量训练样本与交互轨迹 |
| EN→ZH | `Chain-of-Thought (CoT)` | **思维链** | 链式思考 | 模型在给出最终答案前显式生成中间推理步骤的机制 |
| EN→ZH | `Test-Time Compute Scaling` | **测试时计算扩展** | 推理期算力缩放 | 在推理阶段通过更长思考链、并行采样或验证搜索换取更高准确率的范式 |
| EN→ZH | `Process Reward Model (PRM)` | **过程奖励模型** | 步骤级奖励模型 | 对推理链中每一步中间推导进行细粒度打分验证的判别模型 |
| EN→ZH | `Latent Reasoning` | **潜在空间推理** | 隐状态连续推理 | 不经过离散表层词元解码、直接在连续隐藏表征空间迭代的推理方式 |
| EN→ZH | `Hybrid Thinking` | **混合思考模式** | 快慢双模自适应推理 | 在单模型内按任务复杂度动态切换直觉快答与深度慢思考的机制 |
| EN→ZH | `Overthinking` | **过度思考** | 冗余推理膨胀 | 推理模型在简单问题上生成大量无效反思词元导致延迟飙升甚至准确率下降的现象 |
| EN→ZH | `Post-Training Quantization (PTQ)` | **训练后量化** | 后量化压缩 | 无需重新训练、直接将预训练浮点权重与激活映射至低比特表示的技术 |
| EN→ZH | `Quantization-Aware Training (QAT)` | **量化感知训练** | 低比特原生训练 | 在前向传播中模拟低比特舍入误差以保持极低位宽精度的训练方法（如 1.58-bit） |
| EN→ZH | `KV Cache` | **键值缓存** | KV缓存 | 自回归解码期间缓存历史词元注意力键与值张量以避免重复计算的显存结构 |
| EN→ZH | `Speculative Decoding` | **推测解码** | 投机采样加速 | 由轻量草稿模型快速猜词、目标大模型并行校验以实现无损加速解码的推理机制 |
| EN→ZH | `Small Language Model (SLM)` | **小语言模型** | 轻量级端侧大模型 | 参数量通常在 0.5B–14B 之间、面向端侧与高吞吐场景深度过训练的模型 |
| EN→ZH | `Early Fusion` | **早期模态融合** | 原生统一词元融合 | 将图像、音频、文本统一离散化或投影至同一主干网络从底层联合建模的架构 |
| EN→ZH | `Visual Grounding` | **视觉定位与指代对齐** | 视觉锚定 | 将文本语义精确绑定到图像/视频空间坐标、边界框或界面元素的能力 |
| EN→ZH | `Agentic Harness` | **智能体运行脚手架** | 智能体控制框架、代理编排器 | 围绕基础模型构建提示管理、规划循环、工具执行、记忆状态与校验反馈的系统层封装 |
| EN→ZH | `Tool Use` | **工具调用** | 外部函数与接口调用 | 模型自主决策生成结构化API请求、执行代码或检索外部环境并解析返回值的能力 |
| EN→ZH | `Skill Distillation` | **技能蒸馏与封装** | 代码库转技能 | 将复杂代码仓库、专家轨迹或操作流程提炼为智能体可复用模块化技能包的过程 |
| EN→ZH | `Recursive Self-Improvement (RSI)` | **递归自我改进** | 自主迭代进化 | 智能体通过自我合成环境任务、自我评测与策略更新实现持续能力跃迁的闭环机制 |
| EN→ZH | `Diffusion Model` | **扩散模型** | 去噪扩散概率模型 | 通过学习从高斯噪声逐步反向去噪生成高保真图像、视频或动作分布的生成范式 |
| EN→ZH | `Flow Matching` | **流匹配** | 连续归一化流匹配 | 学习将噪声分布沿直线常微分方程轨迹映射至目标数据分布的高效生成方法 |
| EN→ZH | `3D Gaussian Splatting (3DGS)` | **三维高斯泼溅** | 3D高斯点云渲染 | 利用数百万显式三维各向异性高斯椭球实现实时辐射场重建与光栅化渲染的技术 |
| EN→ZH | `Sim-to-Real Transfer` | **仿真到现实迁移** | 虚实迁移 | 克服物理仿真器与真实世界动力学及传感器域差以部署机器人控制策略的技术 |
| EN→ZH | `Action Chunking` | **动作分块预测** | 多步动作序列预测 | 单次推理联合输出未来短窗口连续控制序列以缓解复合误差与高频控制延迟的策略机制 |
| EN→ZH | `Physical Agency` | **物理主体性** | 物理环境自主执行力 | 智能系统在三维物理世界中融合感知、空间记忆、规划与动作闭环达成物理目标的综合能力 |
| EN→ZH | `Retrieval-Augmented Generation (RAG)` | **检索增强生成** | 外挂知识检索生成 | 在生成前动态检索外部知识库并注入上下文以提升事实准确性与时效性的架构 |
| EN→ZH | `Persistent Memory` | **持久记忆机制** | 跨会话长程记忆 | 突破有限上下文窗口、在长周期交互中压缩、存储与按需召回关键状态信息的记忆模块 |
| EN→ZH | `Continual Learning` | **持续学习** | 终身学习、增量学习 | 模型在不断吸收新任务与新知识的同时避免灾难性遗忘历史能力的机制 |
| EN→ZH | `Machine Unlearning` | **机器遗忘** | 模型定向知识擦除 | 从已训练模型中精准移除特定隐私、版权或危险知识而不损害通用能力的技术 |
| EN→ZH | `Jailbreak Attack` | **越狱攻击** | 安全护栏绕过攻击 | 通过精心构造对抗提示词诱导对齐模型输出违规或受限内容的红队测试手段 |
| EN→ZH | `Red Teaming` | **红队测试** | 对抗性安全评测 | 系统性探测模型安全边界、潜在偏见、越狱漏洞与代理失控风险的主动攻击评估 |
| EN→ZH | `Hallucination` | **模型幻觉** | 事实性编造 | 生成式模型输出看似流畅自洽但违背客观事实或偏离输入证据的现象 |
| EN→ZH | `Alignment Entropy` | **对齐熵增** | 多智能体安全衰减 | 自演化或多智能体交互系统在缺乏外部锚定时安全约束随迭代自然退化的现象 |
| EN→ZH | `CoT Monitorability` | **思维链可监控性** | 推理过程忠实度审计 | 通过审查模型中间思维链日志来检测隐蔽意图、欺骗行为或奖励黑客的可审计性质 |
| EN→ZH | `Mechanistic Interpretability` | **机制可解释性** | 电路级机理可解释性 | 逆向工程神经网络内部特征表征、注意力头与计算电路以理解模型因果机制的研究方向 |
| EN→ZH | `Sparse Autoencoder (SAE)` | **稀疏自编码器** | 过完备稀疏字典学习 | 将神经网络多义叠加激活解耦为单义可解释特征方向的无监督探针工具 |
| EN→ZH | `Out-of-Distribution (OOD) Generalization` | **分布外泛化** | 跨域泛化能力 | 模型在显著偏离训练数据分布的新场景、新形态或新规则下保持有效推理与控制的能力 |
| EN→ZH | `Scaling Law` | **尺度定律** | 缩放定律、规模法则 | 刻画模型损失或能力随参数量、数据规模及预训练/推理算力呈幂律变化的定量规律 |
| EN→ZH | `In-Context Learning (ICL)` | **上下文学习** | 少样本提示学习 | 无需更新模型权重、仅凭上下文输入中的示例或指令即时适配新任务的涌现机制 |
| EN→ZH | `Zero-Shot Generalization` | **零样本泛化** | 零样本迁移 | 在未见过目标任务任何训练样本的情况下直接完成任务指令或真机控制的能力 |
| EN→ZH | `Pareto Frontier` | **帕累托前沿** | 性能-成本最优边界 | 在准确率与算力开销、延迟或参数规模等多目标权衡中无法单向改进的最优解集合 |
| EN→ZH | `Contamination-Free Benchmark` | **无数据污染基准** | 防泄漏动态评测集 | 通过动态更新题目、私有化测试集或程序化生成防止预训练语料刷榜的评测体系 |

<!-- AUTO-SYNC:END:appendix_glossary -->
