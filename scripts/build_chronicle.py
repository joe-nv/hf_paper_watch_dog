#!/usr/bin/env python3
"""
Synchronize live cumulative statistics into chronicle/chapters/*.md, build
chronicle/README.md, convert all chapters + figures into Typst academic textbook
markup, and compile chronicle/AI_Research_Chronicle_Textbook.pdf.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

try:
    from scripts.generate_figures import compute_archive_analytics, generate_all_figures
    from scripts.taxonomy import DOMAINS, GLOSSARY_TERMS
except ImportError:
    from generate_figures import compute_archive_analytics, generate_all_figures
    from taxonomy import DOMAINS, GLOSSARY_TERMS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

CHAPTER_PLAN: list[dict] = [
    {
        "part": None,
        "badge": "PREFACE · 前言导读",
        "file": "ch00_preface_and_guide.md",
    },
    {
        "part": (
            "PART I",
            "宏观全景与热点流向图谱",
            "Macro Landscape, Empirical Scaling & Multi-Year Sankey Flows",
            "第一部分从全局定量视角出发，基于 2023–2026 全量日度论文归档构建跨年度桑基流向图（Sankey Diagrams）、15 季度结构面积流图与 24 子方向速度热力矩阵，揭示人工智能研究主航道四年来三次历史性改道的全貌。",
        ),
        "badge": "CHAPTER 01 · MACRO LANDSCAPE & SANKEY ATLAS",
        "file": "ch01_macro_landscape_sankey.md",
    },
    {
        "part": (
            "PART II",
            "年度演进编年史（2023–2026）",
            "Chronological History of Modern AI Research: Year by Year",
            "第二部分以断代史体例逐年复盘 2023 基座破冰与扩散黄金时代、2024 极低比特与早期全模态融合、2025 可验证强化学习与推理超级周期，以及 2026 智能体脚手架、递归自进化与具身物理主体元年，并内嵌自动更新的近期前沿动态雷达。",
        ),
        "badge": "CHAPTER 02 · ANNUAL CHRONICLE: 2023",
        "file": "ch02_chronicle_2023.md",
    },
    {"part": None, "badge": "CHAPTER 03 · ANNUAL CHRONICLE: 2024", "file": "ch03_chronicle_2024.md"},
    {"part": None, "badge": "CHAPTER 04 · ANNUAL CHRONICLE: 2025", "file": "ch04_chronicle_2025.md"},
    {"part": None, "badge": "CHAPTER 05 · ANNUAL CHRONICLE: 2026 & LIVE RADAR", "file": "ch05_chronicle_2026.md"},
    {
        "part": (
            "PART III",
            "十大核心技术范式纵向演进专论",
            "Vertical Evolution of Core AI Paradigms & Engineering Stacks",
            "第三部分打破时间横截面限制，按大学高阶专业课结构纵向剖析序列建模架构、后训练与强化学习、测试时计算推理、低比特与系统效率、统一多模态基座、自主智能体与代码工程、世界模型与具身机器人、安全对齐与可解释性、科学智能与开源生态九大支柱。",
        ),
        "badge": "CHAPTER 06 · SEQUENCE ARCHITECTURE & BACKBONES",
        "file": "ch06_architecture_evolution.md",
    },
    {"part": None, "badge": "CHAPTER 07 · POST-TRAINING, RLVR & DATA CURATION", "file": "ch07_training_rl_data.md"},
    {"part": None, "badge": "CHAPTER 08 · REASONING & TEST-TIME COMPUTE", "file": "ch08_reasoning_test_time.md"},
    {"part": None, "badge": "CHAPTER 09 · EFFICIENCY, QUANTIZATION & SYSTEMS", "file": "ch09_efficiency_systems.md"},
    {"part": None, "badge": "CHAPTER 10 · MULTIMODAL & UNIFIED MODELS", "file": "ch10_multimodal_unified.md"},
    {"part": None, "badge": "CHAPTER 11 · AUTONOMOUS AGENTS, SKILLS & RSI", "file": "ch11_agents_coding_rsi.md"},
    {"part": None, "badge": "CHAPTER 12 · WORLD MODELS & EMBODIED PHYSICAL AI", "file": "ch12_vision_world_embodied.md"},
    {"part": None, "badge": "CHAPTER 13 · SAFETY, GUARDRAILS & INTERPRETABILITY", "file": "ch13_safety_interpretability.md"},
    {"part": None, "badge": "CHAPTER 14 · AI4SCIENCE, MEMORY & OPEN ECOSYSTEM", "file": "ch14_science_memory_open.md"},
    {
        "part": (
            "PART IV",
            "方法论规范、百篇里程碑全集与双向术语表",
            "Methodology, Compendium of 100 Landmark Papers & Bilingual Glossary",
            "第四部分提供支撑全书定量结论的双层分类学与质量守恒 Sinkhorn 桑基配平数学模型，完整收录全库历史热度最高的 100 篇里程碑论文结构化四维提要（观点、实验、结论、Takeaway），并附双向术语一致性对照标准。",
        ),
        "badge": "APPENDIX A · QUANTITATIVE METHODOLOGY",
        "file": "appA_methodology_taxonomy.md",
    },
    {"part": None, "badge": "APPENDIX B · TOP 100 LANDMARK COMPENDIUM", "file": "appB_landmark_compendium.md"},
    {"part": None, "badge": "APPENDIX C · BILINGUAL TECHNICAL GLOSSARY", "file": "appC_bilingual_glossary.md"},
]


def load_summary_by_date_and_id(summaries_dir: Path, date_str: str, arxiv_id: str) -> dict | None:
    yr, mo, _ = date_str.split("-")
    jf = summaries_dir / yr / mo / f"{date_str}.json"
    if not jf.exists():
        return None
    data = json.loads(jf.read_text(encoding="utf-8"))
    for s in data.get("summaries", []):
        if s.get("arxiv_id") == arxiv_id:
            return s
    return None


def _build_sync_payloads(stats: dict, summaries_dir: Path) -> dict[str, str]:
    """Build Markdown blocks for all <!-- AUTO-SYNC:START:... --> anchors."""
    payloads: dict[str, str] = {}
    years = sorted(stats["years"].keys())

    # 1. Macro overview table
    macro_lines = [
        "### 表 1.1 2023–2026 年度宏观规模与核心领域主份额演进总表（实时同步自归档库）",
        "",
        "| 年份 | 归档论文数 | 平均热度 (Upvotes) | 代码开源率 (GitHub) | 年度第一大主赛道 | 年度最高热度代表作 |",
        "| :--- | ---: | ---: | ---: | :--- | :--- |",
    ]
    for yr in years:
        yd = stats["years"][yr]
        top_dom = max(yd["primary_domain"].items(), key=lambda kv: kv[1])[0]
        top_dom_pct = yd["primary_domain"][top_dom] / max(1, yd["total"]) * 100.0
        tp = yd["top_papers"][0]
        short_t = tp["title"] if len(tp["title"]) <= 44 else tp["title"][:42] + "..."
        macro_lines.append(
            f"| **{yr}** | {yd['total']:,} 篇 | {yd['avg_upvotes']:.2f} | {yd['github_rate']:.1f}% | "
            f"{DOMAINS[top_dom]['zh_short']} ({top_dom_pct:.1f}%) | [{short_t}]({tp['hf_url']}) (`{tp['upvotes']}` 赞) |"
        )
    overall_gh = sum(stats["years"][yr]["total"] * stats["years"][yr]["github_rate"] for yr in years) / max(1, stats["total_papers"])
    overall_upv = sum(stats["years"][yr]["total"] * stats["years"][yr]["avg_upvotes"] for yr in years) / max(1, stats["total_papers"])
    macro_lines.append(
        f"| **全周期累计** | **{stats['total_papers']:,} 篇** | **{overall_upv:.2f}** | **{overall_gh:.1f}%** | "
        f"跨代演进（共 {stats['total_days']} 天） | 去重唯一 ArXiv：{stats['unique_papers']:,} 篇 |"
    )
    yr_hdrs = " | ".join(f"{yr} 主域 (多标签%)" for yr in years)
    yr_align = " | ".join("---:" for _ in years)
    macro_lines.extend(
        [
            "",
            "### 表 1.2 十大核心赛道跨年度主领域论文数与多标签渗透率对照矩阵",
            "",
            f"| 核心研究赛道 | {yr_hdrs} | 跨期演进态势 |",
            f"| :--- | {yr_align} | :--- |",
        ]
    )
    for d, meta in DOMAINS.items():
        cells = []
        pcts = []
        for yr in years:
            yd = stats["years"][yr]
            p_cnt = yd["primary_domain"].get(d, 0)
            m_pct = yd["multi_domain"].get(d, 0) / max(1, yd["total"]) * 100.0
            pcts.append(p_cnt / max(1, yd["total"]) * 100.0)
            cells.append(f"{p_cnt:,} ({m_pct:.1f}%)")
        diff = pcts[-1] - pcts[0]
        trend = "强劲跃升 ↑↑" if diff >= 4.0 else ("稳步扩容 ↑" if diff >= 1.0 else ("高位稳态 →" if diff > -2.5 else "沉淀分流 ↓"))
        macro_lines.append(f"| **{meta['zh_short']}** | {' | '.join(cells)} | {trend} (`{diff:+.1f}pp`) |")
    payloads["macro_overview_table"] = "\n".join(macro_lines)

    # 2. Annual tables (2023..present)
    for yr in years:
        yd = stats["years"][yr]
        qs_yr = [q for q in stats["quarters"] if q.startswith(yr)]
        q_summary = " · ".join(f"`{q}`: {stats['quarters'][q]['total']:,} 篇" for q in qs_yr)
        lines = [
            f"### 表 {max(2, int(yr) - 2021)}.1 {yr} 年度归档核心统计与 Top 12 社区最高影响力论文榜",
            "",
            f"- **年度收录总量**：**{yd['total']:,} 篇**（季度分布：{q_summary}）",
            f"- **平均社区热度**：**{yd['avg_upvotes']:.2f} Upvotes** ｜ **代码仓库开源率**：**{yd['github_rate']:.1f}%**",
            "",
            "| 排名 | 日期 | ArXiv ID | 论文标题 | 机构 | 主领域 | Upvotes |",
            "| ---: | :--- | :--- | :--- | :--- | :--- | ---: |",
        ]
        for idx, tp in enumerate(yd["top_papers"][:12], 1):
            t_disp = tp["title"].replace("|", "\\|")
            if len(t_disp) > 58:
                t_disp = t_disp[:56] + "..."
            org_disp = (tp["organization"] or "—").replace("|", "\\|")
            if len(org_disp) > 22:
                org_disp = org_disp[:20] + ".."
            lines.append(
                f"| {idx} | `{tp['date']}` | [{tp['arxiv_id']}]({tp['arxiv_url']}) | [{t_disp}]({tp['hf_url']}) | "
                f"{org_disp} | {DOMAINS[tp['primary_domain']]['zh_short']} | **{tp['upvotes']}** |"
            )
        payloads[f"year_{yr}_table"] = "\n".join(lines)

    # 3. Recent 30-day frontier radar (live updated on every daily run!)
    rw = stats["recent_window"]
    radar_lines = [
        f"> **最新归档滚动窗口**：`{rw['from']}` 至 `{rw['to']}` ｜ 自动筛选近期最高社区关注度 Top 12 代表作",
        "",
        "| 日期 | ArXiv | 标题与核心切入点 | 机构 | 赛道 | 热度 |",
        "| :--- | :--- | :--- | :--- | :--- | ---: |",
    ]
    for rp in stats["recent_frontier_papers"][:12]:
        t_disp = rp["title"].replace("|", "\\|")
        if len(t_disp) > 54:
            t_disp = t_disp[:52] + "..."
        org_disp = (rp["organization"] or "—").replace("|", "\\|")
        if len(org_disp) > 20:
            org_disp = org_disp[:18] + ".."
        radar_lines.append(
            f"| `{rp['date']}` | [{rp['arxiv_id']}]({rp['arxiv_url']}) | [{t_disp}]({rp['hf_url']}) | "
            f"{org_disp} | {DOMAINS[rp['primary_domain']]['zh_short']} | **{rp['upvotes']}** |"
        )
    payloads["recent_frontier_radar"] = "\n".join(radar_lines)

    # 4. Per-domain longitudinal tables for Chapters 6–14
    all_top_pool = stats["top_100_landmark_papers"]
    yr_cols_hdr = " | ".join(years)
    yr_cols_sep = " | ".join("---:" for _ in years)
    for d, meta in DOMAINS.items():
        d_lines = [
            f"### 实证数据切片：{meta['zh']}（跨年度演化指标与代表作）",
            "",
            f"| 统计维度 | {yr_cols_hdr} | 全周期开源率 |",
            f"| :--- | {yr_cols_sep} | ---: |",
        ]
        p_row = [f"{stats['years'][yr]['primary_domain'].get(d, 0):,} 篇" for yr in years]
        m_row = [
            f"{stats['years'][yr]['multi_domain'].get(d, 0) / max(1, stats['years'][yr]['total']) * 100:.1f}%"
            for yr in years
        ]
        gh_rate = f"{stats['domain_open_source_rate'][d]:.1f}%"
        d_lines.append(f"| **主领域归档篇数** | {' | '.join(p_row)} | {gh_rate} |")
        d_lines.append(f"| **跨领域多标签渗透率** | {' | '.join(m_row)} | — |")

        dom_reps = [p for p in all_top_pool if d in p.get("domains", [])][:6]
        if dom_reps:
            d_lines.extend(
                [
                    "",
                    "| 年份 | ArXiv | 本赛道高影响力里程碑论文 | 机构 | Upvotes |",
                    "| :--- | :--- | :--- | :--- | ---: |",
                ]
            )
            for dp in dom_reps:
                td = dp["title"].replace("|", "\\|")
                if len(td) > 62:
                    td = td[:60] + "..."
                od = (dp["organization"] or "—").replace("|", "\\|")[:22]
                d_lines.append(
                    f"| `{dp['date']}` | [{dp['arxiv_id']}]({dp['arxiv_url']}) | [{td}]({dp['hf_url']}) | {od} | **{dp['upvotes']}** |"
                )
        payloads[f"domain_stats_{d}"] = "\n".join(d_lines)

    # 5. Appendix B: Top 100 Landmark Compendium with 4-field structured summaries!
    top100_lines = []
    for rank, p in enumerate(stats["top_100_landmark_papers"], 1):
        s_rec = load_summary_by_date_and_id(summaries_dir, p["date"], p["arxiv_id"])
        org_txt = p["organization"] or "Community / Unaffiliated"
        dom_txt = " / ".join(DOMAINS[x]["zh_short"] for x in p.get("domains", []) if x in DOMAINS)
        top100_lines.append(f"### {rank}. [{p['title']}]({p['hf_url']})")
        top100_lines.append("")
        top100_lines.append(
            f"**ArXiv**: [{p['arxiv_id']}]({p['arxiv_url']}) ｜ **归档日期**: `{p['date']}` ｜ **机构**: {org_txt} ｜ **Upvotes**: `{p['upvotes']}` ｜ **领域**: {dom_txt}"
        )
        top100_lines.append("")
        if s_rec:
            top100_lines.append(f"- **核心观点**: {s_rec['perspective']}")
            top100_lines.append(f"- **方法与实验**: {s_rec['experiments']}")
            top100_lines.append(f"- **实验结论**: {s_rec['conclusions']}")
            top100_lines.append(f"- **Takeaway**: {s_rec['takeaway']}")
        top100_lines.append("")
    payloads["appendix_top100"] = "\n".join(top100_lines)

    # 6. Appendix C: 5-column Bilingual Technical Glossary
    gl_lines = [
        "| 方向 | 源语言术语 (English Term) | 目标语主译名 (锁定) | 常见别名 / 备选译法 | 语境与定名说明 |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for g in GLOSSARY_TERMS:
        gl_lines.append(
            f"| EN→ZH | `{g['en']}` | **{g['zh']}** | {g['aliases'] or '—'} | {g['notes']} |"
        )
    payloads["appendix_glossary"] = "\n".join(gl_lines)

    return payloads


def sync_markdown_chapters(chapters_dir: Path, payloads: dict[str, str]) -> None:
    """Inject live computed payloads into <!-- AUTO-SYNC:START:id --> blocks."""
    pattern = re.compile(r"(<!-- AUTO-SYNC:START:([a-zA-Z0-9_]+) -->)(.*?)(<!-- AUTO-SYNC:END:\2 -->)", re.S)
    for md_path in sorted(chapters_dir.glob("*.md")):
        orig = md_path.read_text(encoding="utf-8")

        def _repl(m: re.Match) -> str:
            key = m.group(2)
            if key not in payloads:
                return m.group(0)
            return f"{m.group(1)}\n\n{payloads[key]}\n\n{m.group(4)}"

        updated = pattern.sub(_repl, orig)
        if updated != orig:
            md_path.write_text(updated, encoding="utf-8")


# -------------------- Markdown -> Typst Compiler --------------------

def _typ_escape_plain(s: str) -> str:
    """Escape characters with syntactic meaning in Typst content mode."""
    out = []
    for ch in s:
        if ch in ("\\", "#", "*", "_", "`", "@", "<", ">", "$", "~", "[", "]"):
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


_INLINE_TOKEN_RE = re.compile(
    r"(`[^`]+`)"                                  # 1: inline code
    r"|(\$\$[^$]+\$\$)"                           # 2: display-like inline math
    r"|(\$(?!\d)(?!\s)[^$\n]{1,80}?(?<!\s)\$)"    # 3: inline math (excludes "$10 ... $20" currency)
    r"|(\*\*\[[^\]]+\]\([^)]+\)\*\*)"             # 4: bold link
    r"|(\[[^\]]+\]\([^)]+\))"                     # 5: markdown link
    r"|(\*\*[^*\n]+?\*\*)"                        # 6: bold
    r"|(\*[^*\s][^*\n]*?\*)"                      # 7: italic
)


def _convert_latex_math_to_typst(expr: str) -> str:
    """Convert lightweight inline LaTeX math notations used in our chapters to valid Typst math."""
    e = expr.strip()
    e = e.replace(r"\times", " times ")
    e = e.replace(r"\approx", " approx ")
    e = e.replace(r"\ge", " >= ").replace(r"\le", " <= ").replace(r"\neq", " != ")
    e = e.replace(r"\in", " in ").replace(r"\forall", " forall ").replace(r"\to", " -> ")
    e = e.replace(r"\sum", "sum").replace(r"\max", "max").replace(r"\log", "log").replace(r"\min", "min")
    e = e.replace(r"\Delta", "Delta").replace(r"\epsilon", "epsilon").replace(r"\gamma", "gamma")
    e = e.replace(r"\quad", " quad ").replace(r"\qquad", " wide ").replace(r"\cdot", " dot ")
    e = re.sub(r"\\text\{([^}]*)\}", lambda m: f'"{m.group(1)}"', e)
    e = re.sub(r"\\mathcal\{([A-Za-z])\}", r"cal(\1)", e)
    e = re.sub(r"\\mathbf\{([A-Za-z0-9]+)\}", r"bold(\1)", e)
    e = re.sub(r"\\dfrac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", e)
    e = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", e)
    e = e.replace(r"\!", " ").replace(r"\left", "").replace(r"\right", "").replace(";", ",")
    e = re.sub(r"_\{([^}]*)\}", r"_(\1)", e)
    e = re.sub(r"_\(([a-z])([a-z])\)", r"_(\1 \2)", e)
    e = re.sub(r"\^\{([^}]*)\}", r"^(\1)", e)
    return e


def md_inline_to_typst(text: str) -> str:
    """Convert Markdown inline formatting to valid Typst markup."""
    parts: list[str] = []
    pos = 0
    for m in _INLINE_TOKEN_RE.finditer(text):
        if m.start() > pos:
            parts.append(_typ_escape_plain(text[pos : m.start()]))
        tok = m.group(0)
        if m.group(1):  # `code`
            inner = tok[1:-1].replace("\\", "\\\\").replace('"', '\\"')
            parts.append(f'#raw("{inner}")')
        elif m.group(2) or m.group(3):  # math
            raw_m = tok.strip("$")
            # Simple fallback if complex cases environment
            if r"\begin{cases}" in raw_m:
                parts.append(_typ_escape_plain(raw_m))
            else:
                parts.append(f"${_convert_latex_math_to_typst(raw_m)}$")
        elif m.group(4):  # **[lbl](url)**
            inner = tok[2:-2]
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", inner)
            if lm:
                lbl, url = lm.group(1), lm.group(2)
                if url.startswith("http"):
                    url_esc = url.replace("\\", "\\\\").replace('"', '\\"')
                    parts.append(f'#strong[#link("{url_esc}")[{md_inline_to_typst(lbl)}]]')
                else:
                    parts.append(f"#strong[{md_inline_to_typst(lbl)}]")
        elif m.group(5):  # [lbl](url)
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)
            if lm:
                lbl, url = lm.group(1), lm.group(2)
                if url.startswith("http"):
                    url_esc = url.replace("\\", "\\\\").replace('"', '\\"')
                    parts.append(f'#link("{url_esc}")[{md_inline_to_typst(lbl)}]')
                else:
                    parts.append(md_inline_to_typst(lbl))
        elif m.group(6):  # **bold**
            parts.append(f"#strong[{md_inline_to_typst(tok[2:-2])}]")
        elif m.group(7):  # *italic*
            parts.append(f"#emph[{md_inline_to_typst(tok[1:-1])}]")
        pos = m.end()
    if pos < len(text):
        parts.append(_typ_escape_plain(text[pos:]))
    return "".join(parts)


def _split_md_table_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells = re.split(r"(?<!\\)\|", s)
    return [c.replace("\\|", "|").strip() for c in cells]


def _render_md_table_to_typst(table_lines: list[str]) -> str:
    if len(table_lines) < 2:
        return ""
    headers = _split_md_table_row(table_lines[0])
    align_spec = _split_md_table_row(table_lines[1])
    rows = [_split_md_table_row(ln) for ln in table_lines[2:] if ln.strip()]
    ncols = len(headers)

    aligns = []
    for a in align_spec[:ncols]:
        a = a.strip()
        if a.startswith(":") and a.endswith(":"):
            aligns.append("center")
        elif a.endswith(":"):
            aligns.append("right")
        else:
            aligns.append("left")
    while len(aligns) < ncols:
        aligns.append("left")

    # Smart column sizing: narrow columns get `auto`, text-heavy columns share `1fr`
    max_lens = [len(h) for h in headers]
    for r in rows:
        for idx in range(min(ncols, len(r))):
            clean_c = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", r[idx])
            max_lens[idx] = max(max_lens[idx], len(clean_c))

    col_specs = []
    for ml in max_lens:
        if ml <= 12:
            col_specs.append("auto")
        elif ml <= 24:
            col_specs.append("1.1fr")
        else:
            col_specs.append("2.1fr")

    out = [
        "#block(width: 100%, above: 10pt, below: 12pt, breakable: true)[",
        "  #set text(font: sans_fonts, size: 8.3pt)",
        f"  #table(",
        f"    columns: ({', '.join(col_specs)}),",
        f"    align: ({', '.join(aligns)}),",
        "    inset: (x: 6pt, y: 5.5pt),",
        "    stroke: (x, y) => if y == 0 { (bottom: 1.2pt + navy, top: 1.2pt + navy) } else { (bottom: 0.4pt + rgb(\"#CBD5E1\")) },",
        "    fill: (x, y) => if y == 0 { navy } else if calc.odd(y) { rgb(\"#FFFFFF\") } else { rgb(\"#F8FAFC\") },",
        "    table.header(",
    ]
    for h_cell in headers:
        out.append(f"      [#text(fill: white, weight: \"bold\")[{md_inline_to_typst(h_cell)}]],")
    out.append("    ),")
    for r in rows:
        padded = (r + [""] * ncols)[:ncols]
        for c in padded:
            out.append(f"    [{md_inline_to_typst(c)}],")
    out.append("  )")
    out.append("]")
    return "\n".join(out)


def markdown_chapter_to_typst(md_text: str, chap_badge: str) -> str:
    """Convert a full Markdown chapter into Typst textbook body."""
    # Remove HTML comments
    cleaned = re.sub(r"<!--.*?-->", "", md_text, flags=re.S)
    lines = cleaned.splitlines()

    out: list[str] = []
    i = 0
    n = len(lines)
    chapter_opened = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            out.append("")
            i += 1
            continue

        # Display math block $$ ... $$
        if stripped.startswith("$$"):
            math_buf = [stripped.lstrip("$").rstrip("$")]
            if not (stripped.endswith("$$") and len(stripped) > 4):
                i += 1
                while i < n and not lines[i].strip().endswith("$$"):
                    math_buf.append(lines[i].strip())
                    i += 1
                if i < n:
                    math_buf.append(lines[i].strip().rstrip("$"))
            raw_math = " ".join(x for x in math_buf if x).strip()
            if r"\begin{cases}" in raw_math:
                out.append(
                    '#block(width: 100%, fill: rgb("#F8FAFC"), inset: 10pt, radius: 3pt)['
                    '$ A_(i j) = cases(gamma_"self" quad &"if" i = j, max(epsilon, C^(t+1)_(i j) / C^(t+1)_(i i) dot g(p^(t+1)_j - p^(t)_j)) quad &"if" i != j) $]'
                )
            else:
                out.append(f"$ {_convert_latex_math_to_typst(raw_math)} $")
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"-{3,}", stripped):
            i += 1
            continue

        # Headings
        hm = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if hm:
            lvl = len(hm.group(1))
            htitle = hm.group(2).strip()
            if lvl == 1 and not chapter_opened:
                chapter_opened = True
                out.append(f"#chapter_start({json.dumps(chap_badge, ensure_ascii=False)}, [{md_inline_to_typst(htitle)}])")
            else:
                typ_lvl = min(4, lvl)
                out.append(f"{'=' * typ_lvl} {md_inline_to_typst(htitle)}")
            i += 1
            continue

        # Image: ![alt](path)
        im = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
        if im:
            cap, img_rel = im.group(1).strip(), im.group(2).strip()
            norm_path = "/" + img_rel.replace("../figures/", "figures/").lstrip("/")
            out.append(f'#textbook_figure("{norm_path}", [{md_inline_to_typst(cap)}])')
            i += 1
            continue

        # Blockquote / Callout box
        if stripped.startswith(">"):
            q_lines = []
            while i < n and lines[i].strip().startswith(">"):
                q_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            first_q = q_lines[0] if q_lines else ""
            rest_md = "\n".join(q_lines[1:]).strip()

            if "LEARNING OBJECTIVES" in first_q:
                body_typ = _convert_simple_blocks(rest_md)
                out.append(f"#learning_box[\n{body_typ}\n]")
            elif "KEY CONCEPT" in first_q:
                tm = re.search(r"\*\*\[KEY CONCEPT[^\]]*\]\*\*\s*(?:\*\*(.+?)\*\*)?", first_q)
                box_t = md_inline_to_typst(tm.group(1)) if (tm and tm.group(1)) else ""
                body_typ = _convert_simple_blocks(rest_md)
                out.append(f'#concept_box("{box_t}")[\n{body_typ}\n]')
            elif "LANDMARK STUDY" in first_q:
                tm = re.search(r"\*\*\[LANDMARK STUDY[^\]]*\]\*\*\s*(?:\*\*(.+?)\*\*)?", first_q)
                box_t = md_inline_to_typst(tm.group(1)) if (tm and tm.group(1)) else ""
                body_typ = _convert_simple_blocks(rest_md)
                out.append(f'#landmark_box("{box_t}")[\n{body_typ}\n]')
            elif "PARADIGM SHIFT" in first_q:
                tm = re.search(r"\*\*\[PARADIGM SHIFT[^\]]*\]\*\*\s*(?:\*\*(.+?)\*\*)?", first_q)
                box_t = md_inline_to_typst(tm.group(1)) if (tm and tm.group(1)) else ""
                body_typ = _convert_simple_blocks(rest_md)
                out.append(f'#shift_box("{box_t}")[\n{body_typ}\n]')
            else:
                body_typ = _convert_simple_blocks("\n".join(q_lines))
                out.append(
                    f'#block(width: 100%, fill: rgb("#F8FAFC"), stroke: (left: 3pt + muted), inset: (x: 12pt, y: 8pt))[\n{body_typ}\n]'
                )
            continue

        # Markdown Table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|\s*[:\-]+", lines[i + 1].strip()):
            t_lines = []
            while i < n and lines[i].strip().startswith("|"):
                t_lines.append(lines[i])
                i += 1
            out.append(_render_md_table_to_typst(t_lines))
            continue

        # Bullet / Numbered list item
        lm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.+)$", line)
        if lm:
            indent_spaces = len(lm.group(1))
            marker = lm.group(2)
            content = lm.group(3).strip()
            typ_indent = "  " * (indent_spaces // 2)
            typ_marker = "-" if marker in ("-", "*") else "+"
            out.append(f"{typ_indent}{typ_marker} {md_inline_to_typst(content)}")
            i += 1
            continue

        # Regular paragraph line
        out.append(md_inline_to_typst(stripped))
        i += 1

    return "\n".join(out)


def _convert_simple_blocks(md_fragment: str) -> str:
    res = []
    for ln in md_fragment.splitlines():
        s = ln.strip()
        if not s:
            res.append("")
            continue
        lm = re.match(r"^([-*]|\d+\.)\s+(.+)$", s)
        if lm:
            mk = "-" if lm.group(1) in ("-", "*") else "+"
            res.append(f"{mk} {md_inline_to_typst(lm.group(2).strip())}")
        else:
            res.append(md_inline_to_typst(s))
    return "\n".join(res)


def build_master_typst_document(stats: dict, chapters_dir: Path) -> str:
    """Assemble cover page, colophon, TOC, list of figures, and all 18 chapters into one Typst book."""
    total_p = f"{stats['total_papers']:,}"
    unique_p = f"{stats['unique_papers']:,}"
    total_d = f"{stats['total_days']:,}"
    span_str = f"{stats['earliest_date']} — {stats['latest_date']}"

    doc_parts = [
        '#import "template/textbook.typ": *',
        "",
        "// --- COVER PAGE ---",
        "#set page(width: 210mm, height: 285mm, margin: 0mm, fill: navy)",
        "#block(width: 100%, height: 100%, inset: (x: 22mm, y: 18mm))[",
        "  #text(font: sans_fonts, size: 9.5pt, weight: \"bold\", fill: rgb(\"#E8C574\"), tracking: 2.0pt)[UNIVERSITY GRADUATE TEXTBOOK & LIVING RESEARCH COMPENDIUM]",
        "  #v(5mm)",
        "  #line(length: 100%, stroke: 1.2pt + rgb(\"#E8C574\"))",
        "  #v(9mm)",
        "  #text(font: body_fonts, size: 28pt, weight: \"bold\", fill: white)[Artificial Intelligence Research]",
        "  #v(3mm)",
        "  #text(font: body_fonts, style: \"italic\", size: 15pt, fill: rgb(\"#CBD5E1\"))[Chronicle, Paradigm Flows & Frontier Evolution (2023–2026)]",
        "  #v(7mm)",
        "  #text(font: sans_fonts, size: 21.5pt, weight: \"bold\", fill: rgb(\"#F8FAFC\"))[人工智能前沿研究编年史与技术演进导论]",
        "  #v(3mm)",
        "  #text(font: sans_fonts, size: 11.2pt, fill: rgb(\"#E8C574\"))[从开源破冰、极低比特、RLVR 推理大爆炸到智能体脚手架与具身物理主体]",
        "  #v(8mm)",
        "  #align(center)[#block(width: 92%, fill: white, radius: 5pt, inset: 4pt)[",
        "    #image(\"/figures/fig02_master_sankey_2023_2026.svg\", width: 100%)",
        "  ]]",
        "  #v(1fr)",
        "  #line(length: 100%, stroke: 0.7pt + rgb(\"#475569\"))",
        "  #v(4mm)",
        "  #grid(",
        "    columns: (1.45fr, 1fr),",
        f"    [#text(font: sans_fonts, size: 9.5pt, fill: rgb(\"#E2E8F0\"))[*Empirical Corpus*: {total_p} Archived Papers ({unique_p} Unique ArXiv IDs)\\ *Archive Window*: {span_str} ({total_d} Daily Editions)]],",
        "    align(right)[#text(font: sans_fonts, size: 9.5pt, weight: \"bold\", fill: rgb(\"#E8C574\"))[HF PAPER WATCH DOG PRESS\\ Living Cumulative Edition]]",
        "  )",
        "]",
        "",
        "// --- MAIN PAGE & TYPOGRAPHY SETTINGS ---",
        "#set page(",
        "  width: 210mm,",
        "  height: 285mm,",
        "  fill: white,",
        "  margin: (top: 24mm, bottom: 23mm, inside: 21mm, outside: 21mm),",
        "  header: context {",
        "    let p = counter(page).get().first()",
        "    if p > 2 [",
        "      #set text(font: sans_fonts, size: 8.2pt, fill: muted)",
        "      #if calc.even(p) [",
        "        人工智能前沿研究编年史与技术演进导论 (2023–2026) #h(1fr) HF Paper Watch Dog",
        "      ] else [",
        "        #emph(current_chapter.get()) #h(1fr) Living Textbook Edition",
        "      ]",
        "      #v(-3pt)",
        "      #line(length: 100%, stroke: 0.4pt + rgb(\"#CBD5E1\"))",
        "    ]",
        "  },",
        "  footer: context {",
        "    let p = counter(page).get().first()",
        "    if p > 1 [",
        "      #line(length: 100%, stroke: 0.4pt + rgb(\"#E2E8F0\"))",
        "      #v(3pt)",
        "      #set text(font: sans_fonts, size: 8.5pt, fill: muted)",
        f"      #grid(columns: (1fr, auto, 1fr), [Edition Sync: {stats['latest_date']}], align(center)[#strong[#p]], align(right)[N = {total_p} Papers])",
        "    ]",
        "  }",
        ")",
        "#counter(page).update(1)",
        "#set text(font: body_fonts, size: 10pt, fill: ink, lang: \"zh\")",
        "#set par(justify: true, leading: 0.84em, spacing: 1.12em)",
        "#set heading(numbering: none)",
        "#show heading.where(level: 1): it => text(font: sans_fonts, size: 19pt, weight: \"bold\", fill: navy)[#it.body]",
        "#show heading.where(level: 2): it => block(above: 18pt, below: 9pt)[#text(font: sans_fonts, size: 13.5pt, weight: \"bold\", fill: navy)[#it.body]]",
        "#show heading.where(level: 3): it => block(above: 14pt, below: 7pt)[#text(font: sans_fonts, size: 11pt, weight: \"bold\", fill: royal)[#it.body]]",
        "#show link: it => text(fill: royal)[#it]",
        "",
        "// --- COPYRIGHT & COLOPHON PAGE ---",
        "#page(header: none)[",
        "  #v(1fr)",
        "  #text(font: sans_fonts, size: 13pt, weight: \"bold\", fill: navy)[人工智能前沿研究编年史与技术演进导论（2023–2026）]",
        "  #v(3pt)",
        "  #text(font: body_fonts, style: \"italic\", size: 10.5pt, fill: muted)[Artificial Intelligence Research: Chronicle, Paradigm Flows & Frontier Evolution]",
        "  #v(14pt)",
        "  #block(fill: rgb(\"#F8FAFC\"), stroke: 0.6pt + rgb(\"#CBD5E1\"), radius: 4pt, inset: 14pt, width: 100%)[",
        "    #set text(font: sans_fonts, size: 8.8pt, fill: ink)",
        f"    - *数据基座（Primary Corpus）*：Hugging Face Daily Papers 连续归档库（`{span_str}`，累计 {total_d} 个归档日、{total_p} 篇次、{unique_p} 篇唯一 ArXiv 论文）",
        "    - *配套单篇精读库*：`summaries/YYYY/MM/YYYY-MM-DD.{md,json}`（覆盖全量论文的「核心观点 · 方法与实验 · 实验结论 · Takeaway」四维结构化档案）",
        "    - *图表渲染引擎*：纯矢量 SVG 质量守恒 Sinkhorn 桑基流向图与多维时序统计矩阵（`chronicle/figures/`）",
        "    - *自动出版机制*：每次仓库论文更新后由 `scripts/update_all.py` 自动重算全量指标、同步章节动态表并经 Typst 引擎合并编译本书 PDF",
        "  ]",
        "  #v(12pt)",
        "  #text(size: 8.6pt, fill: muted)[本书用于学术研究与个人技术趋势研判。原始论文摘要与元数据版权归各自作者及 arXiv / Hugging Face 社区所有；本书分析框架、分类体系、可视化图表与编年史综述遵循仓库 MIT 许可协议开源。]",
        "]",
        "",
        "// --- TABLE OF CONTENTS & LIST OF FIGURES ---",
        "#pagebreak()",
        "#current_chapter.update(\"目录 · Contents\")",
        "#text(font: sans_fonts, size: 20pt, weight: \"bold\", fill: navy)[全书目录 · Table of Contents]",
        "#v(4pt)",
        "#line(length: 100%, stroke: 1.5pt + navy)",
        "#v(10pt)",
        "#outline(title: none, depth: 2, indent: 14pt)",
        "#v(18pt)",
        "#text(font: sans_fonts, size: 15pt, weight: \"bold\", fill: navy)[插图与桑基流向图目录 · List of Figures]",
        "#v(4pt)",
        "#line(length: 100%, stroke: 1pt + royal)",
        "#v(8pt)",
        "#outline(title: none, target: figure.where(kind: image))",
        "",
    ]

    for item in CHAPTER_PLAN:
        if item["part"] is not None:
            p_lbl, p_zh, p_en, p_desc = item["part"]
            doc_parts.append(
                f'#part_divider("{p_lbl}", "{p_zh}", "{p_en}", [{md_inline_to_typst(p_desc)}])'
            )
        md_file = chapters_dir / item["file"]
        md_content = md_file.read_text(encoding="utf-8")
        doc_parts.append(markdown_chapter_to_typst(md_content, item["badge"]))
        doc_parts.append("")

    return "\n".join(doc_parts)


def write_chronicle_readme(chronicle_dir: Path, stats: dict, pdf_name: str) -> None:
    """Generate chronicle/README.md indexing all chapters, figures, and PDF textbook."""
    chap_rows = []
    for item in CHAPTER_PLAN:
        f = item["file"]
        first_line = (chronicle_dir / "chapters" / f).read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        chap_rows.append(f"| `{item['badge'].split('·')[0].strip()}` | [{first_line}](./chapters/{f}) |")

    readme = f"""# 人工智能前沿研究编年史与技术演进导论（2023–2026）

> **欧美大学教材风活体编年史（Living University Textbook）** ｜ 累计覆盖 **{stats['total_papers']:,} 篇**论文（`{stats['earliest_date']}` — `{stats['latest_date']}`，共 {stats['total_days']} 个归档日）

📘 **全书精装合并版 PDF（含完整封面、目录、12 幅矢量桑基/趋势图与百篇里程碑全集）**：
👉 **[`{pdf_name}`](./{pdf_name})**

---

## 核心全景可视化预览（桑基图与热力矩阵）

![AI 研究热点跨年度注意力流向与赛道排位变迁全景桑基图](./figures/fig02_master_sankey_2023_2026.svg)

![核心技术范式四代演进谱系桑基图](./figures/fig03_paradigm_genealogy_sankey.svg)

![24 个核心技术子方向季度渗透率热力图](./figures/fig05_subtopic_velocity_heatmap.svg)

---

## 分章阅读导航（`chronicle/chapters/`）

| 章节标识 | 章节标题与独立 Markdown 入口 |
| :--- | :--- |
{chr(10).join(chap_rows)}

---

## 矢量插图索引（`chronicle/figures/`）

1. [`fig01_volume_growth_and_engagement.svg`](./figures/fig01_volume_growth_and_engagement.svg) — 2023–2026 季度规模扩张、社区热度与代码开源率双轴图
2. [`fig02_master_sankey_2023_2026.svg`](./figures/fig02_master_sankey_2023_2026.svg) — 跨年度十大研究赛道注意力流向全景桑基图
3. [`fig03_paradigm_genealogy_sankey.svg`](./figures/fig03_paradigm_genealogy_sankey.svg) — 核心技术范式四代演进谱系桑基图
4. [`fig04_quarterly_stream_share.svg`](./figures/fig04_quarterly_stream_share.svg) — 15 季度研究份额 100% 堆叠面积流图
5. [`fig05_subtopic_velocity_heatmap.svg`](./figures/fig05_subtopic_velocity_heatmap.svg) — 24 核心子方向 × 15 季度渗透率热力图
6. [`fig06_2023_2024_transition_sankey.svg`](./figures/fig06_2023_2024_transition_sankey.svg) — 2023 → 2024 奠基向效率/早融合跃迁桑基图
7. [`fig07_2025_2026_transition_sankey.svg`](./figures/fig07_2025_2026_transition_sankey.svg) — 2025 → 2026 推理超级周期向智能体与具身跃迁桑基图
8. [`fig08_architecture_and_efficiency_trends.svg`](./figures/fig08_architecture_and_efficiency_trends.svg) — 序列架构与高效推理系统季度趋势图
9. [`fig09_training_and_reasoning_coevolution.svg`](./figures/fig09_training_and_reasoning_coevolution.svg) — 训练信号三代迁移与推理范式协同演进图
10. [`fig10_multimodal_agents_embodied_rise.svg`](./figures/fig10_multimodal_agents_embodied_rise.svg) — 智能体脚手架、世界模型与具身 VLA 爆发曲线
11. [`fig11_institutions_and_open_ecosystem.svg`](./figures/fig11_institutions_and_open_ecosystem.svg) — 全球头部机构产出格局与各领域开源代码比例图
12. [`fig12_safety_vs_capability_arms_race.svg`](./figures/fig12_safety_vs_capability_arms_race.svg) — 自主能力前沿与安全护栏剪刀差演进图

---

## 本地或 CI 一键重编译命令

```bash
# 安装轻量 PDF 排版引擎依赖
pip install -r requirements.txt

# 一键增量生成单篇总结 + 重绘全部桑基/趋势图 + 同步活体章节 + 编译合并教材 PDF
python scripts/update_all.py --skip-fetch
```
"""
    (chronicle_dir / "README.md").write_text(readme, encoding="utf-8")


def build_chronicle_book(
    repo_root: Path,
    recompute_stats: bool = True,
    pdf_filename: str = "AI_Research_Chronicle_Textbook.pdf",
) -> Path:
    papers_dir = repo_root / "papers"
    summaries_dir = repo_root / "summaries"
    chronicle_dir = repo_root / "chronicle"
    chapters_dir = chronicle_dir / "chapters"
    figures_dir = chronicle_dir / "figures"

    if recompute_stats or not (chronicle_dir / "stats_snapshot.json").exists():
        stats = compute_archive_analytics(papers_dir)
        slim_stats = dict(stats)
        slim_stats["recent_frontier_papers"] = [
            {k: v for k, v in p.items() if k != "abstract"} for p in stats["recent_frontier_papers"]
        ]
        slim_stats["top_100_landmark_papers"] = [
            {k: v for k, v in p.items() if k != "abstract"} for p in stats["top_100_landmark_papers"]
        ]
        (chronicle_dir / "stats_snapshot.json").write_text(
            json.dumps(slim_stats, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        generate_all_figures(stats, figures_dir)
    else:
        stats = json.loads((chronicle_dir / "stats_snapshot.json").read_text(encoding="utf-8"))

    payloads = _build_sync_payloads(stats, summaries_dir)
    sync_markdown_chapters(chapters_dir, payloads)
    write_chronicle_readme(chronicle_dir, stats, pdf_filename)

    master_typ_content = build_master_typst_document(stats, chapters_dir)
    master_typ_path = chronicle_dir / "_compiled_book.typ"
    master_typ_path.write_text(master_typ_content, encoding="utf-8")

    pdf_out_path = chronicle_dir / pdf_filename
    try:
        import typst

        typst.compile(str(master_typ_path), root=str(chronicle_dir), output=str(pdf_out_path))
    finally:
        if master_typ_path.exists():
            master_typ_path.unlink()

    logger.info(
        "Compiled textbook PDF: %s (%.2f MB)",
        pdf_out_path,
        pdf_out_path.stat().st_size / (1024 * 1024),
    )
    return pdf_out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build living AI Research Chronicle textbook & PDF")
    parser.add_argument("--cached-stats", action="store_true", help="Reuse chronicle/stats_snapshot.json if present")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    build_chronicle_book(repo_root, recompute_stats=not args.cached_stats)


if __name__ == "__main__":
    main()
