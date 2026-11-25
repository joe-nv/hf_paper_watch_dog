# HuggingFace Daily Papers Archive, Summaries & Living Chronicle

Automatically fetch, summarize, and synthesize [Hugging Face Daily Papers](https://huggingface.co/papers) into a per-paper structured knowledge base and an auto-compiled **Western university textbook-style AI Research Chronicle PDF** with multi-year Sankey flow diagrams.

## Repository Structure

```
papers/                                     # Raw daily paper archive (2023-05 to present)
└── YYYY/MM/
    ├── YYYY-MM-DD.md                       # Human-readable daily papers
    └── YYYY-MM-DD.json                     # Structured metadata & abstracts

summaries/                                  # Per-paper structured summaries (中文为主 + 英文术语)
├── README.md                               # Domain breakdown & archive index
├── index.json                              # Cumulative summary counts
└── YYYY/MM/
    ├── YYYY-MM-DD.md                       # 观点 / 实验 / 结论 / Takeaway per paper
    └── YYYY-MM-DD.json                     # Machine-readable structured summaries

chronicle/                                  # Living University Textbook & Sankey Trend Atlas
├── README.md                               # Chapter navigation & embedded Sankey previews
├── AI_Research_Chronicle_Textbook.pdf      # Auto-compiled merged textbook PDF (110+ pages, vector charts)
├── stats_snapshot.json                     # Longitudinal metrics across 15+ quarters
├── chapters/                               # 18 modular chapters & appendices (ch00..ch14, appA..appC)
├── figures/                                # 12 vector SVG Sankey diagrams, heatmaps & trend curves
└── template/textbook.typ                   # Typst university textbook typesetting template
```

## Key Features

1. **Daily Raw Archive (`papers/`)**: ArXiv ID, Title, Authors, Organization, Published/Submitted dates, Upvotes, Abstract, and GitHub/Project links sorted by upvotes.
2. **Per-Paper Structured Digest (`summaries/`)**: Every archived paper is distilled into four structured dimensions — **核心观点 (Perspective)**, **方法与实验 (Experiments)**, **实验结论 (Conclusions)**, and **核心启示 (Takeaway)** — with unified bilingual terminology.
3. **Living Chronicle Textbook (`chronicle/`)**:
   - **Multi-Year Sankey / Alluvial Flow Diagrams** tracking how research attention flows and mutates from 2023 → 2024 → 2025 → 2026 across 10 core domains and 24 subtopics.
   - **Hybrid Structure**: Part I (Macro Panorama & Sankey Flows), Part II (2023–2026 Annual Chronicles + Live 30-Day Frontier Radar), Part III (9 Vertical Technical Deep-Dive Chapters), and Part IV (Methodology, Top-100 Landmark Compendium & Bilingual Glossary).
   - **Auto-Merged PDF**: Rebuilt automatically after every daily paper update into [`chronicle/AI_Research_Chronicle_Textbook.pdf`](./chronicle/AI_Research_Chronicle_Textbook.pdf).

## Automation & Local Usage

A GitHub Actions workflow runs daily at **08:00 UTC**, fetches the day's papers, generates structured summaries, updates all Sankey/trend charts, recompiles the textbook PDF, and commits the updates.

```bash
# install PDF compiler dependency (fetching, summarizing & SVG generation use Python stdlib only)
pip install -r requirements.txt

# run full pipeline: fetch today's papers -> incremental summaries -> rebuild figures & textbook PDF
python scripts/update_all.py

# rebuild summaries, Sankey figures, and textbook PDF from existing local papers/ without network fetch
python scripts/update_all.py --skip-fetch

# fetch papers only for a specific date or backfill range
python scripts/fetch_papers.py 2026-03-17
python scripts/fetch_papers.py --backfill 7
```

## Data Source & Credit

All paper metadata (titles, authors, abstracts, upvotes, etc.) is sourced from
[Hugging Face Daily Papers](https://huggingface.co/papers), which aggregates
submissions from the research community. The original paper content is hosted on
[arXiv](https://arxiv.org/) and is subject to each paper's own license
(typically CC BY or similar open-access terms).

This repository is an **unofficial archive** and is not affiliated with or
endorsed by Hugging Face or arXiv.

## License

The archiving scripts in this repository are released under the
[MIT License](LICENSE). The archived paper metadata originates from publicly
accessible sources (Hugging Face and arXiv) and is redistributed here for
research and educational purposes with full attribution. All rights to the
original paper content remain with their respective authors and publishers.
If you are an author and wish to have your metadata removed, please
[open an issue](https://github.com/joe0731/hf_paper_watch_dog/issues).
