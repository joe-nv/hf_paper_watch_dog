import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestTaxonomyAndGlossary(unittest.TestCase):
    def test_domain_classification_accuracy(self):
        from scripts.taxonomy import DOMAINS, GLOSSARY_TERMS, classify_paper

        self.assertEqual(len(DOMAINS), 10)
        self.assertGreaterEqual(len(GLOSSARY_TERMS), 60)

        seen_keys = set()
        for entry in GLOSSARY_TERMS:
            key = (entry["en"].lower(), entry.get("sense", "default"))
            self.assertNotIn(key, seen_keys, f"Duplicate glossary entry: {key}")
            seen_keys.add(key)
            self.assertTrue(entry["zh"].strip())

        r1 = classify_paper(
            {
                "title": "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
                "abstract": "We incentivize reasoning in LLMs using pure reinforcement learning and GRPO without SFT.",
            }
        )
        self.assertIn(r1["primary_domain"], {"Training_RL", "Reasoning"})
        self.assertIn("Training_RL", r1["domains"])
        self.assertIn("Reasoning", r1["domains"])

        vla = classify_paper(
            {
                "title": "Motion Mamba 2.0: Autoregressive Diffusion Mamba for Long-Horizon Humanoid Control",
                "abstract": "Real-time controllable motion generation for humanoid robotics using Mamba states and CUDA Graph kernels.",
            }
        )
        self.assertIn("Embodied", vla["domains"])
        self.assertIn("Architecture", vla["domains"])


class TestPaperSummarizer(unittest.TestCase):
    def test_single_paper_summary_structure_and_fidelity(self):
        from scripts.summarize_papers import summarize_date_file, summarize_paper

        sample_path = REPO_ROOT / "papers" / "2026" / "11" / "2026-11-24.json"
        data = json.loads(sample_path.read_text(encoding="utf-8"))
        first_paper = data["papers"][0]

        summary = summarize_paper(first_paper, date_str="2026-11-24")
        for field in ("perspective", "experiments", "conclusions", "takeaway"):
            self.assertIn(field, summary)
            self.assertGreater(len(summary[field]), 30)
            has_cjk = any("\u4e00" <= ch <= "\u9fff" for ch in summary[field])
            self.assertTrue(has_cjk, f"Field {field} must contain Chinese prose")

        self.assertIn("276.14", summary["conclusions"])
        self.assertIn("HiPHI", summary["experiments"])

        with tempfile.TemporaryDirectory() as tmp:
            out_base = Path(tmp) / "summaries"
            res = summarize_date_file(sample_path, out_base)
            self.assertTrue(res["md_path"].exists())
            self.assertTrue(res["json_path"].exists())
            saved = json.loads(res["json_path"].read_text(encoding="utf-8"))
            self.assertEqual(saved["total"], data["total"])


class TestAnalyticsAndFigures(unittest.TestCase):
    def test_stats_and_svg_generation(self):
        from scripts.generate_figures import compute_archive_analytics, generate_all_figures

        stats = compute_archive_analytics(REPO_ROOT / "papers")
        self.assertGreater(stats["total_papers"], 18000)
        self.assertTrue({"2023", "2024", "2025", "2026"}.issubset(stats["years"].keys()))

        with tempfile.TemporaryDirectory() as tmp:
            fig_dir = Path(tmp) / "figures"
            paths = generate_all_figures(stats, fig_dir)
            self.assertGreaterEqual(len(paths), 12)
            for p in paths:
                self.assertTrue(p.exists(), f"Missing SVG figure {p}")
                root = ET.fromstring(p.read_text(encoding="utf-8"))
                self.assertTrue(root.tag.endswith("svg"))


class TestChronicleBookBuild(unittest.TestCase):
    def test_compiled_book_and_synced_chapters(self):
        from scripts.build_chronicle import CHAPTER_PLAN, build_chronicle_book, md_inline_to_typst

        escaped = md_inline_to_typst("Cost is between $15 and $20 per paper, while $x_1 + x_2 = 1$ holds.")
        self.assertIn(r"\$15", escaped)
        self.assertIn(r"\$20", escaped)

        pdf_path = build_chronicle_book(REPO_ROOT, recompute_stats=False)
        self.assertTrue(pdf_path.exists())
        self.assertGreater(pdf_path.stat().st_size, 500_000)

        chapters_dir = REPO_ROOT / "chronicle" / "chapters"
        self.assertEqual(len(list(chapters_dir.glob("*.md"))), len(CHAPTER_PLAN))
        ch01 = (chapters_dir / "ch01_macro_landscape_sankey.md").read_text(encoding="utf-8")
        self.assertIn("表 1.1", ch01)
        self.assertIn("18,137", ch01)


if __name__ == "__main__":
    unittest.main()
