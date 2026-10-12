import contextlib
import io
import json
import unittest

from intentline.cli import main, parser


class CLI(unittest.TestCase):
    def test_help_has_commands(self):
        self.assertIn("audit-record", parser().format_help())

    def test_error_envelope(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--json", "status"]), 2)
        result = json.loads(out.getvalue())
        self.assertFalse(result["ok"])
        self.assertEqual(result["schema_version"], 1)
