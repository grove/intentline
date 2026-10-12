import copy
import json
import os
from pathlib import Path
import tempfile
import unittest

from intentline.errors import IntentlineError
from intentline.records import canonical, sha
from intentline.sources import prepare


class WorkCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'request.md'
        self.source.write_bytes(b'Reject empty and whitespace-only usernames\r\nKeep valid usernames unchanged\n')
        self.work = self.root / 'work'
        self.draft_path = self.root / 'draft.json'

    def setup_work(self):
        if os.name != 'posix':
            with self.assertRaises(IntentlineError) as error:
                prepare(str(self.source), [], str(self.root), str(self.work))
            self.assertEqual(error.exception.code, 3)
            return False
        result = prepare(str(self.source), [], str(self.root), str(self.work))
        self.draft = {'contract': 'intentline.acceptance', 'schema_version': 1,
                      'contract_id': 'username-validation', 'revision': 1,
                      'source_bundle_sha256': result['source_bundle_sha256'],
                      'intended_outcome': 'Reject empty and whitespace-only usernames',
                      'requirements': [{'id': 'R1', 'statement': 'Reject empty and whitespace-only usernames',
                                        'basis': 'request', 'source_refs': [{'source_id':'S1', 'line_start':1, 'line_end':1,
                                                                         'quote':'Reject empty and whitespace-only usernames'}],
                                        'boundaries': ['empty', 'spaces', 'tabs'], 'seam': 'public validation interface',
                                        'oracle': 'validation error for empty/whitespace-only usernames',
                                        'planned_evidence': 'call interface with empty, spaces, and tabs', 'plan_state':'planned'}],
                      'constraints': [], 'out_of_scope': [], 'open_decisions': [], 'evidence_gaps': [],
                      'change_notes': [{'revision':1, 'kind':'initial'}]}
        self.write_draft(self.draft)
        return True

    def write_draft(self, draft):
        self.draft_path.write_bytes(canonical(draft))
        return self.draft_path

    def revision(self, prior, replacements=None):
        new = copy.deepcopy(prior)
        new['revision'] += 1
        if replacements is not None:
            new['requirements'] = replacements
        new['change_notes'].append({'revision':new['revision'], 'kind':'revision', 'reason':'Operator revision proposal',
                                    'previous_contract_sha256':sha(canonical(prior)),
                                    'mappings':[], 'retired_ids':[], 'claimed_authority':'Unadopted operator proposal'})
        return new
