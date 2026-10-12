import os
from pathlib import Path
import unittest

from intentline.records import parse, sha


class Readiness05(unittest.TestCase):
    def test_distinct_sanitized_receipts_and_known_missing_evidence(self):
        root = Path(__file__).resolve().parents[1] / 'evaluation/results'
        for name in ('planning-05-not-run', 'slicing-05-not-run', 'intake-05-readiness',
                     'intake-05-receipt', 'proofline-consumer-05', 'proofline-native-05-not-run'):
            raw = (root / (name + '.json')).read_bytes()
            self.assertEqual(sha(raw), (root / (name + '.sha256')).read_text().strip(), name)
        readiness = parse((root / 'intake-05-readiness.json').read_bytes())
        self.assertEqual(readiness['candidate_count'], 9)
        self.assertEqual(readiness['project_count'], 3)
        self.assertEqual(readiness['eligible_count'], 0)
        self.assertEqual(readiness['registered_assignments'], 0)
        self.assertEqual(readiness['executed'], 0)
        self.assertTrue(all(readiness[k] == 'missing' for k in ('model_authorization', 'host_isolation', 'blinding_ready', 'cost_permission')))
        consumer = parse((root / 'proofline-consumer-05.json').read_bytes())
        snapshot = parse((Path(__file__).parent / 'compatibility/native-identity.json').read_bytes())
        self.assertEqual(consumer['files']['checks/intentline_input.py'], snapshot['file_sha256'])
        self.assertEqual(consumer['native_live_gate'], 'blocked_trust_gate')
        self.assertEqual(consumer['intentline_native_runs'], 0)

    def test_existing_evaluators_keep_new_not_run_measures_unknown(self):
        if os.name != 'posix':
            return  # Actual Windows refusal is covered by the CLI/storage and intake tests.
        from evaluation import planning_02, slicing_04
        root = Path(__file__).resolve().parents[1] / 'evaluation'
        for module, name in ((planning_02, 'planning'), (slicing_04, 'slicing')):
            study = parse((root / ('results/' + name + '-05-not-run.json')).read_bytes())
            result = module.assess(study, root)
            self.assertEqual(result['eligible_tasks'], 0)
            self.assertFalse(result['pilot_minimum_met'])
            for arm in result['arms'].values():
                self.assertEqual(arm['assignments'], 0)
                self.assertIsNone(arm['adverse_counts'])
                self.assertIsNone(arm['clean_fraction'])
                self.assertTrue(all(value is None for value in arm['usage'].values()))
