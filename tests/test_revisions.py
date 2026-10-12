import copy

from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from tests.support import WorkCase


class Revisions(WorkCase):
    def test_noop_and_expected_before_identity(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        before = (self.work / 'current.json').read_bytes()
        propose(self.work, self.draft_path)
        self.assertEqual(before, (self.work / 'current.json').read_bytes())
        self.assertEqual(len(list((self.work / 'revisions').iterdir())), 1)
        new = self.revision(self.draft)
        new['advisory_notes'] = ['Alternative credible evidence methods are allowed']
        propose(self.work, self.write_draft(new))
        self.assertEqual(inspect(self.work)[1]['revision'], 2)
        self.assertEqual((self.work / 'revisions/000001.json').read_bytes(), before_contract(self.draft))
        bad = self.revision(new)
        bad['change_notes'][-1]['previous_contract_sha256'] = '0' * 64
        with self.assertRaises(IntentlineError):
            propose(self.work, self.write_draft(bad))

    def test_unexplained_deletion_and_retired_id_reuse(self):
        if not self.setup_work():
            return
        self.draft['requirements'].append({**copy.deepcopy(self.draft['requirements'][0]), 'id':'R2'})
        propose(self.work, self.write_draft(self.draft))
        new = self.revision(self.draft, [self.draft['requirements'][0]])
        with self.assertRaises(IntentlineError):
            propose(self.work, self.write_draft(new))
        note = new['change_notes'][-1]
        note['retired_ids'] = ['R2']
        note['mappings'] = [{'from':['R2'], 'to':['R1'], 'reason':'Remove duplicate obligation'}]
        propose(self.work, self.write_draft(new))
        another = self.revision(new, self.draft['requirements'])
        with self.assertRaisesRegex(IntentlineError, 'Retired'):
            propose(self.work, self.write_draft(another))

    def test_changed_row_needs_mapping_and_split_mapping(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        new = self.revision(self.draft)
        new['requirements'][0]['oracle'] = 'Requested validation error'
        with self.assertRaises(IntentlineError):
            propose(self.work, self.write_draft(new))
        new['change_notes'][-1]['mappings'] = [{'from':['R1'], 'to':['R1'], 'reason':'Clarify expected outcome'}]
        propose(self.work, self.write_draft(new))
        split = self.revision(new, [{**new['requirements'][0], 'id':'R2'}, {**new['requirements'][0], 'id':'R3'}])
        split['change_notes'][-1]['retired_ids'] = ['R1']
        split['change_notes'][-1]['mappings'] = [{'from':['R1'], 'to':['R2','R3'], 'reason':'Proposed split; semantic audit still needed'}]
        propose(self.work, self.write_draft(split))

    def test_recover_revision_without_pointer_and_reject_tamper(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        (self.work / 'current.json').unlink()
        propose(self.work, self.draft_path)
        self.assertEqual(inspect(self.work)[1]['revision'], 1)
        (self.work / 'revisions/000001.json').write_text('{}')
        with self.assertRaises(IntentlineError):
            inspect(self.work)


def before_contract(draft):
    from intentline.records import canonical
    return canonical(draft)
