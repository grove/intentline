"""Issue #54: real CLI behavior tests, separate from immutable historical tests.

Subprocesses use the actual python -B -m intentline entrypoint.
No saved Intentline acceptance records, targets or project files are created.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from intentline import __version__
from intentline.cli import parser


class VersionQueries(unittest.TestCase):
    def invoke(self, *args):
        with tempfile.TemporaryDirectory(prefix="intentline-54-") as directory:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
            p = subprocess.run(
                [sys.executable, "-B", "-m", "intentline", *args],
                cwd=directory, env=env, capture_output=True, text=True,
                timeout=20, check=False,
            )
            self.assertEqual(
                list(Path(directory).iterdir()), [],
                "Version and usage queries may not leave a saved work record",
            )
            return p

    def test_R1_human_version(self):
        """R1: one exact human-readable line; no record or stderr."""
        result = self.invoke("--version")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, f"intentline {__version__}\n")
        self.assertEqual(result.stderr, "")
        self.assertIn("--version", parser().format_help())

    def test_R2_json_version(self):
        """R2: both global flag orders produce the schema-1 machine result."""
        for flags in (("--json", "--version"), ("--version", "--json")):
            with self.subTest(flags=flags):
                result = self.invoke(*flags)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stderr, "")
                self.assertEqual(result.stdout.count("\n"), 1)
                obj = json.loads(result.stdout)
                self.assertEqual(obj["result"], "intentline.result")
                self.assertEqual(obj["schema_version"], 1)
                self.assertEqual(obj["command"], "version")
                self.assertIs(obj["ok"], True)
                self.assertEqual(obj["data"]["version"], __version__)

    def test_version_with_command_is_rejected_not_executed(self):
        result = self.invoke("--version", "status", "--work", "missing")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("cannot be combined", result.stderr)

    def test_missing_subcommand_still_fails_in_json_mode(self):
        result = self.invoke("--json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("required: command", result.stderr)
        obj = json.loads(result.stdout)
        self.assertIs(obj["ok"], False)
        self.assertEqual(obj["error"]["code"], 2)


if __name__ == "__main__":
    unittest.main()
