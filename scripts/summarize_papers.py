#!/usr/bin/env python3
"""
Generate structured per-paper Chinese (+ English technical term) summaries
covering Perspective (观点), Experiments (实验), Conclusions (结论), and Takeaway
for every daily paper archive under papers/YYYY/MM/YYYY-MM-DD.json.

Outputs mirror papers/ into summaries/YYYY/MM/YYYY-MM-DD.{md,json} plus summaries/index.json.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections import Counter
from pathlib import Path

try:
    from scripts.taxonomy import DOMAINS, SUBTOPICS, classify_paper
except ImportError:
    from taxonomy import DOMAINS, SUBTOPICS, classify_paper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

_SUBTOPIC_MAP = {s["id"]: s for s in SUBTOPICS}

_ABBREV_PROTECT = re.compile(r"\b(e\.g|i\.e|et al|vs|Fig|Tab|Eq|Sec|Dr|Prof|Mr|Ms|No|approx|cf)\.", re.I)

_BOTTLENECK_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"latency|inference overhead|computationally expensive|high computational cost|slow|repeated denoising", re.I), "推理延迟与高昂计算开销"),
    (re.compile(r"memory|kv[- ]cache|vram|limited memory|resource-constrained", re.I), "显存占用与端侧资源受限"),
    (re.compile(r"bounded attention|long-horizon|distant history|long context|long sequences?|long documents?", re.I), "长程上下文建模与远距历史记忆衰减"),
    (re.compile(r"data scarcity|annotation|human-labeled|extensive training data|man-powered", re.I), "高质量标注数据稀缺与规模成本瓶颈"),
    (re.compile(r"generalization|out-of-distribution|\bood\b|domain shift|morphological heterogeneity|cross-embodiment", re.I), "跨域/跨本体分布外泛化受限"),
    (re.compile(r"hallucination|factuality|unfaithful|inconsistency|consistency bug", re.I), "模型幻觉、事实失真与长程一致性退化"),
    (re.compile(r"handcrafted|manual|task-specific|heuristic|brittle", re.I), "对人工先验规则或定制化流水线的过度依赖"),
    (re.compile(r"credit assignment|sparse reward|reward hacking|unstable|collapse", re.I), "强化学习信用分配困难与训练不稳定性"),
    (re.compile(r"safety|jailbreak|adversarial|vulnerability|decepti|privacy|copyright", re.I), "安全对齐脆弱性、隐私版权与潜在失控风险"),
    (re.compile(r"remains unclear|under[- ]explored|poorly understood|lack of|limited benchmark", re.I), "系统性评测缺失与内在作用机理不明"),
]

_METHOD_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\btwo-stage\b|\bthree-stage\b|\bmulti-stage\b|\bstaged\b", re.I), "分阶段渐进式训练/建模流水线"),
    (re.compile(r"\btraining-free\b|\bzero-shot\b", re.I), "免训练（Training-Free）/零样本适配机制"),
    (re.compile(r"\breinforcement learning\b|\bgrpo\b|\brlvr\b|\bdpo\b|\bppo\b|policy optimization", re.I), "强化学习策略优化与奖励驱动对齐"),
    (re.compile(r"\bdistillation\b|\bteacher\b.*\bstudent\b", re.I), "师生知识蒸馏与能力迁移"),
    (re.compile(r"\bsynthetic\b|\bsynthesis\b|\bdata selection\b|\bcuration\b", re.I), "高质量合成数据构造与精选配比"),
    (re.compile(r"\bdiffusion\b|\bflow matching\b|\bdenoising\b", re.I), "迭代去噪生成/流匹配建模"),
    (re.compile(r"\bmamba\b|\brecurrent\b|\bstate space\b|\blinear attention\b", re.I), "线性复杂度递归状态/注意力融合架构"),
    (re.compile(r"\bmixture[- ]of[- ](?:experts|transformers|depths|flow)|\bmoe\b", re.I), "稀疏专家路由与解耦表征设计"),
    (re.compile(r"\bcuda\b|\bfused kernel|\bquantiz|\bpruning|\bspeculative", re.I), "底层算子融合、量化压缩与执行流加速"),
    (re.compile(r"\bagentic\b|\btool[- ]use\b|\bharness\b|\bplanner\b|\bexecutor\b", re.I), "感知-规划-工具执行闭环智能体架构"),
    (re.compile(r"\bmemory\b|\bretrieval\b|\brag\b", re.I), "动态记忆槽更新与检索增强机制"),
    (re.compile(r"\bcontrolled intervention|\bablation|\bsystematically compare|\bempircally", re.I), "受控干预消融与多范式系统对比"),
]

_KNOWN_BENCHMARKS = re.compile(
    r"\b(MMLU(?:-Pro)?|GSM8K|MATH(?:-500)?|AIME(?:\s*202[456])?|GPQA(?:-Diamond)?|HumanEval(?:\+)?|MBPP(?:\+)?|"
    r"SWE-bench(?:\s*Verified|\s*Lite)?|LiveCodeBench|ARC-AGI|BIG-Bench|HellaSwag|TruthfulQA|IFEval|"
    r"MMMU(?:-Pro)?|MathVista|DocVQA|ChartQA|Video-MME(?:-v2)?|MVBench|EgoSchema|ActivityNet|"
    r"ImageNet(?:-1K)?|MS-COCO|COCO|LAION|HumanML3D|HiPHI|BONES(?:\s*Seed)?|ShapeNet|Objaverse|"
    r"LIBERO|RoboCasa|RLBench|CALVIN|Meta-World|RoboLab-\d+|WorldLeague|DivDynBench|OmniCompass|"
    r"GAIA|WebArena|OSWorld|VisualWebArena|Mind2Web|Tau-bench|AgentBench|AlpacaEval|MT-Bench|Arena-Hard|"
    r"BABILong|FineWeb|The Pile|PerSeg)\b"
)

_EVAL_PROP_RE = re.compile(
    r"\b(?:evaluated\s+on|evaluations?\s+on|tested\s+on|experiments?\s+on|comparisons?\s+on|benchmark(?:ed)?\s+on)\s+"
    r"(?:retargeted\s+|the\s+)?([A-Z][A-Za-z0-9_-]{2,28}(?:-\d+(?:\.\d+)?)?)\b"
)

_STOP_PROPER = {
    "The", "This", "These", "Our", "We", "In", "On", "For", "With", "Beyond", "Among", "Unlike",
    "However", "While", "Despite", "Moreover", "Furthermore", "Finally", "Specifically", "First",
    "Second", "Third", "Table", "Figure", "Section", "Project", "GitHub", "Hugging", "ArXiv",
    "Large", "Language", "Models", "Model", "Vision", "Multimodal", "Reinforcement", "Learning",
    "Artificial", "Intelligence", "Transformer", "Transformers", "Diffusion", "Neural", "Networks",
}

_SCALE_RE = re.compile(
    r"\b(\d+(?:\.\d+)?\s*(?:B|M|K|T|billion|million|trillion)\s*(?:parameters?|tokens?|samples?|examples?|hours?|tasks?|benchmarks?|episodes?|models?|APIs?)|"
    r"\d+(?:,\d{3})+\s*(?:hours?|samples?|examples?|tokens?|tasks?|pairs?|APIs?)|"
    r"\b\d+(?:\.\d+)?B(?:-A\d+(?:\.\d+)?B)?\b|"
    r"\b(?:RTX\s*\d{4}|A100|H100|H200|B200|TPU\s*v\d+|Unitree\s*[A-Z0-9]+|single\s+GPU)\b)",
    re.I,
)

_METRIC_RE = re.compile(
    r"(?:from\s+\d+(?:\.\d+)?\s*(?:ms|s|GB|MB|%)?\s+to\s+\d+(?:\.\d+)?\s*(?:ms|s|GB|MB|%)|"
    r"[+-]?\d+(?:\.\d+)?\s*(?:%|percentage points|\bpp\b)|"
    r"\d+(?:\.\d+)?\s*(?:×|x\b|times)\s*(?:speedup|faster|less|more|larger|smaller|reduction|improvement)?|"
    r"\b\d+\s+of\s+(?:the\s+)?\d+\s+(?:zero-shot\s+)?(?:trials?|goals?|tasks?|episodes?)|"
    r"\d+(?:\.\d+)?/\d+)",
    re.I,
)


def clean_latex_text(text: str) -> str:
    """Normalize common LaTeX inline markup in arXiv abstracts."""
    t = text.replace(r"\%", "%").replace(r"\_", "_").replace(r"\&", "&")
    t = re.sub(r"(\d+(?:\.\d+)?)\s*\\?times\b", r"\1×", t)
    t = re.sub(r"\$([^$]{1,40})\$", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def split_sentences(text: str) -> list[str]:
    """Split scientific abstract into clean sentences."""
    cleaned = clean_latex_text(text)
    if not cleaned:
        return []
    protected = _ABBREV_PROTECT.sub(lambda m: m.group(0).replace(".", "<DOT>"), cleaned)
    raw_parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\"\'])", protected)
    return [p.replace("<DOT>", ".").strip() for p in raw_parts if p.strip()]


def extract_artifact_name(title: str, abstract: str) -> str:
    """Extract the primary proposed model, benchmark, or framework name."""
    if ":" in title:
        prefix = title.split(":", 1)[0].strip()
        if 1 <= len(prefix.split()) <= 6 and len(prefix) <= 48:
            return prefix
    words = title.split()
    if len(words) <= 4:
        return title
    m = re.search(
        r"\b(?:we\s+(?:present|introduce|propose|develop)|termed\s+as|called|named)\s+([A-Z][A-Za-z0-9._+-]{2,30}(?:\s+[0-9]+\.[0-9]+)?)",
        abstract,
    )
    if m and m.group(1) not in _STOP_PROPER and m.group(1).lower() not in {"block", "layer", "method", "model", "system", "framework"}:
        return m.group(1)
    return " ".join(words[: min(5, len(words))])


def load_funny_index_lookup(repo_root: Path) -> dict[str, dict]:
    """Load curated bilingual picks from funny_index/ indexed by arxiv_id."""
    lookup: dict[str, dict] = {}
    fi_dir = repo_root / "funny_index"
    if not fi_dir.exists():
        return lookup
    entry_re = re.compile(
        r"\*\*`\[([^\]]+)\]`\*\*.*?\*\*ArXiv\*\*:\s*\[([0-9.]+)\].*?"
        r"\*\*Skill:\s*\"([^\"]+)\"\s*/\s*技能名：「([^」]+)」\*\*.*?"
        r"\*\*CN\*\*:\s*(.+?)(?:\n\n---|\Z)",
        re.S,
    )
    for md_file in sorted(fi_dir.glob("**/picks.md")):
        content = md_file.read_text(encoding="utf-8")
        for m in entry_re.finditer(content):
            tag, aid, skill_en, skill_zh, cn_desc = m.groups()
            lookup[aid.strip()] = {
                "tag": tag.strip(),
                "skill_en": skill_en.strip(),
                "skill_zh": skill_zh.strip(),
                "cn_desc": re.sub(r"\s+", " ", cn_desc).strip(),
            }
    return lookup


def _truncate_clause(sent: str, max_len: int = 190) -> str:
    s = re.sub(r"https?://\S+", "", sent).strip(" ,;.")
    if len(s) <= max_len:
        return s
    cut = s[:max_len].rsplit(" ", 1)[0]
    return cut + "..."


def summarize_paper(paper: dict, date_str: str = "", curated_lookup: dict[str, dict] | None = None) -> dict:
    """
    Produce a structured Chinese-primary + English-technical-term summary for one paper:
    - perspective (核心观点)
    - experiments (方法与实验)
    - conclusions (结论与指标)
    - takeaway (核心启示)
    """
    title = clean_latex_text(paper.get("title", ""))
    abstract = clean_latex_text(paper.get("abstract", ""))
    arxiv_id = paper.get("arxiv_id", "")
    org = paper.get("organization", "") or ""
    upvotes = int(paper.get("upvotes", 0) or 0)
    github_repo = paper.get("github_repo", "") or ""
    project_page = paper.get("project_page", "") or ""

    tax = classify_paper(paper)
    sents = split_sentences(abstract)
    artifact = extract_artifact_name(title, abstract)

    # 1. Identify bottleneck, proposal, experiment, and result sentences
    bottlenecks = [label for rx, label in _BOTTLENECK_RULES if rx.search(abstract)]
    methods = [label for rx, label in _METHOD_RULES if rx.search(abstract)]

    proposal_sent = ""
    exp_sents: list[str] = []
    result_sents: list[str] = []
    bg_sent = sents[0] if sents else ""

    for s in sents:
        s_low = s.lower()
        if not proposal_sent and re.search(
            r"\b(we present|we propose|we introduce|in this paper|this paper|this study|we develop|we investigate|we hypothesize)\b",
            s_low,
        ):
            proposal_sent = s
        if re.search(
            r"\b(evaluat|experiment|benchmark|dataset|across \d+|we test|we compare|real-world|ablation|trials?|simulated)\b",
            s_low,
        ):
            exp_sents.append(s)
        if re.search(
            r"\b(achiev|outperform|surpass|reduc|improv|speedup|state-of-the-art|\bsota\b|accuracy|success rate|"
            r"demonstrate that|reveal that|indicate that|show that|find that|findings?:|\(1\))\b|\d+(?:\.\d+)?%",
            s_low,
        ):
            result_sents.append(s)

    if not proposal_sent and len(sents) >= 2:
        proposal_sent = sents[1]
    elif not proposal_sent and sents:
        proposal_sent = sents[0]

    # 2. Extract benchmarks, scales, and metrics faithfully from source text
    benchmarks: list[str] = []
    for m in _KNOWN_BENCHMARKS.finditer(f"{title} {abstract}"):
        val = m.group(1).strip()
        if val not in benchmarks:
            benchmarks.append(val)
    for m in _EVAL_PROP_RE.finditer(abstract):
        cand = m.group(1).strip(".,;:")
        if cand not in _STOP_PROPER and cand != artifact and not cand.isdigit() and cand not in benchmarks:
            benchmarks.append(cand)
        if len(benchmarks) >= 6:
            break

    scales: list[str] = []
    for m in _SCALE_RE.finditer(abstract):
        val = re.sub(r"\s+", " ", m.group(0).strip())
        if val not in scales:
            scales.append(val)
        if len(scales) >= 5:
            break

    metrics: list[str] = []
    for m in _METRIC_RE.finditer(abstract):
        val = re.sub(r"\s+", " ", m.group(0).strip(" ,;."))
        if val and val not in metrics and not re.fullmatch(r"202[0-9]/\d+", val):
            metrics.append(val)
        if len(metrics) >= 6:
            break

    term_pairs = [f"{t['zh']}（{t['en']}）" for t in tax["matched_terms"][:3]]
    custom_defs = tax["custom_defs"]
    subtopic_labels = [_SUBTOPIC_MAP[sid]["zh"] for sid in tax["subtopics"][:3] if sid in _SUBTOPIC_MAP]

    curated = (curated_lookup or {}).get(arxiv_id)

    # --- Build Field 1: 核心观点 (perspective) ---
    bottleneck_str = "、".join(bottlenecks[:2]) if bottlenecks else "现有方法在复杂场景下的性能与效率权衡"
    term_str = "、".join(term_pairs) if term_pairs else f"{tax['primary_domain_zh']}（{tax['primary_domain_en']}）"
    custom_str = f"，并引入 {', '.join(custom_defs)} 等关键机制" if custom_defs else ""
    thesis_anchor = _truncate_clause(proposal_sent or bg_sent, 175)

    perspective = (
        f"本研究聚焦于**{tax['primary_domain_zh']}**（{tax['primary_domain_en']}）赛道，属于{tax['paper_type']['zh']}。"
        f"针对当前领域面临的「{bottleneck_str}」痛点，作者围绕 **{artifact}** 展开攻关，核心切入概念涵盖{term_str}{custom_str}。"
        f"核心论点主张：{thesis_anchor}。"
    )
    if curated:
        perspective += f"（入选月度技术树 `[{curated['tag']}]` 技能「{curated['skill_zh']} / {curated['skill_en']}」）"

    # --- Build Field 2: 方法与实验 (experiments) ---
    method_str = "、".join(methods[:3]) if methods else "针对性模型架构设计与多维受控实验验证"
    bench_part = f"评测基准/数据集涵盖 **{', '.join(benchmarks[:5])}**" if benchmarks else "结合代表性公开任务与受控消融设置开展系统评测"
    scale_part = f"；实验规模与算力/平台配置涉及 **{', '.join(scales[:4])}**" if scales else ""
    exp_anchor = _truncate_clause(exp_sents[0], 165) if exp_sents else _truncate_clause(sents[min(2, len(sents) - 1)], 150) if sents else ""
    experiments = f"技术路线上采用{method_str}。{bench_part}{scale_part}。实验设计与验证细节：{exp_anchor}。"

    # --- Build Field 3: 实验结论 (conclusions) ---
    if curated:
        conclusions = f"{curated['cn_desc']}"
        if metrics:
            conclusions += f" 原文关键量化指标包括：**{', '.join(metrics[:5])}**。"
    else:
        metric_part = f"关键量化指标达到 **{', '.join(metrics[:5])}**；" if metrics else ""
        res_clause = _truncate_clause(result_sents[-1] if result_sents else (sents[-1] if sents else title), 185)
        if result_sents and len(result_sents) >= 2 and result_sents[0] != result_sents[-1]:
            res_clause = _truncate_clause(result_sents[0], 115) + "；" + _truncate_clause(result_sents[-1], 115)
        conclusions = f"实证分析表明：{metric_part}核心实验发现验证了所提方案的有效性与边界条件（{res_clause}）。"

    # --- Build Field 4: 核心启示 (takeaway) ---
    sub_str = "、".join(subtopic_labels[:2]) if subtopic_labels else tax["primary_domain_zh"]
    open_status = "已开源代码/模型仓库，具备直接复现与工程接入条件" if github_repo else ("提供项目主页与可视化案例参考" if project_page else "提供了清晰的算法/评测设计范式参考")
    impact_tier = "社区高关注度代表作" if upvotes >= 80 else ("具有代表性的前沿探索" if upvotes >= 25 else "细分方向的扎实推进")

    type_code = tax["paper_type"]["code"]
    if type_code == "benchmark":
        action_hint = f"可作为评估 **{sub_str}** 真实能力上限与诊断失分盲区的标准测试床"
    elif type_code == "survey":
        action_hint = f"系统梳理了 **{sub_str}** 的技术谱系与开放难题，适合作为切入该赛道的全局路线图"
    elif type_code == "analysis":
        action_hint = f"修正了对 **{sub_str}** 的经验性直觉假设，为后续算法改进指明了真正起作用的因果关键点"
    elif type_code == "system":
        action_hint = f"证明了系统级编排/底层执行优化在 **{sub_str}** 落地中的决定性收益"
    else:
        action_hint = f"为突破 **{sub_str}** 中的「{bottlenecks[0] if bottlenecks else '性能-开销瓶颈'}」提供了可迁移的建模配方"

    takeaway = f"作为{impact_tier}（HF {upvotes} 赞{f'，出自 {org}' if org else ''}），本工作{action_hint}；{open_status}。"

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "date": date_str,
        "organization": org,
        "upvotes": upvotes,
        "primary_domain": tax["primary_domain"],
        "primary_domain_zh": tax["primary_domain_zh"],
        "domains": tax["domains"],
        "subtopics": tax["subtopics"],
        "paper_type": tax["paper_type"]["zh"],
        "benchmarks": benchmarks[:6],
        "metrics": metrics[:6],
        "perspective": perspective,
        "experiments": experiments,
        "conclusions": conclusions,
        "takeaway": takeaway,
        "github_repo": github_repo,
        "hf_url": paper.get("hf_url", ""),
        "arxiv_url": paper.get("arxiv_url", ""),
    }


def render_daily_summary_md(date_str: str, summaries: list[dict], rel_paper_md: str) -> str:
    """Render one day's structured paper summaries into readable Markdown."""
    domain_counts = Counter(s["primary_domain_zh"] for s in summaries)
    top_domains_str = " · ".join(f"{k} ({v})" for k, v in domain_counts.most_common(5))

    lines = [
        f"# 每日论文结构化精读 - {date_str}",
        "",
        f"> **原始归档**: [{rel_paper_md}](../../../{rel_paper_md}) | **收录篇数**: {len(summaries)} 篇 | **当日热点分布**: {top_domains_str}",
        "",
        "---",
        "",
    ]

    for idx, s in enumerate(summaries, 1):
        dom_badges = " / ".join(f"`{DOMAINS[d]['zh_short']}`" for d in s["domains"] if d in DOMAINS)
        org_part = f" | **机构**: {s['organization']}" if s["organization"] else ""
        repo_part = f" | **[GitHub]({s['github_repo']})**" if s["github_repo"] else ""

        lines.extend(
            [
                f"## {idx}. [{s['title']}]({s['hf_url']})",
                "",
                f"- **ArXiv**: [{s['arxiv_id']}]({s['arxiv_url']}){org_part} | **Upvotes**: `{s['upvotes']}` | **类型**: `{s['paper_type']}` | **领域**: {dom_badges}{repo_part}",
                f"- **核心观点（观点）**: {s['perspective']}",
                f"- **方法与实验（实验）**: {s['experiments']}",
                f"- **实验结论（结论）**: {s['conclusions']}",
                f"- **核心启示（Takeaway）**: {s['takeaway']}",
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def summarize_date_file(
    paper_json_path: Path,
    summaries_base_dir: Path,
    curated_lookup: dict[str, dict] | None = None,
) -> dict:
    """Summarize all papers in a single daily JSON file and write .md + .json."""
    raw = json.loads(paper_json_path.read_text(encoding="utf-8"))
    date_str = raw["date"]
    year, month, _ = date_str.split("-")

    summaries = [
        summarize_paper(p, date_str=date_str, curated_lookup=curated_lookup)
        for p in raw.get("papers", [])
    ]

    out_dir = summaries_base_dir / year / month
    out_dir.mkdir(parents=True, exist_ok=True)

    rel_paper_md = f"papers/{year}/{month}/{date_str}.md"
    md_path = out_dir / f"{date_str}.md"
    json_path = out_dir / f"{date_str}.json"

    md_path.write_text(render_daily_summary_md(date_str, summaries, rel_paper_md), encoding="utf-8")
    json_payload = {
        "date": date_str,
        "total": len(summaries),
        "source_paper_file": rel_paper_md,
        "summaries": summaries,
    }
    json_path.write_text(json.dumps(json_payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    return {"date": date_str, "count": len(summaries), "md_path": md_path, "json_path": json_path}


def build_summaries_readme_and_index(summaries_base_dir: Path) -> None:
    """Generate summaries/index.json and summaries/README.md across all summarized days."""
    json_files = sorted(summaries_base_dir.glob("*/*/*.json"))
    by_year = Counter()
    by_domain = Counter()
    total_papers = 0
    latest_date = ""
    earliest_date = ""

    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        dt = data["date"]
        if not earliest_date or dt < earliest_date:
            earliest_date = dt
        if dt > latest_date:
            latest_date = dt
        yr = dt[:4]
        n = data["total"]
        by_year[yr] += n
        total_papers += n
        for item in data["summaries"]:
            by_domain[item["primary_domain"]] += 1

    index_data = {
        "earliest_date": earliest_date,
        "latest_date": latest_date,
        "total_days": len(json_files),
        "total_papers": total_papers,
        "papers_by_year": dict(sorted(by_year.items())),
        "papers_by_primary_domain": {
            DOMAINS[k]["zh_short"]: by_domain[k] for k in DOMAINS if by_domain[k]
        },
    }
    (summaries_base_dir / "index.json").write_text(
        json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    year_rows = "\n".join(
        f"| `{yr}` | {cnt:,} 篇 | [查看 {yr} 目录](./{yr}/) |"
        for yr, cnt in sorted(by_year.items())
    )
    dom_rows = "\n".join(
        f"| **{DOMAINS[k]['zh']}** (`{DOMAINS[k]['en_short']}`) | {by_domain[k]:,} 篇 | {by_domain[k] / max(1, total_papers) * 100:.1f}% |"
        for k in DOMAINS
    )

    readme = f"""# HuggingFace Daily Papers 逐篇结构化精读库 (`summaries/`)

本目录与仓库 [`papers/`](../papers/) 按 `YYYY/MM/YYYY-MM-DD.{{md,json}}` 一一镜像，为收录的全部 **{total_papers:,} 篇论文（共 {len(json_files)} 个归档日，覆盖 `{earliest_date}` 至 `{latest_date}`）** 提供统一四维结构化中文（保留关键英文专业术语）总结：

1. **核心观点（观点 / Perspective & Thesis）**：赛道定位、针对的前沿痛点、提出的核心模型/框架与学术论点。
2. **方法与实验（实验 / Methodology & Experiments）**：算法/系统设计模块、评测基准（Benchmarks）、参数与数据规模、算力与真机配置。
3. **实验结论（结论 / Findings & Quantitative Results）**：严格提取自原文的定量提升指标、加速比、胜率与关键消融结论。
4. **核心启示（Takeaway）**：在技术演进坐标中的现实启发、适用场景与开源复现状态。

> 宏观编年史与跨年度桑基流向教材请参阅仓库独立教材目录：[`chronicle/`](../chronicle/)（含自动编译合并的欧美大学教材版式 PDF：[`chronicle/AI_Research_Chronicle_Textbook.pdf`](../chronicle/AI_Research_Chronicle_Textbook.pdf)）。

---

## 年度归档总览

| 年份 | 结构化精读论文数 | 目录入口 |
| :--- | ---: | :--- |
{year_rows}
| **合计** | **{total_papers:,} 篇** | **覆盖 {len(json_files)} 天** |

---

## 主研究领域分布（Primary Domain Distribution）

| 研究领域 | 论文数量 | 占比 |
| :--- | ---: | ---: |
{dom_rows}

---

## 自动增量更新

每日 GitHub Actions 拉取最新 Hugging Face Daily Papers 后，会自动调用 `python scripts/summarize_papers.py --skip-existing` 增量生成当日总结，并联动更新 `chronicle/` 编年史教材与全书 PDF。
"""
    (summaries_base_dir / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate structured per-paper summaries for papers/")
    parser.add_argument("date", nargs="?", default=None, help="Optional single date YYYY-MM-DD")
    parser.add_argument("--skip-existing", action="store_true", help="Only summarize dates missing in summaries/")
    parser.add_argument("--papers-dir", type=str, default=None)
    parser.add_argument("--summaries-dir", type=str, default=None)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    papers_dir = Path(args.papers_dir) if args.papers_dir else (repo_root / "papers")
    summaries_dir = Path(args.summaries_dir) if args.summaries_dir else (repo_root / "summaries")
    curated_lookup = load_funny_index_lookup(repo_root)

    if args.date:
        yr, mo, _ = args.date.split("-")
        targets = [papers_dir / yr / mo / f"{args.date}.json"]
    else:
        targets = sorted(papers_dir.glob("*/*/*.json"))

    processed = 0
    skipped = 0
    total_papers = 0
    for pf in targets:
        if not pf.exists():
            logger.warning("Paper file not found: %s", pf)
            continue
        date_str = pf.stem
        yr, mo, _ = date_str.split("-")
        out_md = summaries_dir / yr / mo / f"{date_str}.md"
        if args.skip_existing and out_md.exists():
            skipped += 1
            continue
        res = summarize_date_file(pf, summaries_dir, curated_lookup=curated_lookup)
        processed += 1
        total_papers += res["count"]

    summaries_dir.mkdir(parents=True, exist_ok=True)
    build_summaries_readme_and_index(summaries_dir)
    logger.info(
        "Summaries complete: %d days processed (%d papers), %d days skipped.",
        processed,
        total_papers,
        skipped,
    )


if __name__ == "__main__":
    main()
