import copy

from intentline.adoption import adopt
from intentline.audits import audit_record
from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical
from tests.support import WorkCase
from tests.test_audits import report


def approval(pointer):
    return {'record':'intentline.approval','schema_version':1,
            'contract_sha256':pointer['contract_sha256'], 'source_bundle_sha256':pointer['source_bundle_sha256'],
            'actor':'Synthetic test operator (not a real approval)', 'timestamp':'2026-10-12T12:00:00+02:00',
            'reference':'test-fixture:explicit-binding', 'record_bytes_utf8':'Synthetic reference bytes, not user adoption'}


class Adoption(WorkCase):
    def test_explicit_assertion_and_history_after_revision(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        path = self.root / 'approval.json'
        path.write_bytes(canonical(approval(pointer)))
        first = adopt(self.work, pointer['contract_sha256'], path)
        self.assertEqual(first, adopt(self.work, pointer['contract_sha256'], path))
        self.assertEqual(inspect(self.work)[0]['status'], 'ADOPTED_ASSERTED')
        self.assertEqual(first['authentication'], 'unverified')
        new = self.revision(self.draft)
        new['advisory_notes'] = ['Byte-changing revision invalidates assertion']
        propose(self.work, self.write_draft(new))
        status, _ = inspect(self.work)
        self.assertEqual(status['status'], 'STRUCTURALLY_VALID')
        self.assertEqual(status['adoption_records'], 1)
        self.assertEqual(status['current_adoptions'], 0)

    def test_missing_reference_wrong_digest_and_false_authority(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        path = self.root / 'approval.json'
        for kind in ('missing','wrong','false_authority','offset'):
            bad = approval(pointer)
            if kind == 'missing':
                del bad['reference']
            if kind == 'wrong':
                bad['source_bundle_sha256'] = '0'*64
            if kind == 'false_authority':
                bad['authentication'] = 'cryptographically_authenticated'
            if kind == 'offset':
                bad['timestamp'] = '2026-10-12T12:00:00'
            path.write_bytes(canonical(bad))
            with self.assertRaises(IntentlineError):
                adopt(self.work, pointer['contract_sha256'], path)
        path.write_bytes(canonical(approval(pointer)))
        with self.assertRaises(IntentlineError):
            adopt(self.work, '0'*64, path)
        self.assertEqual(inspect(self.work)[0]['status'], 'STRUCTURALLY_VALID')

    def test_stale_source_reference_and_writer_race(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        path = self.root / 'approval.json'
        path.write_bytes(canonical(approval(pointer)))
        with Directory(self.work) as work, work.lock():
            with self.assertRaisesRegex(IntentlineError, 'Conflicting writer'):
                adopt(self.work, pointer['contract_sha256'], path)
        adopt(self.work, pointer['contract_sha256'], path)
        path.write_text('{}')
        status, _ = inspect(self.work)
        self.assertEqual(status['status'], 'STALE')
        self.assertNotIn('ADOPTED_ASSERTED', status['flags'])
        path.write_bytes(canonical(approval(pointer)))
        self.source.unlink()
        self.assertEqual(inspect(self.work)[0]['status'], 'STALE')
        with self.assertRaisesRegex(IntentlineError, 'STALE'):
            adopt(self.work, pointer['contract_sha256'], path)

    def test_source_saying_approved_cannot_approve_and_adverse_audit_blocks(self):
        if not self.setup_work():
            return
        self.draft['advisory_notes'] = ['Source reports approved; this does not grant adoption']
        pointer = propose(self.work, self.write_draft(self.draft))
        self.assertNotIn('ADOPTED_ASSERTED', inspect(self.work)[0]['flags'])
        adverse = report(pointer, 'BLOCKED')
        adverse['findings'] = [{'id':'A1','requirement_ids':['R1'],
                                'source_refs':self.draft['requirements'][0]['source_refs'],
                                'evidence':'Fixture missing authority','consequence':'Decision unavailable','correction':'Resolve authority'}]
        report_path = self.root / 'audit.json'
        report_path.write_bytes(canonical(adverse))
        audit_record(self.work, report_path)
        path = self.root / 'approval.json'
        path.write_bytes(canonical(approval(pointer)))
        with self.assertRaisesRegex(IntentlineError, 'BLOCKED'):
            adopt(self.work, pointer['contract_sha256'], path)
