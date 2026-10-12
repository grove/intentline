import copy
import json

from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.records import canonical, parse
from intentline.render import markdown
from intentline.schemas import ACCEPTANCE
from tests.support import WorkCase


class Contracts(WorkCase):
    def test_valid_identity_and_renderer(self):
        if not self.setup_work():
            return
        result = propose(self.work, self.draft_path)
        status, c = inspect(self.work)
        self.assertEqual(status['status'], 'STRUCTURALLY_VALID')
        self.assertNotIn('ADOPTED_ASSERTED', status['flags'])
        self.assertEqual(status['contract_sha256'], result['contract_sha256'])
        self.assertEqual(markdown(c, status), markdown(c, status))
        self.assertIn('| R1 |', markdown(c, status))
        self.assertIn('planned', markdown(c, status))

    def test_strict_schema_negative_controls(self):
        if not self.setup_work():
            return
        bad = []
        for key, value in [('schema_version', True), ('revision', 1.0), ('source_bundle_sha256', 'abc'),
                           ('requirements', []), ('approved', True), ('contract_id', '../escape')]:
            draft = copy.deepcopy(self.draft)
            draft[key] = value
            bad.append(draft)
        for key, value in [('id', 'R0'), ('plan_state', 'passed'), ('basis','advice'), ('oracle', ''), ('result','proven')]:
            draft = copy.deepcopy(self.draft)
            draft['requirements'][0][key] = value
            bad.append(draft)
        duplicate = copy.deepcopy(self.draft)
        duplicate['requirements'] *= 2
        bad.append(duplicate)
        for draft in bad:
            with self.subTest(draft=draft):
                with self.assertRaises(IntentlineError):
                    propose(self.work, self.write_draft(draft))
        self.assertFalse((self.work / 'current.json').exists())

    def test_exact_quotes_and_supported_basis(self):
        if not self.setup_work():
            return
        for key, value in [('quote','Reject empty'), ('line_end',99), ('source_id','S2')]:
            draft = copy.deepcopy(self.draft)
            draft['requirements'][0]['source_refs'][0][key] = value
            with self.assertRaises(IntentlineError):
                propose(self.work, self.write_draft(draft))
        draft = copy.deepcopy(self.draft)
        draft['requirements'][0]['basis'] = 'project_constraint'
        with self.assertRaises(IntentlineError):
            propose(self.work, self.write_draft(draft))
        draft['requirements'][0]['basis'] = 'necessary_invariant'
        propose(self.work, self.write_draft(draft))

    def test_gap_and_decision_are_distinct(self):
        if not self.setup_work():
            return
        self.draft['requirements'][0]['plan_state'] = 'gap'
        with self.assertRaises(IntentlineError):
            propose(self.work, self.write_draft(self.draft))
        self.draft['evidence_gaps'] = [{'requirement_ids':['R1'], 'reason':'No runtime harness supplied'}]
        propose(self.work, self.write_draft(self.draft))
        self.assertEqual(inspect(self.work)[0]['status'], 'STRUCTURALLY_VALID')
        next_draft = self.revision(self.draft)
        next_draft['open_decisions'] = [{'id':'D1', 'statement':'Which error message?', 'kind':'outcome',
                                       'source_refs':self.draft['requirements'][0]['source_refs']}]
        propose(self.work, self.write_draft(next_draft))
        self.assertEqual(inspect(self.work)[0]['status'], 'BLOCKED')

    def test_duplicate_keys_nonfinite_json_and_schema_inventory(self):
        for data in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'{}garbage'):
            with self.assertRaises(IntentlineError):
                parse(data)
        from pathlib import Path
        schema = json.loads((Path(__file__).resolve().parents[1] / 'schema/acceptance-v1.schema.json').read_text())
        schema.pop('$schema')
        self.assertEqual(schema, ACCEPTANCE)

    def test_stale_sources_are_not_fresh_snapshots(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        self.source.unlink()
        status, c = inspect(self.work)
        self.assertEqual(status['status'], 'STALE')
        self.assertEqual(status['exit_code'], 2)
        self.assertIsNotNone(c)
        with self.assertRaisesRegex(IntentlineError, 'STALE'):
            propose(self.work, self.draft_path)
