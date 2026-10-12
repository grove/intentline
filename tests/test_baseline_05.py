import os
from pathlib import Path
import unittest

from intentline.records import parse, sha


class Baseline05(unittest.TestCase):
    def test_frozen_04_source_and_historical_evidence_bytes(self):
        root = Path(__file__).resolve().parents[1]
        baseline = root / 'evaluation/baseline_05'
        identity = parse((baseline / 'identity.json').read_bytes())
        self.assertEqual(identity['commit'], '587ef061287f02d4d7328f7c291bf57b85892603')
        for name, digest in identity['files'].items():
            self.assertEqual(sha((baseline / name).read_bytes()), digest, name)
        for name, digest in identity['preserved'].items():
            self.assertEqual(sha((root / name).read_bytes()), digest, name)
        for name in identity['files']:
            if name.startswith(('schema/', 'skills/')):
                self.assertEqual((baseline / name).read_bytes(), (root / name).read_bytes(), name)

    def test_original_cli_render_and_portable_native_child_identities(self):
        from intentline.native_handoff import inspect_native
        from intentline.slice_export import inspect as inspect_child
        from intentline.render import markdown
        root = Path(__file__).resolve().parents[1] / 'evaluation/baseline_05/captures'
        for name, digest in parse((root / 'identity.json').read_bytes())['files'].items():
            self.assertEqual(sha((root / name).read_bytes()), digest, name)
        contract = parse((root / 'draft.json').read_bytes())
        manifest = parse((root / 'work/source-manifest.json').read_bytes())
        status = parse((root / 'status-result.json').read_bytes())['data']
        rendered = parse((root / 'render-result.json').read_bytes())['data']['markdown']
        self.assertEqual(markdown(contract, status, manifest), rendered)
        if os.name == 'posix':
            native = inspect_native(root / 'native')
            child = inspect_child(root / 'child')
            self.assertEqual(native['contract_sha256'], status['contract_sha256'])
            self.assertEqual(native['authorization'], 'not_established')
            self.assertEqual(child['child_acceptance'], 'not_established')
