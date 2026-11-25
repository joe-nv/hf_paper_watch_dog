# 附录 A 定量分类学、质量守恒桑基流向模型与活体教材自动化构建规范

## A.1 数据源与去重统计口径

本教材及配套逐篇精读库（`summaries/`）的全部统计指标均严格派生自仓库 `papers/YYYY/MM/YYYY-MM-DD.json` 归档文件：

- **日度切片统计（Archive-Entry Basis）**：在计算年度/季度论文产出总量、社区点赞均值（Mean Upvotes）、代码仓库开源率（GitHub Release Rate）及领域季度渗透率时，以每日归档条目为统计单元，忠实反映社区每日技术议程的密度变化。
- **全局唯一去重（Unique ArXiv Basis）**：对于跨日重复上榜的极少数论文（约占总条目 <0.1%），在生成全库百篇最高影响力里程碑榜单（附录 B）与近期前沿滚动雷达时，严格按 `arxiv_id` 唯一去重并保留最高社区热度记录。

---

## A.2 十维主领域与 31 子方向双层分类学（Two-Tier Taxonomy）

分类引擎（`scripts/taxonomy.py`）采用标题三倍加权匹配（$w_{\text{title}} = 3.0$）与摘要全文匹配（$w_{\text{abstract}} = 1.0$）相结合的确定性规则体系，为每篇论文同时赋予：

1. **唯一主研究领域（Primary Domain）**：得分最高的核心赛道，用于计算各季度/各年度严格和为 100% 的主领域结构份额（如第 1 章图 1.4 堆叠面积流图及图 3.1 / 图 5.1 断代转移图）。
2. **跨领域多标签集合（Multi-Domain Tags，最多保留前 4 个显著耦合域）**：凡得分达到主领域得分 30% 且不少于 1 次精确命中的交叉赛道均予保留，真实刻画诸如“具身 VLA + 强化学习 + 多模态”或“代码智能体 + 安全漏洞基准”的跨学科本质。
3. **31 个微观技术子方向（Fine-Grained Subtopics）**：精确锚定具体方法簇（如 `rlvr_grpo`、`ssm_linear`、`dlm_non_ar`、`harness_skills`、`rsi_self_evol`、`vla_policy` 等），支撑第 1 章图 1.5 的 24×15 速度热力图及第 6–14 章的子方向演化曲线。

---

## A.3 跨年度桑基流向图（Sankey Diagram）的质量守恒 Sinkhorn 配平模型

在第 1 章图 1.2、图 3.1 与图 5.1 的跨年度桑基图中，设第 $t$ 年与第 $t+1$ 年十大领域的归一化注意力分布向量分别为 $\mathbf{p}^{(t)}, \mathbf{p}^{(t+1)} \in \Delta^{9}$（满足 $\sum_i p^{(t)}_i = \sum_j p^{(t+1)}_j = 100\%$）。为了求解从第 $t$ 年领域 $i$ 流向第 $t+1$ 年领域 $j$ 的转移流量矩阵 $\mathbf{T}^{(t \to t+1)} = [T_{ij}]$，我们构建经验亲和度先验矩阵 $\mathbf{A}^{(t \to t+1)}$：

$$A_{ij} = \begin{cases} \gamma_{\text{self}}, & \text{if } i = j \\ \max\!\left(\epsilon,\; \dfrac{C^{(t+1)}_{ij}}{C^{(t+1)}_{ii}} \cdot g\!\left(p^{(t+1)}_j - p^{(t)}_j\right)\right), & \text{if } i \neq j \end{cases}$$

其中 $C^{(t+1)}_{ij}$ 为第 $t+1$ 年同时命中领域 $i$ 与领域 $j$ 的实证论文共现频数，$\gamma_{\text{self}}$ 表征学科主干延续惯性，$g(\cdot)$ 为对净扩容赛道的正向上游吸引增益。随后对先验矩阵 $\mathbf{A}$ 执行交替行归一化与列归一化的 **Sinkhorn-Knopp 双随机比例拟合迭代**，直至严格满足边缘质量守恒约束：

$$\sum_{j=1}^{10} T_{ij} = p^{(t)}_i \quad (\forall i), \qquad \sum_{i=1}^{10} T_{ij} = p^{(t+1)}_j \quad (\forall j)$$

由此渲染出的三次贝塞尔（Cubic Bézier）矢量流带既严格忠实于每年真实的领域占比高度，又由真实跨领域论文共现强度决定了交叉合流与分流的拓扑结构。

---

## A.4 每日自动增量更新与 PDF 编译流水线

仓库提供一键式幂等编排入口 `scripts/update_all.py`，并已集成至 `.github/workflows/daily_papers.yml`：

1. **抓取归档**：`scripts/fetch_papers.py` 拉取当日 Hugging Face Daily Papers 存入 `papers/YYYY/MM/`；
2. **逐篇四维精读**：`scripts/summarize_papers.py --skip-existing` 增量解析新增日期的每篇论文，输出中文为主、保留关键英文术语的 `观点 / 实验 / 结论 / Takeaway` 至 `summaries/YYYY/MM/` 并刷新全局索引；
3. **重算统计与矢量制图**：`scripts/generate_figures.py` 扫描全量归档生成 `chronicle/stats_snapshot.json` 并重新渲染 `chronicle/figures/` 下全部 12 幅纯矢量 SVG 图表；
4. **同步活体章节与编译精装教材 PDF**：`scripts/build_chronicle.py` 自动更新各章 `AUTO-SYNC` 数据表、近期前沿雷达与百篇里程碑全集，将 `chronicle/chapters/*.md` 转换为 Typst 学术出版源码并调用 `typst` 引擎一键合并编译为带完整目录书签、奇偶页眉页脚、教学专栏框与高清矢量插图的 `chronicle/AI_Research_Chronicle_Textbook.pdf`。
