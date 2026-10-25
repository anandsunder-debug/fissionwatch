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


class CanceModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = APP_PATH.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source, filename=str(APP_PATH))
        cls.lenses = literal_assignment(cls.tree, "LENSES")

    def test_app_parses_as_python(self):
        self.assertIsNotNone(self.tree)

    def test_has_multiple_distinct_causal_lenses(self):
        self.assertGreaterEqual(len(self.lenses), 8)
        self.assertEqual(len({lens["name"] for lens in self.lenses}), len(self.lenses))
        self.assertTrue(all(lens["mechanism"] and lens["focus"] for lens in self.lenses))

    def test_generic_inputs_and_branch_generator_exist(self):
        for term in ("plot", "decision", "intervention", "character_rules", "world_rules"):
            self.assertIn(term, self.source)
        self.assertIn("def make_branches", self.source)
        self.assertIn("def build_report", self.source)

    def test_traceability_fields_exist(self):
        for term in ('"Baseline"', '"Intervention"', '"Mechanism"', '"Decision response"',
                     '"Immediate consequence"', '"Downstream propagation"', '"Outcome"',
                     '"basis"', '"status"', '"assumptions"', '"checks"'):
            self.assertIn(term, self.source)

    def test_exports_markdown_and_json(self):
        self.assertIn("report_markdown", self.source)
        self.assertIn("json.dumps", self.source)
        self.assertIn("download_button", self.source)

    def test_no_calibrated_numeric_probabilities_claimed(self):
        self.assertIn("No numeric probabilities are assigned", self.source)
        self.assertIn("not calibrated", self.source.lower())

    def test_not_tied_to_one_film(self):
        self.assertNotIn("Zubeidaa", self.source)
        self.assertIn("Plot / synopsis", self.source)
        self.assertIn("Generate counterfactual outcomes", self.source)


if __name__ == "__main__":
    unittest.main()
