"""Unit tests for the pure CANCE story-generation engine.

The app is a Streamlit script, so tests load its constants and pure functions from
the AST without executing the UI or requiring a browser session.
"""
import ast
import json
import re
import unittest
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def load_engine():
    source = APP_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(APP_PATH))
    wanted_constants = {"APP_VERSION", "GENRES", "TONES", "VARIATIONS"}
    body = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = {t.id for t in node.targets if isinstance(t, ast.Name)}
            if names & wanted_constants:
                body.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {
            "words", "similarity", "build_candidates", "score_candidate",
            "score_diversity", "make_report", "markdown_report",
            "alternate_plots_markdown",
        }:
            body.append(node)
    module = ast.Module(body=body, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {
        "re": re,
        "combinations": combinations,
        "datetime": datetime,
        "timezone": timezone,
        "Any": Any,
    }
    exec(compile(module, str(APP_PATH), "exec"), namespace)
    namespace["source"] = source
    return namespace


class CanceMovieGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = load_engine()
        cls.source = cls.engine["source"]
        cls.variations = cls.engine["VARIATIONS"]

    def sample_candidates(self, count=5, scene_count=8):
        return self.engine["build_candidates"](
            "Test Film",
            "A coastal engineer discovers the flood barriers are being sabotaged",
            "Mira, a coastal engineer",
            "identify who is sabotaging the flood barriers",
            "a city could be flooded during the next storm",
            "Keep the engineering plausible and preserve the protagonist's motivation.",
            "Thriller",
            "Suspenseful",
            scene_count,
            count,
        )

    def score(self, candidates, weights=None, constraints="keep it plausible"):
        if weights is None:
            weights = {
                "Causal coherence": 3.0,
                "Character / goal continuity": 2.5,
                "Variation capture": 2.5,
                "Premise specificity": 2.0,
                "Payoff structure": 2.0,
                "Constraint adherence (proxy)": 2.0,
            }
        return [
            self.engine["score_candidate"](c, candidates, weights, constraints)
            for c in candidates
        ]

    def test_app_parses_and_compiles(self):
        tree = ast.parse(self.source)
        compile(tree, str(APP_PATH), "exec")

    def test_variation_operators_have_unique_names_and_tags(self):
        self.assertGreaterEqual(len(self.variations), 8)
        self.assertEqual(len({v["name"] for v in self.variations}), len(self.variations))
        self.assertEqual(len({v["tag"] for v in self.variations}), len(self.variations))

    def test_generation_and_export_functions_exist(self):
        names = {n.name for n in ast.parse(self.source).body if isinstance(n, ast.FunctionDef)}
        expected = {
            "build_candidates", "score_candidate", "score_diversity",
            "make_report", "markdown_report", "alternate_plots_markdown",
        }
        self.assertTrue(expected.issubset(names))

    def test_requested_number_of_candidates_is_generated(self):
        for count in (3, 5, 10):
            with self.subTest(count=count):
                self.assertEqual(len(self.sample_candidates(count=count)), count)

    def test_candidate_ids_are_unique_and_sequential(self):
        candidates = self.sample_candidates(count=6)
        self.assertEqual([c["id"] for c in candidates], [1, 2, 3, 4, 5, 6])

    def test_scene_count_is_clamped_to_supported_range(self):
        self.assertEqual(len(self.sample_candidates(scene_count=2)[0]["beats"]), 4)
        self.assertEqual(len(self.sample_candidates(scene_count=20)[0]["beats"]), 8)
        self.assertEqual(len(self.sample_candidates(scene_count=6)[0]["beats"]), 6)

    def test_scene_beats_have_causal_links(self):
        for candidate in self.sample_candidates():
            self.assertTrue(candidate["script_draft"])
            self.assertTrue(all(beat["causal_link"].strip() for beat in candidate["beats"]))
            self.assertEqual(len(candidate["beats"]), 8)

    def test_user_inputs_propagate_into_candidate(self):
        candidate = self.sample_candidates(count=1)[0]
        self.assertEqual(candidate["genre"], "Thriller")
        self.assertEqual(candidate["tone"], "Suspenseful")
        self.assertIn("coastal engineer", candidate["protagonist"])
        self.assertIn("flood barriers", candidate["goal"])

    def test_variation_paths_rotate_across_candidates(self):
        candidates = self.sample_candidates(count=10)
        self.assertGreaterEqual(len({c["variation"] for c in candidates}), 8)
        self.assertGreater(len({c["causal_summary"] for c in candidates}), 1)

    def test_word_and_similarity_metrics_are_bounded(self):
        words = self.engine["words"]
        similarity = self.engine["similarity"]
        self.assertIn("story", words("A clear story with causal links"))
        self.assertEqual(similarity("same text", "same text"), 1.0)
        self.assertGreaterEqual(similarity("alpha beta", "beta gamma"), 0.0)
        self.assertLessEqual(similarity("alpha beta", "beta gamma"), 1.0)
        self.assertEqual(similarity("", ""), 0.0)

    def test_scoring_adds_components_and_reward(self):
        candidates = self.sample_candidates(count=3)
        scored = self.score(candidates)
        expected = {
            "Causal coherence", "Character / goal continuity", "Variation capture",
            "Premise specificity", "Payoff structure", "Constraint adherence (proxy)",
        }
        for candidate in scored:
            self.assertEqual(set(candidate["utility_components"]), expected)
            self.assertGreaterEqual(candidate["reward_score"], 0)
            self.assertLessEqual(candidate["reward_score"], 10)
            self.assertIn("heuristic", candidate["reward_caveat"].lower())

    def test_zero_weights_produce_zero_reward_without_division_error(self):
        candidates = self.sample_candidates(count=1)
        zero_weights = {key: 0 for key in (
            "Causal coherence", "Character / goal continuity", "Variation capture",
            "Premise specificity", "Payoff structure", "Constraint adherence (proxy)",
        )}
        scored = self.score(candidates, zero_weights)
        self.assertEqual(scored[0]["reward_score"], 0.0)

    def test_negative_weights_are_ignored(self):
        candidates = self.sample_candidates(count=1)
        negative_weights = {"Causal coherence": -10}
        scored = self.score(candidates, negative_weights)
        self.assertEqual(scored[0]["reward_score"], 0.0)

    def test_shorter_scene_plan_has_lower_payoff_proxy(self):
        full = self.score(self.sample_candidates(count=1, scene_count=8))[0]
        short = self.score(self.sample_candidates(count=1, scene_count=4))[0]
        self.assertGreater(full["utility_components"]["Payoff structure"],
                           short["utility_components"]["Payoff structure"])

    def test_diversity_pair_count_and_metrics(self):
        candidates = self.score(self.sample_candidates(count=4))
        diversity = self.engine["score_diversity"](candidates)
        self.assertEqual(len(diversity["pairwise"]), 6)
        self.assertGreaterEqual(diversity["mean_text_similarity"], 0)
        self.assertLessEqual(diversity["mean_text_similarity"], 1)
        for pair in diversity["pairwise"]:
            self.assertAlmostEqual(pair["variation_distance"], 1 - pair["similarity"], places=3)
        self.assertGreater(diversity["variation_coverage_count"], 0)

    def test_diversity_handles_zero_or_one_candidate(self):
        score_diversity = self.engine["score_diversity"]
        self.assertEqual(score_diversity([])["pairwise"], [])
        single = self.sample_candidates(count=1)
        self.assertEqual(score_diversity(single)["mean_text_similarity"], 0.0)
        self.assertEqual(score_diversity(single)["pairwise"], [])

    def test_report_is_json_serializable(self):
        candidates = self.score(self.sample_candidates(count=3))
        diversity = self.engine["score_diversity"](candidates)
        report = self.engine["make_report"](
            {"title": "Test Film", "candidate_count": len(candidates)},
            candidates,
            diversity,
        )
        encoded = json.dumps(report, ensure_ascii=False)
        decoded = json.loads(encoded)
        self.assertEqual(len(decoded["candidates"]), 3)
        self.assertIn("generated_at_utc", decoded)

    def test_full_markdown_report_contains_each_candidate(self):
        candidates = self.score(self.sample_candidates(count=3))
        for rank, candidate in enumerate(candidates, 1):
            candidate["rank"] = rank
        report = self.engine["make_report"](
            {"title": "Test Film"}, candidates, self.engine["score_diversity"](candidates)
        )
        markdown = self.engine["markdown_report"](report)
        self.assertIn("# CANCE Movie Generator Report", markdown)
        for candidate in candidates:
            self.assertIn(candidate["title"], markdown)
            self.assertIn(candidate["script_draft"], markdown)

    def test_alternate_plot_file_contains_every_branch_and_scene_draft(self):
        candidates = self.score(self.sample_candidates(count=5))
        for rank, candidate in enumerate(candidates, 1):
            candidate["rank"] = rank
        report = self.engine["make_report"](
            {"title": "Alternate Plot Test"},
            candidates,
            self.engine["score_diversity"](candidates),
        )
        output = self.engine["alternate_plots_markdown"](report)
        self.assertTrue(output.startswith("# CANCE — Alternate Plot Branches"))
        self.assertIn("Number of alternatives:** 5", output)
        for candidate in candidates:
            self.assertIn(candidate["title"], output)
            self.assertIn(candidate["script_draft"], output)
        self.assertIn("\n## Alternative", output)

    def test_ui_exposes_separate_alternate_plot_download(self):
        self.assertIn("Save alternate plots (.md)", self.source)
        self.assertIn('file_name="cance_alternate_plots.md"', self.source)
        self.assertIn('file_name="cance_movie_generator_report.json"', self.source)

    def test_reward_and_diversity_metrics_are_caveated(self):
        self.assertIn("not an audience preference estimate", self.source)
        self.assertIn("not a semantic originality score", self.source)
        self.assertIn("not finished film or video", self.source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
