import io
import unittest
from contextlib import redirect_stderr
from contextlib import redirect_stdout

from fissionwatch import __version__
from fissionwatch.cli import main


class CliTests(unittest.TestCase):
    def test_version_command_prints_package_version(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["version"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), __version__)

    def test_ceq_command_prints_numeric_value(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                ["ceq", "--availability", "1.0", "--latency-s", "0.0", "--error-rate", "0.0"]
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "1.000000")

    def test_rsri_command_prints_numeric_value(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["rsri", "--rho", "0.2", "--sigma-star", "0.5", "--cia", "0.8"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "0.179732")

    def test_invalid_arguments_return_nonzero_exit_code(self):
        output = io.StringIO()
        with redirect_stderr(output):
            exit_code = main(["ceq", "--availability", "1.0"])

        self.assertNotEqual(exit_code, 0)
        self.assertIn("usage:", output.getvalue())

    def test_missing_subcommand_returns_nonzero_exit_code(self):
        output = io.StringIO()
        with redirect_stderr(output):
            exit_code = main([])

        self.assertEqual(exit_code, 2)
        self.assertIn("usage:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
