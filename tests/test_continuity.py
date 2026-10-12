import copy

from intentline.amendments import amend_source
from intentline.contracts import propose
from intentline.continuity import reconcile
from intentline.errors import IntentlineError
from intentline.records import canonical, sha
from tests.test_amendments import SuccessorCase


class Continuity(SuccessorCase):
    def test_retired_ancestor_ids_cannot_return(self):
        if not self.setup_work(): return
        self.draft['requirements'].append({**copy.deepcopy(self.draft['requirements'][0]), 'id': 'R2'})
        propose(self.work, self.write_draft(self.draft))
        retired = self.revision(self.draft, [self.draft['requirements'][0]])
        retired['change_notes'][-1].update(retired_ids=['R2'], mappings=[{'from':['R2'], 'to':[], 'reason':'Retire duplicate'}])
        propose(self.work, self.write_draft(retired))
        out, draft, mapping, dp, mp = self.successor(self.work, retired)
        draft['requirements'].append({**copy.deepcopy(draft['requirements'][0]), 'id':'R2'})
        mapping['added_requirement_ids'] = ['R2']; mapping['contract_sha256'] = sha(canonical(draft))
        dp.write_bytes(canonical(draft)); mp.write_bytes(canonical(mapping))
        with self.assertRaisesRegex(IntentlineError, 'Retired ancestor'): reconcile(out, dp, mp)

    def test_ancillary_obligations_cannot_disappear(self):
        if not self.setup_work(): return
        self.draft['out_of_scope'] = [{'statement':'Keep valid usernames unchanged', 'source_refs':[{'source_id':'S1','line_start':2,'line_end':2,'quote':'Keep valid usernames unchanged'}]}]
        propose(self.work, self.write_draft(self.draft))
        out, draft, mapping, dp, mp = self.successor()
        draft['out_of_scope'] = []; mapping['contract_sha256'] = sha(canonical(draft));dp.write_bytes(canonical(draft));mp.write_bytes(canonical(mapping))
        with self.assertRaisesRegex(IntentlineError, 'Inherited'): reconcile(out, dp, mp)
        mapping['other_changes'] = [{'category':'out_of_scope','from_index':1,'to_indices':[], 'reason':'Caller amendment proposes retirement', 'source_refs':[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Disable retries by default'}]}]
        mp.write_bytes(canonical(mapping)); reconcile(out, dp, mp)
