#!/usr/bin/env python3
"""
Unified orchestrator for daily updates:
1. (Optional) Fetch daily papers via scripts/fetch_papers.py
2. Incrementally summarize new papers into summaries/YYYY/MM/
3. Recompute longitudinal analytics & regenerate vector Sankey/trend SVG charts
4. Sync live chapter tables/radars and compile chronicle/AI_Research_Chronicle_Textbook.pdf
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

try:
    from scripts.build_chronicle import build_chronicle_book
    from scripts.summarize_papers import build_summaries_readme_and_index, load_funny_index_lookup, summarize_date_file
except ImportError:
    from build_chronicle import build_chronicle_book
    from summarize_papers import build_summaries_readme_and_index, load_funny_index_lookup, summarize_date_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch, summarize, and rebuild the AI Research Chronicle PDF")
    parser.add_argument("date", nargs="?", default=None, help="Optional date YYYY-MM-DD for fetch_papers.py")
    parser.add_argument("--backfill", type=int, default=0, help="Optional backfill days for fetch_papers.py")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetching from HF API; use local papers/")
    parser.add_argument("--resummarize-all", action="store_true", help="Regenerate all summaries even if existing")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    if not args.skip_fetch:
        cmd = [sys.executable, str(repo_root / "scripts" / "fetch_papers.py")]
        if args.date:
            cmd.append(args.date)
        if args.backfill > 0:
            cmd.extend(["--backfill", str(args.backfill)])
        logger.info("Step 1/3: Running %s", " ".join(cmd))
        subprocess.run(cmd, check=True)

    logger.info("Step 2/3: Updating structured per-paper summaries in summaries/...")
    papers_dir = repo_root / "papers"
    summaries_dir = repo_root / "summaries"
    curated_lookup = load_funny_index_lookup(repo_root)
    new_days = 0
    for pf in sorted(papers_dir.glob("*/*/*.json")):
        date_str = pf.stem
        yr, mo, _ = date_str.split("-")
        out_md = summaries_dir / yr / mo / f"{date_str}.md"
        if not args.resummarize_all and out_md.exists():
            continue
        summarize_date_file(pf, summaries_dir, curated_lookup=curated_lookup)
        new_days += 1
    summaries_dir.mkdir(parents=True, exist_ok=True)
    build_summaries_readme_and_index(summaries_dir)
    logger.info("Summaries synced (%d newly generated date files).", new_days)

    logger.info("Step 3/3: Rebuilding longitudinal figures, chapters, and textbook PDF...")
    pdf_path = build_chronicle_book(repo_root, recompute_stats=True)
    logger.info("All steps complete -> %s", pdf_path)


if __name__ == "__main__":
    main()
