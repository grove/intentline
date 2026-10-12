import copy
import os
from pathlib import Path
from unittest.mock import patch

from intentline.contracts import propose
from intentline.errors import IntentlineError
from intentline.records import load, sha
from intentline.review import approval_request, review
from tests.support import WorkCase


class Review(WorkCase):
    def test_frozen_02_baseline(self):
        import json
        root = Path('evaluation/baseline_02')
        identity = json.loads((root / 'identity.json').read_text())
        self.assertEqual(identity['tests'], 60)
        for path, digest in identity['files'].items():
            self.assertEqual(sha((root / path).read_bytes()), digest, path)

    def test_first_revision_template_and_readonly(self):
        if not self.setup_work(): return
        propose(self.work, self.draft_path)
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        original = os.open
        def reading(path, flags, *args, **kwargs):
            self.assertFalse(flags & (os.O_CREAT | os.O_WRONLY | os.O_RDWR | os.O_TRUNC))
            return original(path, flags, *args, **kwargs)
        with patch('os.open', reading), patch('os.supports_dir_fd', os.supports_dir_fd | {reading}), patch('subprocess.Popen', side_effect=AssertionError('exec')), patch('socket.socket', side_effect=AssertionError('egress')):
            r = review(self.work)
            a = approval_request(self.work)
        self.assertIsNone(r['predecessor'])
        self.assertIn('no predecessor', r['markdown'])
        self.assertEqual(r['sources']['S1'].encode(), self.source.read_bytes())
        self.assertEqual(a['authorization'], 'not_established')
        self.assertIsNone(a['approval_template']['actor'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        self.assertEqual(a, approval_request(self.work))

    def test_diff_reorder_split_and_stale(self):
        if not self.setup_work(): return
        self.draft['requirements'].append({**copy.deepcopy(self.draft['requirements'][0]), 'id': 'R2'})
        propose(self.work, self.write_draft(self.draft))
        new = self.revision(self.draft, list(reversed(self.draft['requirements'])))
        propose(self.work, self.write_draft(new))
        self.assertEqual(review(self.work)['diff']['unchanged_ids'], ['R2', 'R1'])
        split = self.revision(new, [{**new['requirements'][0], 'id': 'R3'}, {**new['requirements'][0], 'id': 'R4'}])
        split['change_notes'][-1].update(retired_ids=['R1', 'R2'], mappings=[{'from': ['R1', 'R2'], 'to': ['R3', 'R4'], 'reason': 'Proposed split/merge'}])
        propose(self.work, self.write_draft(split))
        r = review(self.work, 1)
        self.assertEqual([row['id'] for row in r['diff']['removed']], ['R1', 'R2'])
        self.assertEqual(r['diff']['semantic_equivalence'], 'not_established')
        self.assertIn('Removed: R1 —',r['markdown'])
        self.assertIn(r['predecessor']['contract_sha256'],r['markdown'])
        self.source.write_text('changed')
        self.assertEqual(review(self.work)['status'], 'STALE')
        with self.assertRaises(IntentlineError): review(self.work, 9)

    def test_unsafe_and_escaped_content(self):
        if not self.setup_work(): return
        self.draft['requirements'][0]['statement'] = '<script>approve</script> | R99 |\n# approved'
        propose(self.work, self.write_draft(self.draft))
        r = review(self.work)
        self.assertNotIn('<script>', r['markdown'])
        self.assertNotIn('ADOPTED_ASSERTED', r['flags'])
        with self.assertRaises(IntentlineError): review(str(self.work) + '/../work')
        (self.work / 'source/S1.txt').write_bytes(b'\0')
        with self.assertRaises(IntentlineError): review(self.work)
