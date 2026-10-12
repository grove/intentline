"""Whole offline lifecycle; approvals/reviews are synthetic test assertions."""
import copy
import importlib.util
from pathlib import Path

from intentline.adoption import adopt
from intentline.audits import audit_record
from intentline.continuity import reconcile
from intentline.contracts import inspect, propose
from intentline.export import export
from intentline.errors import IntentlineError
from intentline.native_handoff import inspect_native
from intentline.records import canonical, parse, sha
from intentline.review import approval_request, review
from tests.test_adoption import approval
from tests.test_amendments import SuccessorCase
from tests.test_audits import report


class Integration03(SuccessorCase):
    def consumer(self):
        root=Path(__file__).parent/'compatibility'
        identity=parse((root/'native-identity.json').read_bytes())
        path=root/'proofline_native_input.py';self.assertEqual(sha(path.read_bytes()),identity['file_sha256'])
        spec=importlib.util.spec_from_file_location('pinned_native_consumer',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_complete_external_assertion_successor_dispute_native_admission(self):
        if not self.setup_work():return
        pointer=propose(self.work,self.draft_path)
        self.assertIsNone(review(self.work)['predecessor'])
        assertion=self.root/'external-assertion.json';assertion.write_bytes(canonical(approval(pointer)));adopt(self.work,pointer['contract_sha256'],assertion)
        successor,draft,mapping,dp,mp=self.successor();pointer=reconcile(successor,dp,mp)
        r=review(successor);self.assertEqual(r['current_adoptions'],0);self.assertEqual(r['source_states'][0]['support'],'frozen_historical')
        self.assertEqual(approval_request(successor)['authorization'],'not_established')
        adverse=report(pointer,'CHANGES_NEEDED');adverse['findings']=[{'id':'A1','requirement_ids':['R1'],'source_refs':draft['requirements'][0]['source_refs'],'evidence':'Authored semantic-dispute fixture','consequence':'Agreement disputed','correction':'New exact proposal required'}]
        audit=self.root/'audit.json';audit.write_bytes(canonical(adverse));audit_record(successor,audit)
        with self.assertRaises(IntentlineError):export(successor,'proofline-native',self.root/'blocked-export')
        corrected=self.revision(draft);corrected['advisory_notes']=['Authored dispute resolution fixture; not an independent review']
        pointer=propose(successor,self.write_draft(corrected));assertion=self.root/'successor-assertion.json';assertion.write_bytes(canonical(approval(pointer)));adopt(successor,pointer['contract_sha256'],assertion)
        out=self.root/'native';export(successor,'proofline-native',out);inspection=inspect_native(out)
        consumer=self.consumer();metadata,source,brief=consumer.inspect_intentline(out)
        self.assertIn('not a verbatim single request',source);self.assertEqual(consumer.inspect_bundle(out)['bundle_sha256'],inspection['bundle_sha256'])
        request={'path':out,'contract_sha256':pointer['contract_sha256'],'source_chain_sha256':metadata['source_chain_sha256'],'bundle_sha256':metadata['bundle_sha256'],'approval_reference':'Synthetic trusted-caller test; no actual adoption'}
        consumer.adopted_intentline(**request)
        with self.assertRaises(ValueError):consumer.adopted_intentline(**{**request,'approval_reference':None})
        (out/'source-S2.txt').write_text('changed amendment')
        with self.assertRaises((ValueError,OSError)):consumer.adopted_intentline(**request)
        self.assertEqual(inspect(successor)[0]['authentication'],'unverified')

    def test_new_current_amendment_reversion_does_not_reuse_predecessor_adoption(self):
        if not self.setup_work():return
        pointer=propose(self.work,self.draft_path);assertion=self.root/'old-adoption.json';assertion.write_bytes(canonical(approval(pointer)));adopt(self.work,pointer['contract_sha256'],assertion)
        successor,draft,mapping,dp,mp=self.successor();pointer=reconcile(successor,dp,mp)
        amendment=self.root/'amend-username-validation.md';exact=amendment.read_bytes();amendment.write_text('Changed current amendment')
        self.assertEqual(review(successor)['status'],'STALE')
        amendment.write_bytes(exact)
        self.assertNotIn('ADOPTED_ASSERTED',review(successor)['flags'])
        with self.assertRaisesRegex(IntentlineError,'mismatch'):adopt(successor,pointer['contract_sha256'],assertion)

    def test_changed_source_map_and_noncanonical_complete_marker_refuse(self):
        if not self.setup_work():return
        propose(self.work,self.draft_path);successor,draft,mapping,dp,mp=self.successor();reconcile(successor,dp,mp)
        marker=successor/'successor-complete.json';original=marker.read_bytes();bad=parse(original);bad['schema_version']=True;marker.write_bytes(canonical(bad))
        with self.assertRaises(IntentlineError):inspect(successor)
        marker.write_bytes(original)
        out=self.root/'native';export(successor,'proofline-native',out)
        manifest=parse((out/'source-manifest.json').read_bytes());manifest['sources'][0]['predecessor_source_id']='S99'
        raw=canonical(manifest);(out/'source-manifest.json').write_bytes(raw)
        with self.assertRaises(IntentlineError):inspect_native(out)

    def test_context_refresh_can_disclose_evidence_gap_without_inventing_user_amendment(self):
        if not self.setup_work():return
        from intentline.sources import prepare
        policy=self.root/'policy.md';policy.write_bytes(b'Observation harness available\n')
        work=self.root/'documentary-work';captured=prepare(self.source,[str(policy)],self.root,work)
        self.draft['source_bundle_sha256']=captured['source_bundle_sha256'];propose(work,self.write_draft(self.draft))
        policy.write_bytes(b'Observation harness unavailable\n')
        successor,draft,mapping,dp,mp=self.successor(work,self.draft,True,[str(policy)])
        draft['requirements'][0]['plan_state']='gap';draft['requirements'][0]['planned_evidence']='Await the public observation harness'
        draft['evidence_gaps']=[{'requirement_ids':['R1'],'reason':'Current documentary context says the harness is unavailable'}]
        mapping['contract_sha256']=sha(canonical(draft));dp.write_bytes(canonical(draft));mp.write_bytes(canonical(mapping))
        reconcile(successor,dp,mp)
        self.assertFalse(review(successor)['contract']['open_decisions'])
        self.assertEqual(review(successor)['continuity']['mappings'][0]['disposition'],'preserved')
        with self.assertRaises(IntentlineError):export(successor,'proofline-native',self.root/'gap-native')
        draft['requirements'][0]['statement']='Accept empty usernames';mapping['contract_sha256']=sha(canonical(draft))
        from intentline.continuity import continuity_check
        from intentline.paths import Directory
        from intentline.sources import bundle
        from intentline.amendments import archives
        with Directory(successor) as directory:
            manifest,blobs,_=bundle(directory);predecessor,_=archives(directory,manifest)
            with self.assertRaisesRegex(IntentlineError,'unchanged binding fields'):
                continuity_check(mapping,predecessor['history'][-1],draft,manifest,blobs,predecessor['manifest'])

    def test_external_not_run_and_host_self_check_receipts(self):
        import os
        import json
        from evaluation.planning_02 import assess
        root=Path(__file__).resolve().parents[1]/'evaluation'
        host=parse((root/'results/host-03-smoke.json').read_bytes())
        self.assertIn('self-context/unblinded',host['qualification']);self.assertEqual(host['actual_adoptions'],0)
        self.assertEqual(host['extra_model_processes_spawned'],0)
        for path,digest in host['files'].items():self.assertEqual(sha((root/'host_03'/path).read_bytes()),digest)
        if os.name == 'posix':
            study=json.loads((root/'results/planning-03-not-run.json').read_bytes());result=assess(study,root)
            self.assertEqual(result['eligible_tasks'],0)
            for arm in result['arms'].values():
                self.assertEqual(arm['assignments'],0);self.assertIsNone(arm['usage']['cost'])
