"""Authored citation/record mechanics, not model behavior or runtime efficacy."""
import copy
import json
import os
from pathlib import Path

from intentline.contracts import inspect, propose
from intentline.records import canonical, sha
from intentline.sources import prepare
from tests.support import WorkCase


class OriginalSourceProbes(WorkCase):
    def test_authored_original_support_and_provisional_records(self):
        root = Path(__file__).resolve().parents[1]
        probes = json.loads((root / 'evaluation/original-source-probes.json').read_bytes())['probes']
        self.assertEqual([p['id'] for p in probes], ['44-report', '44-exception', '44-unavailable'])
        for probe in probes:
            self.assertEqual(sha(probe['request'].encode()), probe['request_sha256'])
            self.assertEqual(sha(probe['context'].encode()), probe['context_sha256'])
            for kind in ('before', 'after'):
                self.assertEqual(sha(canonical(probe[kind])), probe[kind + '_template_sha256'])
        if os.name != 'posix':
            self.setup_work()  # Assert storage fails closed on unsupported platforms.
            return
        for probe in probes:
            case = self.root / probe['id']
            case.mkdir()
            source = case / 'request.md'
            source.write_text(probe['request'], encoding='utf-8')
            policy = case / 'policy.md'
            policy.write_text(probe['context'], encoding='utf-8')
            for kind in ('before', 'after'):
                with self.subTest(probe=probe['id'], kind=kind):
                    work = case / kind
                    captured = prepare(str(source), [str(policy)], str(case), str(work))
                    draft = copy.deepcopy(probe[kind])
                    draft['source_bundle_sha256'] = captured['source_bundle_sha256']
                    propose(work, self.write_draft(draft))
                    expected = probe.get('after_status', 'STRUCTURALLY_VALID') if kind == 'after' else 'STRUCTURALLY_VALID'
                    self.assertEqual(inspect(work)[0]['status'], expected)
                    # Semantically adverse drafts pass structural validation too.
                    self.assertEqual(inspect(work)[0]['audit_records'], 0)
