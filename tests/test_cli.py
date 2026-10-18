import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from intentline import __version__
from intentline.cli import main, parser


class CLI(unittest.TestCase):
    def run_version_entrypoint(self, *args):
        """Run the real module in an otherwise empty disposable working directory."""
        with tempfile.TemporaryDirectory(prefix="intentline-54-") as directory:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
            completed = subprocess.run(
                [sys.executable, "-B", "-m", "intentline", *args],
                cwd=directory, env=env, capture_output=True, text=True,
                timeout=20, check=False,
            )
            self.assertEqual(
                list(Path(directory).iterdir()), [],
                "A read-only CLI version/argument query must not create work files",
            )
            return completed

    def test_help_has_commands(self):
        help_text = parser().format_help()
        self.assertIn("audit-record", help_text)
        self.assertIn("--version", help_text)

    def test_error_envelope(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--json", "status"]), 2)
        result = json.loads(out.getvalue())
        self.assertFalse(result["ok"])
        self.assertEqual(result["schema_version"], 1)

    def test_R1_human_version_subprocess(self):
        """R1: version prints to a human without needing a work directory."""
        completed = self.run_version_entrypoint("--version")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, f"intentline {__version__}\n")
        self.assertEqual(completed.stderr, "")

    def test_R2_structured_version_subprocess(self):
        """R2: both global flag orders produce one stable schema-1 result."""
        for argv in (("--json", "--version"), ("--version", "--json")):
            with self.subTest(argv=argv):
                completed = self.run_version_entrypoint(*argv)
                self.assertEqual(completed.returncode, 0)
                self.assertEqual(completed.stderr, "")
                self.assertEqual(completed.stdout.count("\n"), 1)
                data = json.loads(completed.stdout)
                self.assertEqual(data["result"], "intentline.result")
                self.assertEqual(data["schema_version"], 1)
                self.assertEqual(data["command"], "version")
                self.assertIs(data["ok"], True)
                self.assertEqual(data["data"]["version"], __version__)

    def test_version_cannot_dispatch_another_command(self):
        completed = self.run_version_entrypoint(
            "--version", "status", "--work", "not-a-real-work-directory"
        )
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertIn("cannot be combined", completed.stderr)

    def test_missing_command_still_fails_and_is_machine_readable(self):
        completed = self.run_version_entrypoint("--json")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("required: command", completed.stderr)
        envelope = json.loads(completed.stdout)
        self.assertEqual(envelope["schema_version"], 1)
        self.assertIs(envelope["ok"], False)
        self.assertEqual(envelope["error"]["code"], 2)
