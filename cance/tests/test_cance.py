import ast
import json
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
        cls.branches = literal_assignment(cls.tree, "BRANCHES")
        cls.facts = literal_assignment(cls.tree, "ESTABLISHED_FACTS")
        cls.invented = literal_assignment(cls.tree, "INVENTED_EVENTS")

    def test_app_parses_as_python(self):
        self.assertIsNotNone(self.tree)

    def test_has_five_distinct_branches(self):
        self.assertEqual(len(self.branches), 5)
        self.assertEqual(len({branch["id"] for branch in self.branches}), 5)

    def test_every_branch_has_required_fields(self):
        required = {
            "intervention", "causal_chain", "response", "ending", "themes",
            "assumptions", "uncertainty", "uncertainty_reason", "mechanism"
        }
        for branch in self.branches:
            self.assertTrue(required.issubset(branch.keys()), branch["name"])
            self.assertGreaterEqual(len(branch["causal_chain"]), 3)
            self.assertGreaterEqual(len(branch["assumptions"]), 1)

    def test_no_empirical_probabilities_are_encoded(self):
        serialized = json.dumps(self.branches).lower()
        self.assertNotIn("survival_probability", serialized)
        self.assertNotIn("p=0.", serialized)

    def test_film_facts_and_hypotheticals_are_separate(self):
        self.assertTrue(self.facts)
        self.assertTrue(self.invented)
        self.assertTrue(any("invented" in item.lower() for item in self.invented))


if __name__ == "__main__":
    unittest.main()
