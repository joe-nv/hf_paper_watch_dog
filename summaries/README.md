# HuggingFace Daily Papers 逐篇结构化精读库 (`summaries/`)

本目录与仓库 [`papers/`](../papers/) 按 `YYYY/MM/YYYY-MM-DD.{md,json}` 一一镜像，为收录的全部 **18,137 篇论文（共 920 个归档日，覆盖 `2023-05-04` 至 `2026-11-24`）** 提供统一四维结构化中文（保留关键英文专业术语）总结：

1. **核心观点（观点 / Perspective & Thesis）**：赛道定位、针对的前沿痛点、提出的核心模型/框架与学术论点。
2. **方法与实验（实验 / Methodology & Experiments）**：算法/系统设计模块、评测基准（Benchmarks）、参数与数据规模、算力与真机配置。
3. **实验结论（结论 / Findings & Quantitative Results）**：严格提取自原文的定量提升指标、加速比、胜率与关键消融结论。
4. **核心启示（Takeaway）**：在技术演进坐标中的现实启发、适用场景与开源复现状态。

> 宏观编年史与跨年度桑基流向教材请参阅仓库独立教材目录：[`chronicle/`](../chronicle/)（含自动编译合并的欧美大学教材版式 PDF：[`chronicle/AI_Research_Chronicle_Textbook.pdf`](../chronicle/AI_Research_Chronicle_Textbook.pdf)）。

---

## 年度归档总览

| 年份 | 结构化精读论文数 | 目录入口 |
| :--- | ---: | :--- |
| `2023` | 1,609 篇 | [查看 2023 目录](./2023/) |
| `2024` | 3,421 篇 | [查看 2024 目录](./2024/) |
| `2025` | 6,466 篇 | [查看 2025 目录](./2025/) |
| `2026` | 6,641 篇 | [查看 2026 目录](./2026/) |
| **合计** | **18,137 篇** | **覆盖 920 天** |

---

## 主研究领域分布（Primary Domain Distribution）

| 研究领域 | 论文数量 | 占比 |
| :--- | ---: | ---: |
| **后训练、强化学习与数据工程** (`Training & RL`) | 2,459 篇 | 13.6% |
| **推理与测试时计算** (`Reasoning & TTC`) | 2,263 篇 | 12.5% |
| **自主智能体与软件工程** (`Agents & SWE`) | 2,460 篇 | 13.6% |
| **多模态理解与统一基座** (`Multimodal`) | 2,550 篇 | 14.1% |
| **模型效率、量化与系统优化** (`Efficiency & Sys`) | 847 篇 | 4.7% |
| **视觉生成、3D与世界模型** (`Vision & World`) | 2,742 篇 | 15.1% |
| **架构创新与序列建模** (`Architecture`) | 862 篇 | 4.8% |
| **安全对齐、可信与可解释性** (`Safety & Interp`) | 928 篇 | 5.1% |
| **具身智能与物理代理** (`Embodied & VLA`) | 832 篇 | 4.6% |
| **科学智能、记忆系统与评测生态** (`Science & Eval`) | 2,194 篇 | 12.1% |

---

## 自动增量更新

每日 GitHub Actions 拉取最新 Hugging Face Daily Papers 后，会自动调用 `python scripts/summarize_papers.py --skip-existing` 增量生成当日总结，并联动更新 `chronicle/` 编年史教材与全书 PDF。
