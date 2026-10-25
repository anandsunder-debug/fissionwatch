import ast
from pathlib import Path
import unittest

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def literal_assignment(module_ast, variable_name):
    for node in module_ast.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"Could not find literal assignment for {variable_name}")


class CanceMovieGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = APP_PATH.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source, filename=str(APP_PATH))
        cls.variations = literal_assignment(cls.tree, "VARIATIONS")

    def test_app_parses(self):
        self.assertIsNotNone(self.tree)

    def test_variation_operators_are_distinct(self):
        self.assertGreaterEqual(len(self.variations), 8)
        self.assertEqual(len({item["name"] for item in self.variations}), len(self.variations))
        self.assertEqual(len({item["tag"] for item in self.variations}), len(self.variations))

    def test_generation_and_scoring_functions_exist(self):
        names = {n.name for n in self.tree.body if isinstance(n, ast.FunctionDef)}
        for name in ("build_candidates", "score_candidate", "score_diversity", "make_report", "markdown_report"):
            self.assertIn(name, names)

    def test_reward_formula_and_variation_metrics_are_explicit(self):
        self.assertIn("reward_score", self.source)
        self.assertIn("utility_components", self.source)
        self.assertIn("variation_coverage", self.source)
        self.assertIn("mean_text_similarity", self.source)
        self.assertIn("variation_distance", self.source)

    def test_user_can_generate_multiple_candidates(self):
        self.assertIn('st.slider("Alternative film trajectories", 3, 10, 5)', self.source)
        self.assertIn("Generate film variations", self.source)

    def test_exports_markdown_and_json(self):
        self.assertIn("download_button", self.source)
        self.assertIn("json.dumps", self.source)
        self.assertIn("cance_movie_generator_report.json", self.source)

    def test_scores_are_caveated_as_heuristics(self):
        self.assertIn("not an audience preference estimate", self.source)
        self.assertIn("not finished film or video", self.source)

if __name__ == "__main__":
    unittest.main()
