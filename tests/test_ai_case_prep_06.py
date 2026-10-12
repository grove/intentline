"""Authored preparation mechanics; mocks do not qualify any real host boundary."""

import errno
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from evaluation.cases.ai_06 import access_canaries as canary


class AccessCanaryTests(unittest.TestCase):
    def test_positive_and_readable_private_path_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "sentinel"
            sentinel.write_bytes(b"nonsecret\n")
            self.assertEqual(canary.visible_canary(sentinel, b"nonsecret\n"), hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"))
            self.assertFalse(canary.visible_canary(sentinel, b"wrong\n"))
            self.assertFalse(canary.forbidden_canary(sentinel))
            self.assertFalse(canary.forbidden_canary(Path(directory) / "absent"))

    def test_permission_denial_is_only_a_sample(self):
        with patch.object(canary.os, "O_NONBLOCK", 0, create=True), \
                patch.object(canary.os, "open", side_effect=PermissionError(errno.EACCES, "denied")):
            self.assertTrue(canary.forbidden_canary("synthetic-private-sentinel"))
        result = canary.summary(True, [True, True, True, True], True, True)
        self.assertTrue(result["sample_probes_passed"])
        self.assertFalse(result["host_qualified"])
        self.assertFalse(canary.summary(True, [], True, True)["sample_probes_passed"])
        self.assertFalse(canary.summary(True, [True, False], True, True)["sample_probes_passed"])

    def test_missing_nonblocking_flag_refuses_before_io(self):
        with patch.dict(canary.os.__dict__), patch.object(canary.os, "open") as opened:
            canary.os.__dict__.pop("O_NONBLOCK", None)
            self.assertFalse(canary.visible_canary("nonsecret", b"visible"))
            self.assertFalse(canary.forbidden_canary("nonsecret"))
            opened.assert_not_called()

    def test_network_refusal_timeout_missing_endpoint_do_not_prove_policy(self):
        for error in (ConnectionRefusedError(errno.ECONNREFUSED, "refused"), TimeoutError(),
                      OSError(errno.ENETUNREACH, "unreachable")):
            with self.subTest(error=type(error).__name__), patch.object(canary.socket, "socket") as factory:
                factory.return_value.__enter__.return_value.connect.side_effect = error
                self.assertFalse(canary.network_canary("127.0.0.1", 12345))
        with patch.object(canary.socket, "socket", side_effect=PermissionError(errno.EPERM, "denied")):
            self.assertTrue(canary.network_canary("127.0.0.1", 12345))
        self.assertFalse(canary.network_canary("not-an-ip", 12345))
        self.assertFalse(canary.network_canary(None, 12345))
        self.assertFalse(canary.network_canary("127.0.0.1", True))

    def test_connected_app_success_absence_or_errors_are_unqualified(self):
        self.assertFalse(canary.connected_app_canary(None))
        requests = []
        self.assertFalse(canary.connected_app_canary(lambda request: requests.append(request)))
        self.assertEqual(requests, [{"resource": "intentline-access-06-nonsecret-sentinel", "read_only": True}])
        def denied(request):
            raise PermissionError("unit-test policy simulation")
        def missing(request):
            raise KeyError("tool unavailable")
        self.assertTrue(canary.connected_app_canary(denied))
        self.assertFalse(canary.connected_app_canary(missing))
        self.assertFalse(canary.summary(True, [True], True, True)["host_qualified"])


if __name__ == "__main__":
    unittest.main()
