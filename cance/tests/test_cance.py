import importlib.util
import json
from pathlib import Path
import unittest

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("cance_app", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
# Streamlit is imported by the app; the test environment installs requirements first.
SPEC.loader.exec_module(MODULE)


class CanceModelTests(unittest.TestCase):
    def test_has_five_distinct_branches(self):
        self.assertEqual(len(MODULE.BRANCHES), 5)
        self.assertEqual(len({b["id"] for b in MODULE.BRANCHES}), 5)

    def test_every_branch_has_required_fields(self):
        required = {
            "intervention", "causal_chain", "response", "ending", "themes",
            "assumptions", "uncertainty", "uncertainty_reason", "mechanism"
        }
        for branch in MODULE.BRANCHES:
            self.assertTrue(required.issubset(branch.keys()), branch["name"])
            self.assertGreaterEqual(len(branch["causal_chain"]), 3)
            self.assertGreaterEqual(len(branch["assumptions"]), 1)

    def test_no_empirical_probabilities_are_encoded(self):
        serialized = json.dumps(MODULE.BRANCHES).lower()
        self.assertNotIn("survival_probability", serialized)
        self.assertNotIn("p=0.", serialized)

    def test_film_facts_and_hypotheticals_are_separate(self):
        self.assertTrue(MODULE.ESTABLISHED_FACTS)
        self.assertTrue(MODULE.INVENTED_EVENTS)
        self.assertTrue(any("invented" in item.lower() for item in MODULE.INVENTED_EVENTS))


if __name__ == "__main__":
    unittest.main()
