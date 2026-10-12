import copy

from intentline.audits import audit_record
from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.records import canonical
from tests.support import WorkCase


def report(pointer, outcome='READY_FOR_ADOPTION'):
    return {'record':'intentline.audit', 'schema_version':1, 'contract_sha256':pointer['contract_sha256'],
            'source_bundle_sha256':pointer['source_bundle_sha256'], 'actor':'Synthetic fixture reviewer',
            'timestamp':'2026-10-12T12:00:00+02:00', 'reported_independence':'self_check',
            'authentication':'unverified', 'outcome':outcome,
            'coverage':'Authored deterministic fixture only; no independent review', 'findings':[]}


class Audits(WorkCase):
    def test_record_idempotence_and_unverified_self_check(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        path = self.root / 'audit.json'
        path.write_bytes(canonical(report(pointer)))
        first = audit_record(self.work, path)
        self.assertEqual(first, audit_record(self.work, path))
        status, _ = inspect(self.work)
        self.assertEqual(status['status'], 'READY_FOR_ADOPTION')
        self.assertEqual(status['authentication'], 'unverified')
        self.assertEqual(status['audit_records'], 1)
        self.assertNotIn('ADOPTED_ASSERTED', status['flags'])

    def test_mismatches_fake_authentication_stale_and_outdated(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        path = self.root / 'audit.json'
        for key, value in [('contract_sha256','0'*64),('source_bundle_sha256','0'*64),
                           ('authentication','authenticated'),('timestamp','2026-10-12')]:
            bad = report(pointer)
            bad[key] = value
            path.write_bytes(canonical(bad))
            with self.assertRaises(IntentlineError):
                audit_record(self.work, path)
        path.write_bytes(canonical(report(pointer)))
        new = self.revision(self.draft)
        new['advisory_notes'] = ['New draft']
        propose(self.work, self.write_draft(new))
        with self.assertRaises(IntentlineError):
            audit_record(self.work, path)
        self.source.write_text('changed')
        with self.assertRaisesRegex(IntentlineError, 'STALE'):
            audit_record(self.work, path)

    def test_conflicting_reports_conservatively_block(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        path = self.root / 'audit.json'
        path.write_bytes(canonical(report(pointer)))
        audit_record(self.work, path)
        adverse = report(pointer, 'CHANGES_NEEDED')
        adverse['findings'] = [{'id':'A1','requirement_ids':['R1'],
                                'source_refs':self.draft['requirements'][0]['source_refs'],
                                'evidence':'Fixture review disagreement', 'consequence':'Acceptance disputed',
                                'correction':'Resolve in a new draft'}]
        path.write_bytes(canonical(adverse))
        audit_record(self.work, path)
        self.assertEqual(inspect(self.work)[0]['status'], 'BLOCKED')
        bad = copy.deepcopy(adverse)
        bad['outcome'] = 'READY_FOR_ADOPTION'
        path.write_bytes(canonical(bad))
        with self.assertRaises(IntentlineError):
            audit_record(self.work, path)
