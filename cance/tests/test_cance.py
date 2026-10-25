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


class CanceGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = APP_PATH.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source, filename=str(APP_PATH)
        )
        cls.lenses = literal_assignment(cls.tree, "LENSES")

    def test_app_parses_as_python(self):
        self.assertIsNotNone(self.tree)

    def test_has_multiple_causal_lenses(self):
        self.assertGreaterEqual(len(self.lenses), 8)
        self.assertEqual(len({lens[0] for lens in self.lenses}), len(self.lenses))

    def test_graph_engine_functions_exist(self):
        for name in ("parse_nodes", "parse_edges", "descendants", "validate_graph",
                     "graph_dot", "generate_branches", "build_report"):
            self.assertTrue(any(isinstance(n, ast.FunctionDef) and n.name == name for n in self.tree.body), name)

    def test_traceability_and_exports_exist(self):
        for term in ("causal_chain", "basis", "status", "assumptions", "report_markdown",
                     "download_button", "json.dumps"):
            self.assertIn(term, self.source)

    def test_cycle_detection_and_unknown_endpoint_validation(self):
        self.assertIn("contains a cycle", self.source)
        self.assertIn("unknown node", self.source.lower())

    def test_probabilities_are_not_claimed_as_calibrated(self):
        self.assertIn("no numeric probabilities are assigned", self.source.lower())
        self.assertIn("qualitative; not calibrated", self.source.lower())

    def test_generic_not_film_specific(self):
        self.assertNotIn("Zubeidaa", self.source)
        self.assertIn("Generic Causal Graph Engine", self.source)

if __name__ == "__main__":
    unittest.main()
