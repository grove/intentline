from pathlib import Path

from intentline.adoption import adopt
from intentline.audits import audit_record
from intentline.continuity import reconcile
from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.records import canonical
from intentline.review import approval_request, review
from tests.test_adoption import approval
from tests.test_amendments import SuccessorCase
from tests.test_audits import report


class SuccessorAdoption(SuccessorCase):
    def test_old_assertions_never_adopt_successor_and_disputes_block(self):
        if not self.setup_work(): return
        prior = propose(self.work, self.draft_path)
        old_approval = self.root / 'old-approval.json'; old_approval.write_bytes(canonical(approval(prior)))
        adopt(self.work, prior['contract_sha256'], old_approval)
        out, draft, mapping, dp, mp = self.successor()
        pointer = reconcile(out, dp, mp)
        with self.assertRaisesRegex(IntentlineError, 'mismatch'): adopt(out, pointer['contract_sha256'], old_approval)
        self.assertEqual(review(out)['current_adoptions'], 0)
        self.assertIsNone(approval_request(out)['approval_template']['reference'])
        audit = self.root / 'audit.json'; audit.write_bytes(canonical(report(pointer)))
        audit_record(out, audit)
        adverse = report(pointer, 'CHANGES_NEEDED')
        adverse['findings'] = [{'id':'A1','requirement_ids':['R1'],'source_refs':draft['requirements'][0]['source_refs'],
                                'evidence':'Authored mechanical fixture: semantic preservation still disputed',
                                'consequence':'Agreement disputed', 'correction':'Resolve in a new draft'}]
        audit.write_bytes(canonical(adverse)); audit_record(out, audit)
        r = review(out); self.assertEqual(r['status'], 'BLOCKED');self.assertEqual(len(r['audit_disputes']), 1)
        self.assertIn('Agreement disputed', r['markdown'])
        new_approval = self.root / 'new-approval.json';new_approval.write_bytes(canonical(approval(pointer)))
        with self.assertRaisesRegex(IntentlineError, 'BLOCKED'): adopt(out, pointer['contract_sha256'], new_approval)
        new = self.revision(draft);new['advisory_notes']=['New exact proposal resolves authored fixture, no real review claim']
        pointer = propose(out, self.write_draft(new));new_approval.write_bytes(canonical(approval(pointer)))
        adopted = adopt(out, pointer['contract_sha256'], new_approval)
        self.assertEqual(adopted['authentication'], 'unverified')
        old_approval.unlink()
        self.assertEqual(inspect(out)[0]['status'], 'ADOPTED_ASSERTED')
        new_approval.unlink()
        self.assertEqual(inspect(out)[0]['status'], 'STALE')

    def test_installed_skill_contract_and_malicious_host_limits(self):
        root = Path(__file__).resolve().parents[1]
        plan = ' '.join((root/'skills/intentline-plan/SKILL.md').read_text().split())
        audit = ' '.join((root/'skills/intentline-audit/SKILL.md').read_text().split())
        for phrase in ('amend-source', 'reconcile', 'exact chat bytes', 'No automatic adopt', 'retired ID'):
            self.assertIn(phrase, plan)
        for phrase in ('both directions', 'full source', 'self_check', 'Never manufacture approval'):
            self.assertIn(phrase, audit)
