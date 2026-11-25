#!/usr/bin/env python3
"""
Shared research taxonomy, subtopic hierarchy, paper-type classifier, and
canonical bilingual terminology registry (consistent-term-translation-polish-guard).
"""

from __future__ import annotations

import re
from collections import OrderedDict

DOMAINS: OrderedDict[str, dict] = OrderedDict(
    [
        (
            "Training_RL",
            {
                "id": "Training_RL",
                "zh": "后训练、强化学习与数据工程",
                "zh_short": "训练与强化学习",
                "en": "Post-Training, RL & Data Curation",
                "en_short": "Training & RL",
                "color": "#1F4E79",
                "pattern": (
                    r"\b(reinforcement learning|\brlhf\b|\bdpo\b|\bgrpo\b|\brlvr\b|\bppo\b|\bgspo\b|\bgdpo\b|\bfipo\b|"
                    r"policy optimization|post-training|pre-training|pretraining|fine-tuning|finetuning|"
                    r"\blora\b|\bqlora\b|\bsft\b|preference optimization|reward model|verifiable reward|"
                    r"synthetic data|data selection|data curation|data mixture|distillation|self-play|"
                    r"curriculum learning|continued pre-training|distributed.*training|credit assignment)\b"
                ),
            },
        ),
        (
            "Reasoning",
            {
                "id": "Reasoning",
                "zh": "推理与测试时计算",
                "zh_short": "推理与测试时计算",
                "en": "Reasoning & Test-Time Compute",
                "en_short": "Reasoning & TTC",
                "color": "#B84A39",
                "pattern": (
                    r"\b(reasoning|chain-of-thought|chains-of-thought|\bcot\b|test-time|tree of thoughts|"
                    r"step-by-step|mathematical|math\b|theorem proving|\blean\b|olympiad|\baime\b|"
                    r"logical|self-correction|process reward|\bprm\b|verifier|thinking mode|hybrid-thinking|"
                    r"overthinking|latent reasoning|recursive reasoning|cognitive map|planning)\b"
                ),
            },
        ),
        (
            "Agents",
            {
                "id": "Agents",
                "zh": "自主智能体与软件工程",
                "zh_short": "智能体与代码工程",
                "en": "Autonomous Agents & Software Engineering",
                "en_short": "Agents & SWE",
                "color": "#2E7D6B",
                "pattern": (
                    r"\b(agent\b|agents\b|agentic|tool use|tool-use|tool learning|function calling|\bmcp\b|"
                    r"multi-agent|software engineering|swe-bench|code generation|coding|code localizer|"
                    r"bug fix|issue resolution|repository-level|web navigation|browser|computer use|"
                    r"harness|harnesses|self-improv|self-evolv|recursive self-improvement|\brsi\b|skill\b|skills\b)\b"
                ),
            },
        ),
        (
            "Multimodal",
            {
                "id": "Multimodal",
                "zh": "多模态理解与统一基座",
                "zh_short": "多模态与统一基座",
                "en": "Multimodal & Unified Foundation Models",
                "en_short": "Multimodal",
                "color": "#6C4F8F",
                "pattern": (
                    r"\b(multimodal|multi-modal|vision-language|\bvlm\b|\bvlms\b|\bmllm\b|\bmllms\b|"
                    r"visual question|image-text|audio-visual|speech|audio|music generation|omni-modal|"
                    r"omnimodal|\bocr\b|document understanding|gui\b|chart|video understanding|"
                    r"video reasoning|video grounding|cross-modal|early fusion)\b"
                ),
            },
        ),
        (
            "Efficiency",
            {
                "id": "Efficiency",
                "zh": "模型效率、量化与系统优化",
                "zh_short": "高效推理与系统",
                "en": "Efficiency, Quantization & Systems",
                "en_short": "Efficiency & Sys",
                "color": "#C98A2C",
                "pattern": (
                    r"\b(quantiz|low-bit|1-bit|1\.58|fp8|int4|pruning|sparsity|sparse|speculative decoding|"
                    r"kv cache|kv-cache|memory-efficient|inference acceleration|fast inference|latency|"
                    r"throughput|token compression|lightweight|small language model|tiny network|"
                    r"on-device|edge device|\bcuda\b|fused kernel|flashattention|offloading)\b"
                ),
            },
        ),
        (
            "Vision_World",
            {
                "id": "Vision_World",
                "zh": "视觉生成、3D与世界模型",
                "zh_short": "视觉生成与世界模型",
                "en": "Visual Generation, 3D & World Models",
                "en_short": "Vision & World",
                "color": "#3B7EA1",
                "pattern": (
                    r"\b(diffusion models?|text-to-image|image generation|video generation|text-to-video|"
                    r"flow matching|3d generation|4d generation|gaussian splatting|\bnerf\b|radiance field|"
                    r"\bmesh\b|rigging|animation|avatar|portrait|image editing|segmentation|segment anything|"
                    r"world models?|scene generation|rendering|visual synthesis)\b"
                ),
            },
        ),
        (
            "Architecture",
            {
                "id": "Architecture",
                "zh": "架构创新与序列建模",
                "zh_short": "模型架构与序列建模",
                "en": "Architecture & Sequence Modeling",
                "en_short": "Architecture",
                "color": "#4A5568",
                "pattern": (
                    r"\b(transformer|attention mechanism|linear attention|lightning attention|differential transformer|"
                    r"softmax attention|attention residuals?|state space|\bssm\b|mamba|rwkv|retnet|hyena|"
                    r"mixture of experts|mixture-of-experts|\bmoe\b|mixture-of-depths|residual connections?|"
                    r"residuals\b|prenorm|postnorm|rmsnorm|layernorm|hyper-connections?|positional encoding|\brope\b|"
                    r"tokenizer|tokenization|\bkan\b|kolmogorov|diffusion language model|diffusion large language|"
                    r"\bllada\b|looped language model|in-context learning|subquadratic)\b"
                ),
            },
        ),
        (
            "Safety_Interp",
            {
                "id": "Safety_Interp",
                "zh": "安全对齐、可信与可解释性",
                "zh_short": "安全对齐与可解释性",
                "en": "Safety, Alignment & Interpretability",
                "en_short": "Safety & Interp",
                "color": "#9E3B52",
                "pattern": (
                    r"\b(safety|alignment|jailbreak|red[- ]teaming|adversarial|hallucination|factuality|"
                    r"unlearning|watermark|copyright|machine-generated text|privacy|bias|fairness|toxicity|"
                    r"guardrail|decepti|interpretability|mechanistic|sparse autoencoder|\bsae\b|probing|"
                    r"model editing|trustworth|vulnerability|security)\b"
                ),
            },
        ),
        (
            "Embodied",
            {
                "id": "Embodied",
                "zh": "具身智能与物理代理",
                "zh_short": "具身智能与物理AI",
                "en": "Embodied AI & Physical Agency",
                "en_short": "Embodied & VLA",
                "color": "#2F6B3C",
                "pattern": (
                    r"\b(robot|robots|robotic|robotics|embodied|humanoid|manipulation|locomotion|"
                    r"vision-language-action|\bvla\b|\bvlas\b|world-action|visuomotor|sim-to-real|"
                    r"grasping|autonomous driving|navigation|physical agency|teleoperation|cross-embodiment)\b"
                ),
            },
        ),
        (
            "Science_Eval",
            {
                "id": "Science_Eval",
                "zh": "科学智能、记忆系统与评测生态",
                "zh_short": "AI4Science与记忆评测",
                "en": "AI for Science, Memory & Evaluation",
                "en_short": "Science & Eval",
                "color": "#5C6B73",
                "pattern": (
                    r"\b(protein|molecule|molecular|drug discovery|chemistry|material|genomic|biology|cell|"
                    r"medical|clinical|fmri|weather|climate|\bpde\b|physics|scientific|"
                    r"benchmark|benchmarks|evaluation suite|leaderboard|"
                    r"continual learning|long-horizon memorization|episodic memory|long-term memory|"
                    r"infinite context|retrieval-augmented|\brag\b|information retrieval|multilingual)\b"
                ),
            },
        ),
    ]
)

SUBTOPICS: list[dict] = [
    {"id": "ssm_linear", "domain": "Architecture", "zh": "状态空间与线性注意力 (SSM/Mamba)", "en": "SSM & Linear Attention", "pattern": r"\b(mamba|state space|\bssm\b|rwkv|retnet|linear attention|lightning attention|subquadratic)\b"},
    {"id": "moe_routing", "domain": "Architecture", "zh": "混合专家与动态深度 (MoE/MoD)", "en": "MoE & Dynamic Routing", "pattern": r"\b(mixture of experts|mixture-of-experts|\bmoe\b|mixture-of-depths|early-exit|dynamic routing)\b"},
    {"id": "dlm_non_ar", "domain": "Architecture", "zh": "扩散语言模型 (Diffusion LLM)", "en": "Diffusion Language Models", "pattern": r"\b(diffusion language model|diffusion large language|\bdlm\b|\bllada\b|discrete diffusion)\b"},
    {"id": "residual_arch", "domain": "Architecture", "zh": "超连接与新型骨干 (mHC/KAN)", "en": "Hyper-Connections & Novel Wiring", "pattern": r"\b(hyper-connection|kolmogorov|\bkan\b|differential transformer|looped language|dragon hatchling)\b"},
    {"id": "peft_sft", "domain": "Training_RL", "zh": "监督微调与参数高效适配 (SFT/LoRA)", "en": "SFT & LoRA/PEFT", "pattern": r"\b(\blora\b|\bqlora\b|parameter-efficient|\bpeft\b|supervised fine-tuning|\bsft\b|instruction tuning)\b"},
    {"id": "dpo_rlhf", "domain": "Training_RL", "zh": "人类反馈与偏好优化 (RLHF/DPO)", "en": "RLHF & Preference Optimization", "pattern": r"\b(\brlhf\b|\bdpo\b|direct preference|preference optimization|reward model)\b"},
    {"id": "rlvr_grpo", "domain": "Training_RL", "zh": "可验证奖励与群组策略优化 (RLVR/GRPO)", "en": "RLVR & Group Policy RL", "pattern": r"\b(\bgrpo\b|\brlvr\b|\bgspo\b|\bgdpo\b|\bfipo\b|verifiable reward|reinforcement pre-training|policy optimization)\b"},
    {"id": "data_synth", "domain": "Training_RL", "zh": "合成数据与精细化配比 (Data Curation)", "en": "Synthetic Data & Curation", "pattern": r"\b(synthetic data|data selection|data curation|data mixture|distillation|weak-driven)\b"},
    {"id": "cot_search", "domain": "Reasoning", "zh": "思维链与树搜索 (CoT & Search)", "en": "CoT & Tree/Graph Search", "pattern": r"\b(chain-of-thought|chains-of-thought|\bcot\b|tree of thoughts|monte carlo tree|\bmcts\b|process reward)\b"},
    {"id": "ttc_scaling", "domain": "Reasoning", "zh": "测试时计算扩展与高效思考 (TTC & Hybrid)", "en": "Test-Time Scaling & Hybrid Thought", "pattern": r"\b(test-time|overthinking|stop thinking|hybrid-thinking|latent reasoning|thinking token)\b"},
    {"id": "math_formal", "domain": "Reasoning", "zh": "数学竞赛与形式化定理证明 (Math & Proof)", "en": "Math & Theorem Proving", "pattern": r"\b(mathematical|olympiad|\baime\b|theorem proving|\blean\b|formal verification)\b"},
    {"id": "quant_lowbit", "domain": "Efficiency", "zh": "极低比特量化 (FP8/INT4/1.58-bit)", "en": "Low-Bit Quantization", "pattern": r"\b(quantiz|1-bit|1\.58|bitnet|fp8|int4|fp4|ternary)\b"},
    {"id": "kv_speculative", "domain": "Efficiency", "zh": "KV缓存压缩与推测解码 (KV & Speculative)", "en": "KV-Cache & Speculative Decoding", "pattern": r"\b(kv cache|kv-cache|speculative decoding|token pruning|token merging|flashattention|cuda graph)\b"},
    {"id": "slm_edge", "domain": "Efficiency", "zh": "小语言模型与端侧推理 (SLM & Edge)", "en": "Small LMs & On-Device", "pattern": r"\b(small language model|tiny network|smollm|phi-3|phi-4|on-device|mobile|lightweight)\b"},
    {"id": "vlm_video_und", "domain": "Multimodal", "zh": "视觉-语言与长视频理解 (VLM & Video)", "en": "VLM & Video Understanding", "pattern": r"\b(vision-language|\bvlm\b|\bmllm\b|video understanding|video reasoning|video grounding)\b"},
    {"id": "omni_fusion", "domain": "Multimodal", "zh": "原生全模态与语音交互 (Omni & Audio)", "en": "Native Omni-Modal & Audio", "pattern": r"\b(omni-modal|omnimodal|early fusion|speech-language|audio-visual|real-time.*interaction)\b"},
    {"id": "doc_ocr_gui", "domain": "Multimodal", "zh": "文档解析、OCR与GUI感知 (Doc/GUI)", "en": "Document, OCR & GUI Grounding", "pattern": r"\b(\bocr\b|document understanding|gui\b|screen|spreadsheet|chart understanding)\b"},
    {"id": "swe_coding", "domain": "Agents", "zh": "软件工程与代码智能体 (SWE & Coding)", "en": "Coding Agents & SWE", "pattern": r"\b(software engineering|swe-bench|issue resolution|bug fix|code generation|code localizer|repository)\b"},
    {"id": "harness_skills", "domain": "Agents", "zh": "智能体脚手架、工具与技能 (Harness & Skills)", "en": "Agent Harnesses, Tools & Skills", "pattern": r"\b(harness|harnesses|tool-use|tool use|\bmcp\b|repo-to-skill|trajectory.*synthesis|multi-agent)\b"},
    {"id": "rsi_self_evol", "domain": "Agents", "zh": "递归自我改进与自主科研 (RSI & AI Scientist)", "en": "Recursive Self-Improvement", "pattern": r"\b(recursive self-improvement|\brsi\b|self-evolving|self-improving|ai scientist|autoresearch)\b"},
    {"id": "img_flow", "domain": "Vision_World", "zh": "图像扩散与流匹配生成 (Diffusion & Flow)", "en": "Image Diffusion & Flow Matching", "pattern": r"\b(text-to-image|image generation|flow matching|image editing|single-stream diffusion)\b"},
    {"id": "video_world", "domain": "Vision_World", "zh": "视频生成与交互世界模型 (Video & World Models)", "en": "Video Gen & World Models", "pattern": r"\b(video generation|text-to-video|world models?|physical simulator|spatial intelligence)\b"},
    {"id": "3d_gs_mesh", "domain": "Vision_World", "zh": "3D高斯泼溅与资产绑定 (3DGS & Rigging)", "en": "3DGS, Mesh & Rigging", "pattern": r"\b(gaussian splatting|\bnerf\b|3d generation|4d generation|\bmesh\b|rigging)\b"},
    {"id": "vla_policy", "domain": "Embodied", "zh": "视觉-语言-动作基座 (VLA & Policy)", "en": "Vision-Language-Action (VLA)", "pattern": r"\b(vision-language-action|\bvla\b|\bvlas\b|frontier-model-as-policy|cross-embodiment|world-action)\b"},
    {"id": "humanoid_manip", "domain": "Embodied", "zh": "人形控制与真机灵巧操作 (Humanoid & Manip)", "en": "Humanoid & Manipulation", "pattern": r"\b(humanoid|locomotion|dexterous|manipulation|sim-to-real|autonomous driving)\b"},
    {"id": "redteam_guard", "domain": "Safety_Interp", "zh": "越狱攻防与智能体护栏 (Red-Team & Guardrails)", "en": "Red-Teaming & Agent Safety", "pattern": r"\b(jailbreak|red[- ]teaming|guardrail|prompt injection|agent.*safety|clawkeeper)\b"},
    {"id": "fact_unlearn", "domain": "Safety_Interp", "zh": "幻觉抑制、机器遗忘与水印 (Factuality & Unlearning)", "en": "Hallucination & Unlearning", "pattern": r"\b(hallucination|factuality|unlearning|watermark|copyright)\b"},
    {"id": "interp_cot_mon", "domain": "Safety_Interp", "zh": "机制可解释性与思维链监控 (Interp & CoT Monitor)", "en": "Mechanistic Interp & CoT Monitoring", "pattern": r"\b(interpretability|mechanistic|sparse autoencoder|\bsae\b|probing|chains? of thought.*control|decepti)\b"},
    {"id": "rag_memory", "domain": "Science_Eval", "zh": "检索增强与长程持续记忆 (RAG & Continual Memory)", "en": "RAG & Long-Horizon Memory", "pattern": r"\b(retrieval-augmented|\brag\b|continual learning|long-horizon memorization|episodic memory|persistent.*memory)\b"},
    {"id": "ai4science", "domain": "Science_Eval", "zh": "科学智能 (生物/化学/物理/医疗)", "en": "AI for Science & Medicine", "pattern": r"\b(protein|molecule|drug discovery|chemistry|material|genomic|medical|clinical|weather|\bpde\b)\b"},
    {"id": "dyn_bench", "domain": "Science_Eval", "zh": "全面评测基准与排行榜 (Holistic Benchmarks)", "en": "Benchmarks & Evaluation", "pattern": r"\b(benchmark|benchmarks|evaluation suite|leaderboard)\b"},
]

_COMPILED_DOMAINS = {k: re.compile(v["pattern"], re.I) for k, v in DOMAINS.items()}
_COMPILED_SUBTOPICS = [(s, re.compile(s["pattern"], re.I)) for s in SUBTOPICS]

# Canonical Bilingual Terminology Registry (following consistent-term-translation-polish-guard)
GLOSSARY_TERMS: list[dict] = [
    {"en": "Large Language Model (LLM)", "zh": "大语言模型", "aliases": "大型语言模型", "notes": "基础文本与通用生成基座统称", "match": r"\blarge language models?\b|\bllms?\b"},
    {"en": "Multimodal Large Language Model (MLLM)", "zh": "多模态大语言模型", "aliases": "多模态大模型", "notes": "融合图文音视频理解或生成的语言基座", "match": r"\bmultimodal large language models?\b|\bmllms?\b"},
    {"en": "Vision-Language Model (VLM)", "zh": "视觉-语言模型", "aliases": "图文大模型", "notes": "面向视觉与自然语言联合表征的模型", "match": r"\bvision-language models?\b|\bvlms?\b"},
    {"en": "Vision-Language-Action Model (VLA)", "zh": "视觉-语言-动作模型", "aliases": "具身动作大模型", "notes": "直接输出机器人控制动作轨迹的多模态策略基座", "match": r"\bvision-language-action\b|\bvlas?\b"},
    {"en": "World Model", "zh": "世界模型", "aliases": "环境动力学模型", "notes": "对物理或交互环境状态转移进行预测与模拟的生成模型", "match": r"\bworld models?\b"},
    {"en": "World-Action Model (WAM)", "zh": "世界-动作模型", "aliases": "世界预测控制模型", "notes": "联合建模环境演化预测与动作生成的具身架构", "match": r"\bworld-action models?\b|\bwams?\b"},
    {"en": "State Space Model (SSM)", "zh": "状态空间模型", "aliases": "状态空间序列模型", "notes": "以线性复杂度处理长序列的递归/卷积对偶架构（如 Mamba）", "match": r"\bstate space models?\b|\bssms?\b|\bmamba\b"},
    {"en": "Mixture-of-Experts (MoE)", "zh": "混合专家架构", "aliases": "专家混合模型", "notes": "按输入动态激活稀疏子网络参数的扩容架构", "match": r"\bmixture[- ]of[- ]experts\b|\bmoe\b"},
    {"en": "Mixture-of-Depths (MoD)", "zh": "混合深度路由", "aliases": "动态层跳过机制", "notes": "按词元难度动态分配计算层深度的自适应机制", "match": r"\bmixture[- ]of[- ]depths\b"},
    {"en": "Manifold-Constrained Hyper-Connections (mHC)", "zh": "流形约束超连接", "aliases": "超连接残差替代架构", "notes": "突破传统残差跨层连接瓶颈的流形受限多路连接机制", "match": r"\bhyper-connections?\b|\bmhc\b"},
    {"en": "Diffusion Language Model (DLM)", "zh": "扩散语言模型", "aliases": "离散扩散大模型", "notes": "以并行迭代去噪替代自回归逐词生成的语言模型（如 LLaDA）", "match": r"\bdiffusion (?:large )?language models?\b|\bllada\b"},
    {"en": "Linear Attention", "zh": "线性注意力", "aliases": "亚二次复杂度注意力", "notes": "消除标准 Softmax 注意力二次序列长度复杂度的核近似或门控注意力", "match": r"\blinear attention\b|\blightning attention\b"},
    {"en": "Rotary Position Embedding (RoPE)", "zh": "旋转位置编码", "aliases": "旋转式位置嵌入", "notes": "通过复平面旋转矩阵注入相对位置信息的编码机制", "match": r"\brotary position|\brope\b"},
    {"en": "Supervised Fine-Tuning (SFT)", "zh": "监督微调", "aliases": "有监督精调", "notes": "利用示范输入-输出对进行最大似然指令适配的后训练阶段", "match": r"\bsupervised fine-tuning\b|\bsft\b"},
    {"en": "Low-Rank Adaptation (LoRA)", "zh": "低秩适配", "aliases": "低秩微调", "notes": "冻结主干权重、仅训练低秩分解矩阵的参数高效微调方法", "match": r"\blow-rank adaptation\b|\blora\b"},
    {"en": "Quantized LoRA (QLoRA)", "zh": "量化低秩适配", "aliases": "4比特LoRA微调", "notes": "在4比特量化基座上挂载高精度低秩适配器的单卡微调方案", "match": r"\bqlora\b"},
    {"en": "Reinforcement Learning from Human Feedback (RLHF)", "zh": "基于人类反馈的强化学习", "aliases": "人类反馈强化学习", "notes": "通过人类偏好奖励模型对齐大模型输出的经典后训练范式", "match": r"\brlhf\b|\breinforcement learning from human feedback\b"},
    {"en": "Direct Preference Optimization (DPO)", "zh": "直接偏好优化", "aliases": "无奖励模型偏好对齐", "notes": "将奖励建模隐式重参数化为分类损失的离线对齐算法", "match": r"\bdirect preference optimization\b|\bdpo\b"},
    {"en": "Group Relative Policy Optimization (GRPO)", "zh": "群组相对策略优化", "aliases": "组内相对策略优化", "notes": "省去独立价值网络、利用同提示采样组内相对奖励计算优势的强化学习算法", "match": r"\bgroup relative policy optimization\b|\bgrpo\b"},
    {"en": "Reinforcement Learning with Verifiable Rewards (RLVR)", "zh": "可验证奖励强化学习", "aliases": "基于规则奖励的强化学习", "notes": "使用数学答案、编译器或单元测试等确定性验证器提供奖励信号的训练范式", "match": r"\brlvr\b|\bverifiable rewards?\b"},
    {"en": "Reinforcement Pre-Training (RPT)", "zh": "强化预训练", "aliases": "预训练阶段强化学习", "notes": "将强化学习奖励信号前移至预训练词元预测阶段的范式", "match": r"\breinforcement pre-training\b"},
    {"en": "On-Policy Distillation", "zh": "同策略蒸馏", "aliases": "在线策略知识蒸馏", "notes": "在学生模型自身采样轨迹上接受教师分布监督以消除分布偏移的蒸馏方法", "match": r"\bon-policy distillation\b"},
    {"en": "Data Curation", "zh": "数据精选与治理", "aliases": "数据筛选、数据配比优化", "notes": "面向预训练或后训练的数据质量评估、去重、配比与课程编排", "match": r"\bdata curation\b|\bdata selection\b"},
    {"en": "Synthetic Data", "zh": "合成数据", "aliases": "模型生成训练数据", "notes": "由模型自动构造、过滤并验证的高质量训练样本与交互轨迹", "match": r"\bsynthetic data\b"},
    {"en": "Chain-of-Thought (CoT)", "zh": "思维链", "aliases": "链式思考", "notes": "模型在给出最终答案前显式生成中间推理步骤的机制", "match": r"\bchains?-of-thought\b|\bcot\b"},
    {"en": "Test-Time Compute Scaling", "zh": "测试时计算扩展", "aliases": "推理期算力缩放", "notes": "在推理阶段通过更长思考链、并行采样或验证搜索换取更高准确率的范式", "match": r"\btest-time compute\b|\btest-time scaling\b|\binference[- ]time compute\b"},
    {"en": "Process Reward Model (PRM)", "zh": "过程奖励模型", "aliases": "步骤级奖励模型", "notes": "对推理链中每一步中间推导进行细粒度打分验证的判别模型", "match": r"\bprocess reward models?\b|\bprms?\b"},
    {"en": "Latent Reasoning", "zh": "潜在空间推理", "aliases": "隐状态连续推理", "notes": "不经过离散表层词元解码、直接在连续隐藏表征空间迭代的推理方式", "match": r"\blatent reasoning\b"},
    {"en": "Hybrid Thinking", "zh": "混合思考模式", "aliases": "快慢双模自适应推理", "notes": "在单模型内按任务复杂度动态切换直觉快答与深度慢思考的机制", "match": r"\bhybrid[- ]thinking\b|\bthinking and non-thinking\b"},
    {"en": "Overthinking", "zh": "过度思考", "aliases": "冗余推理膨胀", "notes": "推理模型在简单问题上生成大量无效反思词元导致延迟飙升甚至准确率下降的现象", "match": r"\boverthinking\b"},
    {"en": "Post-Training Quantization (PTQ)", "zh": "训练后量化", "aliases": "后量化压缩", "notes": "无需重新训练、直接将预训练浮点权重与激活映射至低比特表示的技术", "match": r"\bpost-training quantization\b|\bptq\b"},
    {"en": "Quantization-Aware Training (QAT)", "zh": "量化感知训练", "aliases": "低比特原生训练", "notes": "在前向传播中模拟低比特舍入误差以保持极低位宽精度的训练方法（如 1.58-bit）", "match": r"\bquantization-aware training\b|\bqat\b|\b1\.58[- ]bits?\b"},
    {"en": "KV Cache", "zh": "键值缓存", "aliases": "KV缓存", "notes": "自回归解码期间缓存历史词元注意力键与值张量以避免重复计算的显存结构", "match": r"\bkv[- ]cache\b"},
    {"en": "Speculative Decoding", "zh": "推测解码", "aliases": "投机采样加速", "notes": "由轻量草稿模型快速猜词、目标大模型并行校验以实现无损加速解码的推理机制", "match": r"\bspeculative decoding\b"},
    {"en": "Small Language Model (SLM)", "zh": "小语言模型", "aliases": "轻量级端侧大模型", "notes": "参数量通常在 0.5B–14B 之间、面向端侧与高吞吐场景深度过训练的模型", "match": r"\bsmall language models?\b|\bslms?\b"},
    {"en": "Early Fusion", "zh": "早期模态融合", "aliases": "原生统一词元融合", "notes": "将图像、音频、文本统一离散化或投影至同一主干网络从底层联合建模的架构", "match": r"\bearly fusion\b"},
    {"en": "Visual Grounding", "zh": "视觉定位与指代对齐", "aliases": "视觉锚定", "notes": "将文本语义精确绑定到图像/视频空间坐标、边界框或界面元素的能力", "match": r"\bvisual grounding\b|\bvideo grounding\b"},
    {"en": "Agentic Harness", "zh": "智能体运行脚手架", "aliases": "智能体控制框架、代理编排器", "notes": "围绕基础模型构建提示管理、规划循环、工具执行、记忆状态与校验反馈的系统层封装", "match": r"\bharnesses\b|\bharness\b"},
    {"en": "Tool Use", "zh": "工具调用", "aliases": "外部函数与接口调用", "notes": "模型自主决策生成结构化API请求、执行代码或检索外部环境并解析返回值的能力", "match": r"\btool[- ]use\b|\bfunction calling\b|\btool learning\b"},
    {"en": "Skill Distillation", "zh": "技能蒸馏与封装", "aliases": "代码库转技能", "notes": "将复杂代码仓库、专家轨迹或操作流程提炼为智能体可复用模块化技能包的过程", "match": r"\brepo-to-skill\b|\bskill distillation\b|\bai4ai skills?\b"},
    {"en": "Recursive Self-Improvement (RSI)", "zh": "递归自我改进", "aliases": "自主迭代进化", "notes": "智能体通过自我合成环境任务、自我评测与策略更新实现持续能力跃迁的闭环机制", "match": r"\brecursive self-improvement\b|\brsi\b"},
    {"en": "Diffusion Model", "zh": "扩散模型", "aliases": "去噪扩散概率模型", "notes": "通过学习从高斯噪声逐步反向去噪生成高保真图像、视频或动作分布的生成范式", "match": r"\bdiffusion models?\b"},
    {"en": "Flow Matching", "zh": "流匹配", "aliases": "连续归一化流匹配", "notes": "学习将噪声分布沿直线常微分方程轨迹映射至目标数据分布的高效生成方法", "match": r"\bflow matching\b"},
    {"en": "3D Gaussian Splatting (3DGS)", "zh": "三维高斯泼溅", "aliases": "3D高斯点云渲染", "notes": "利用数百万显式三维各向异性高斯椭球实现实时辐射场重建与光栅化渲染的技术", "match": r"\bgaussian splatting\b|\b3dgs\b"},
    {"en": "Sim-to-Real Transfer", "zh": "仿真到现实迁移", "aliases": "虚实迁移", "notes": "克服物理仿真器与真实世界动力学及传感器域差以部署机器人控制策略的技术", "match": r"\bsim-to-real\b"},
    {"en": "Action Chunking", "zh": "动作分块预测", "aliases": "多步动作序列预测", "notes": "单次推理联合输出未来短窗口连续控制序列以缓解复合误差与高频控制延迟的策略机制", "match": r"\baction chunking\b|\bchunked control\b|\bchunking\b"},
    {"en": "Physical Agency", "zh": "物理主体性", "aliases": "物理环境自主执行力", "notes": "智能系统在三维物理世界中融合感知、空间记忆、规划与动作闭环达成物理目标的综合能力", "match": r"\bphysical agency\b"},
    {"en": "Retrieval-Augmented Generation (RAG)", "zh": "检索增强生成", "aliases": "外挂知识检索生成", "notes": "在生成前动态检索外部知识库并注入上下文以提升事实准确性与时效性的架构", "match": r"\bretrieval-augmented generation\b|\brag\b"},
    {"en": "Persistent Memory", "zh": "持久记忆机制", "aliases": "跨会话长程记忆", "notes": "突破有限上下文窗口、在长周期交互中压缩、存储与按需召回关键状态信息的记忆模块", "match": r"\bpersistent (?:content )?memory\b|\blong-term memory\b|\bepisodic memory\b"},
    {"en": "Continual Learning", "zh": "持续学习", "aliases": "终身学习、增量学习", "notes": "模型在不断吸收新任务与新知识的同时避免灾难性遗忘历史能力的机制", "match": r"\bcontinual learning\b"},
    {"en": "Machine Unlearning", "zh": "机器遗忘", "aliases": "模型定向知识擦除", "notes": "从已训练模型中精准移除特定隐私、版权或危险知识而不损害通用能力的技术", "match": r"\bunlearning\b"},
    {"en": "Jailbreak Attack", "zh": "越狱攻击", "aliases": "安全护栏绕过攻击", "notes": "通过精心构造对抗提示词诱导对齐模型输出违规或受限内容的红队测试手段", "match": r"\bjailbreak\b"},
    {"en": "Red Teaming", "zh": "红队测试", "aliases": "对抗性安全评测", "notes": "系统性探测模型安全边界、潜在偏见、越狱漏洞与代理失控风险的主动攻击评估", "match": r"\bred[- ]teaming\b"},
    {"en": "Hallucination", "zh": "模型幻觉", "aliases": "事实性编造", "notes": "生成式模型输出看似流畅自洽但违背客观事实或偏离输入证据的现象", "match": r"\bhallucinations?\b"},
    {"en": "Alignment Entropy", "zh": "对齐熵增", "aliases": "多智能体安全衰减", "notes": "自演化或多智能体交互系统在缺乏外部锚定时安全约束随迭代自然退化的现象", "match": r"\balignment entropy\b|\bsafety decay\b"},
    {"en": "CoT Monitorability", "zh": "思维链可监控性", "aliases": "推理过程忠实度审计", "notes": "通过审查模型中间思维链日志来检测隐蔽意图、欺骗行为或奖励黑客的可审计性质", "match": r"\bmonitorability\b|\bchains? of thought\b.*\bcontrol\b"},
    {"en": "Mechanistic Interpretability", "zh": "机制可解释性", "aliases": "电路级机理可解释性", "notes": "逆向工程神经网络内部特征表征、注意力头与计算电路以理解模型因果机制的研究方向", "match": r"\bmechanistic interpretability\b"},
    {"en": "Sparse Autoencoder (SAE)", "zh": "稀疏自编码器", "aliases": "过完备稀疏字典学习", "notes": "将神经网络多义叠加激活解耦为单义可解释特征方向的无监督探针工具", "match": r"\bsparse autoencoders?\b|\bsaes?\b"},
    {"en": "Out-of-Distribution (OOD) Generalization", "zh": "分布外泛化", "aliases": "跨域泛化能力", "notes": "模型在显著偏离训练数据分布的新场景、新形态或新规则下保持有效推理与控制的能力", "match": r"\bout-of-distribution\b|\bood\b"},
    {"en": "Scaling Law", "zh": "尺度定律", "aliases": "缩放定律、规模法则", "notes": "刻画模型损失或能力随参数量、数据规模及预训练/推理算力呈幂律变化的定量规律", "match": r"\bscaling laws?\b"},
    {"en": "In-Context Learning (ICL)", "zh": "上下文学习", "aliases": "少样本提示学习", "notes": "无需更新模型权重、仅凭上下文输入中的示例或指令即时适配新任务的涌现机制", "match": r"\bin-context learning\b|\bicl\b"},
    {"en": "Zero-Shot Generalization", "zh": "零样本泛化", "aliases": "零样本迁移", "notes": "在未见过目标任务任何训练样本的情况下直接完成任务指令或真机控制的能力", "match": r"\bzero-shot\b"},
    {"en": "Pareto Frontier", "zh": "帕累托前沿", "aliases": "性能-成本最优边界", "notes": "在准确率与算力开销、延迟或参数规模等多目标权衡中无法单向改进的最优解集合", "match": r"\bpareto\b"},
    {"en": "Contamination-Free Benchmark", "zh": "无数据污染基准", "aliases": "防泄漏动态评测集", "notes": "通过动态更新题目、私有化测试集或程序化生成防止预训练语料刷榜的评测体系", "match": r"\bcontamination\b|\bleakage-free\b"},
]

_COMPILED_GLOSSARY = [(g, re.compile(g["match"], re.I)) for g in GLOSSARY_TERMS]
_ACRONYM_DEF_RE = re.compile(r"\b([A-Z][A-Za-z0-9-]*(?:\s+[A-Za-z0-9-]+){1,5})\s*\(([A-Z][A-Z0-9-]{1,8})\)")


def detect_paper_type(title: str, abstract: str) -> dict:
    """Classify the methodological genre of a paper."""
    t_low = title.lower()
    a_low = abstract.lower()
    if re.search(r"\b(survey|comprehensive review|systematic review|taxonomy|roadmap|landscape of)\b", t_low) or re.search(
        r"\bthis paper presents a (?:systematic |comprehensive )?survey\b", a_low
    ):
        return {"code": "survey", "zh": "综述与体系调研", "en": "Survey & Taxonomy"}
    if re.search(r"\b(benchmark|benchmarking|leaderboard|evaluation suite|dataset for evaluating|testbed)\b", t_low) or re.search(
        r"\bwe introduce [A-Za-z0-9_-]+, a (?:new |comprehensive |holistic )?benchmark\b", a_low
    ):
        return {"code": "benchmark", "zh": "评测基准与数据集", "en": "Benchmark & Dataset"}
    if re.search(r"\b(technical report|foundation models? family|open foundation)\b", t_low):
        return {"code": "report", "zh": "基座模型技术报告", "en": "Technical Report"}
    if re.search(r"\b(do |does |can |is |why |when |how far|mirage|illusion|demystifying|towards understanding|empirical study)\b", t_low):
        return {"code": "analysis", "zh": "实证与机理剖析", "en": "Empirical & Mechanistic Study"}
    if re.search(r"\b(framework|system|engine|library|toolkit|harness|compiler|serving)\b", t_low):
        return {"code": "system", "zh": "系统与工程框架", "en": "System & Framework"}
    return {"code": "method", "zh": "算法与架构创新", "en": "Methodological Innovation"}


def classify_paper(paper: dict) -> dict:
    """
    Assign primary domain, multi-label domains, fine-grained subtopics,
    paper genre, and matched bilingual technical terms.
    """
    title = paper.get("title", "") or ""
    abstract = paper.get("abstract", "") or ""
    full_text = f"{title} {abstract}"

    scores: dict[str, float] = {}
    for dom_id, rx in _COMPILED_DOMAINS.items():
        t_hits = len(rx.findall(title))
        a_hits = len(rx.findall(abstract))
        score = t_hits * 3.0 + a_hits * 1.0
        if score > 0:
            scores[dom_id] = score

    if not scores:
        primary_domain = "Science_Eval"
        domains = ["Science_Eval"]
    else:
        ordered = sorted(scores.items(), key=lambda kv: (-kv[1], list(DOMAINS.keys()).index(kv[0])))
        primary_domain = ordered[0][0]
        top_score = ordered[0][1]
        domains = [k for k, v in ordered if v >= max(1.0, top_score * 0.3)][:4]

    matched_subtopics = []
    for sub, rx in _COMPILED_SUBTOPICS:
        if rx.search(full_text):
            matched_subtopics.append(sub["id"])

    matched_terms = []
    for g, rx in _COMPILED_GLOSSARY:
        if rx.search(full_text):
            matched_terms.append({"zh": g["zh"], "en": g["en"]})
            if len(matched_terms) >= 6:
                break

    custom_defs = []
    seen_acro = set()
    lead_noise = re.compile(
        r"^(?:(?:We|Our|This|To|In|By|With|Through|Furthermore|Moreover|Finally)\s+)?"
        r"(?:(?:further|also|first|then|here)\s+)?"
        r"(?:(?:propose|present|introduce|develop|formulate|design|use|leverage|adopt)\s+)?"
        r"(?:(?:a|an|the|novel|new)\s+)?",
        re.I,
    )
    for m in _ACRONYM_DEF_RE.finditer(abstract):
        full_name = lead_noise.sub("", m.group(1).strip()).strip()
        acro = m.group(2).strip()
        if (
            full_name
            and len(full_name) >= 4
            and acro not in seen_acro
            and acro not in {"LLM", "LLMs", "VLM", "VLMs", "MLLM", "AI", "NLP", "RL", "SFT", "GPU", "API"}
        ):
            seen_acro.add(acro)
            custom_defs.append(f"{full_name} ({acro})")
            if len(custom_defs) >= 3:
                break

    ptype = detect_paper_type(title, abstract)
    return {
        "primary_domain": primary_domain,
        "primary_domain_zh": DOMAINS[primary_domain]["zh_short"],
        "primary_domain_en": DOMAINS[primary_domain]["en_short"],
        "domains": domains,
        "subtopics": matched_subtopics[:5],
        "paper_type": ptype,
        "matched_terms": matched_terms,
        "custom_defs": custom_defs,
    }
