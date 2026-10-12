import copy
from unittest.mock import patch

from intentline.contracts import propose
from intentline.continuity import reconcile
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical,sha
from intentline.slice_impact import impact
from intentline.slice_records import preview,status
from tests.test_amendments import SuccessorCase
from tests.test_slicing_coverage import CoverageCase


class SliceImpact(CoverageCase,SuccessorCase):
    def test_same_source_revision_and_all_dependency_rechecks(self):
        if not self.setup_split():return
        self.save_record();new=self.revision(self.draft);new['requirements'][0]['planned_evidence']='Observe a separate public entry point'
        new['change_notes'][-1]['mappings']=[{'from':['R1'],'to':['R1'],'reason':'New evidence path'}]
        propose(self.work,self.write_draft(new))
        with patch.object(Directory,'write',side_effect=AssertionError('write')),patch('subprocess.Popen',side_effect=AssertionError('spawn')),patch('socket.socket',side_effect=AssertionError('network')):
            data=impact(self.work,self.work)
        self.assertEqual(data['status'],'IMPACT_REVIEW_REQUIRED');self.assertEqual(data['potentially_affected_children'],['S1','S2'])
        self.assertEqual(data['unchanged_candidate_ids'],['R2']);self.assertEqual(status(self.work)['status'],'STALE_PARENT')
        with self.assertRaises(IntentlineError):preview(self.work,self.plan_path)

    def test_transitive_successors_and_reversion_never_reuse(self):
        if not self.setup_split():return
        self.save_record()
        second,draft,mapping,dp,mp=self.successor();reconcile(second,dp,mp)
        third,d3,m3,d3p,m3p=self.successor(second,draft);reconcile(third,d3p,m3p)
        with patch.object(Directory,'write',side_effect=AssertionError('write')):data=impact(self.work,third)
        self.assertEqual(len(data['lineage_mappings']),2);self.assertEqual(data['authorization'],'not_transferred')
        self.assertEqual(status(third)['status'],'NO_PLAN')
        self.assertNotEqual(data['prior_parent']['source_chain_sha256'],data['successor_parent']['source_chain_sha256'])
        with self.assertRaises(IntentlineError):preview(third,self.plan_path)
        # Matching original R text in two later generations never imports old allocation.
        self.assertEqual(d3['requirements'],self.draft['requirements'])

    def test_unrelated_lineage_and_missing_ancestor_refuse(self):
        if not self.setup_split():return
        self.save_record()
        from intentline.sources import prepare
        unrelated=self.root/'unrelated';capture=prepare(self.source,[],self.root,unrelated)
        other=copy.deepcopy(self.draft);other['contract_id']='unrelated';other['source_bundle_sha256']=capture['source_bundle_sha256'];propose(unrelated,self.write_draft(other))
        with self.assertRaisesRegex(IntentlineError,'continuity'):impact(self.work,unrelated)
        second,draft,mapping,dp,mp=self.successor();reconcile(second,dp,mp)
        archive=second/'archive';next(p for p in archive.iterdir() if p.suffix=='.json').unlink()
        with self.assertRaises((IntentlineError,OSError)):impact(self.work,second)
