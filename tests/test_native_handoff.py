import copy
import os
import subprocess
import sys
from unittest.mock import patch

from intentline.adoption import adopt
from intentline.contracts import propose
from intentline.continuity import reconcile
from intentline.errors import IntentlineError
from intentline.export import export
from intentline.native_handoff import inspect_native
from intentline.paths import Directory
from intentline.records import canonical, parse, sha
from tests.test_adoption import approval
from tests.test_amendments import SuccessorCase


class NativeHandoff(SuccessorCase):
    def test_original_successor_standalone_and_private_provenance(self):
        if not self.setup_work(): return
        pointer = propose(self.work,self.draft_path)
        raw_approval = self.root/'approval.json';raw_approval.write_bytes(canonical(approval(pointer)))
        adopt(self.work,pointer['contract_sha256'],raw_approval)
        out = self.root/'original-native';export(self.work,'proofline-native',out)
        receipt=inspect_native(out)
        self.assertEqual(receipt['authorization'],'not_established')
        self.assertEqual(receipt['consumer_execution'],'not_observed')
        self.assertFalse(any(b'Synthetic test operator' in p.read_bytes() for p in out.iterdir() if p.is_file()))
        with patch('subprocess.Popen',side_effect=AssertionError('exec')),patch('socket.socket',side_effect=AssertionError('egress')):
            self.assertEqual(receipt,inspect_native(out))
        ran=subprocess.run([sys.executable,'-I','-B',str(out/'inspect_bundle.py'),str(out)],cwd=self.root,capture_output=True)
        self.assertEqual(ran.returncode,0,ran.stderr)
        self.assertEqual(parse(ran.stdout)['contract_sha256'],pointer['contract_sha256'])
        successor,draft,mapping,dp,mp=self.successor();reconcile(successor,dp,mp)
        second=self.root/'successor-native';export(successor,'proofline-native',second)
        self.assertEqual(inspect_native(second)['source_manifest']['schema_version'],2)
        self.assertEqual((second/'source-S2.txt').read_bytes(),b'Disable retries by default\r\n')
        with self.assertRaisesRegex(IntentlineError,'unsupported'):export(successor,'proofline-direct',self.root/'no-fallback')

    def test_tampering_inventory_and_rehashed_semantic_changes(self):
        if not self.setup_work(): return
        propose(self.work,self.draft_path)
        out=self.root/'native';export(self.work,'proofline-native',out)
        marker=parse((out/'native-manifest.json').read_bytes())
        for filename in ('source-S1.txt','brief.md','contract.json','history.json'):
            p=out/filename;before=p.read_bytes();p.write_bytes(before+b'changed')
            with self.assertRaises(IntentlineError):inspect_native(out)
            p.write_bytes(before)
        before=(out/'brief.md').read_bytes();(out/'brief.md').write_bytes(b'Forged summary\n')
        bad=copy.deepcopy(marker);bad['files']['brief.md']=sha(b'Forged summary\n');(out/'native-manifest.json').write_bytes(canonical(bad))
        with self.assertRaisesRegex(IntentlineError,'brief changed'):inspect_native(out)
        (out/'brief.md').write_bytes(before)
        for change in ('duplicate_filename','dropped_id','authority','missing_source'):
            bad=copy.deepcopy(marker)
            if change=='duplicate_filename':bad['files']['../source-S1.txt']=bad['files']['source-S1.txt']
            if change=='dropped_id':bad['requirement_ids']=[]
            if change=='authority':bad['authorization']='approved'
            if change=='missing_source':del bad['files']['source-S1.txt']
            (out/'native-manifest.json').write_bytes(canonical(bad))
            with self.assertRaises(IntentlineError):inspect_native(out)
        (out/'native-manifest.json').write_bytes(canonical(marker))
        source=out/'source-S1.txt';source.unlink();source.symlink_to(self.source)
        with self.assertRaises(IntentlineError):inspect_native(out)

    def test_interrupted_races_output_reuse_and_gaps(self):
        if not self.setup_work():return
        propose(self.work,self.draft_path)
        original=Directory.write
        def race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name=='brief.md':self.source.write_text('changed during export')
            return result
        out=self.root/'raced-native'
        with patch.object(Directory,'write',race):
            with self.assertRaisesRegex(IntentlineError,'changed before completion'):export(self.work,'proofline-native',out)
        self.assertFalse((out/'native-manifest.json').exists())
        self.source.write_bytes((self.work/'source/S1.txt').read_bytes())
        export(self.work,'proofline-native',self.root/'complete')
        export(self.work,'proofline-native',self.root/'complete')
        new=self.revision(self.draft);new['requirements'][0]['plan_state']='gap';new['evidence_gaps']=[{'requirement_ids':['R1'],'reason':'No observation harness'}]
        new['change_notes'][-1]['mappings']=[{'from':['R1'],'to':['R1'],'reason':'Disclose observation gap'}]
        propose(self.work,self.write_draft(new))
        with self.assertRaisesRegex(IntentlineError,'not ready'):export(self.work,'proofline-native',self.root/'unready')
        # Ordinary advisory exports remain usable for gaps.
        export(self.work,'proofline-direct',self.root/'advisory-gap')

    def test_product_context_race_and_stale_adoption(self):
        if not self.setup_work():return
        from intentline.sources import prepare
        policy=self.root/'policy.md';policy.write_bytes(b'Keep current policy\n')
        work=self.root/'policy-work';captured=prepare(self.source,[str(policy)],self.root,work)
        self.draft['source_bundle_sha256']=captured['source_bundle_sha256']
        self.draft['constraints']=[{'statement':'Keep policy','basis':'project_constraint','scope':'All usernames','source_refs':[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Keep current policy'}]}]
        pointer=propose(work,self.write_draft(self.draft))
        product=self.root/'product';product.mkdir();(product/'policy.md').write_bytes(policy.read_bytes())
        with self.assertRaisesRegex(IntentlineError,'product-root'):export(work,'proofline-native',self.root/'no-product')
        original=Directory.write
        def race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name=='brief.md':(product/'policy.md').write_text('changed downstream')
            return result
        with patch.object(Directory,'write',race):
            with self.assertRaisesRegex(IntentlineError,'binding project'):export(work,'proofline-native',self.root/'raced-context',product)
        self.assertFalse((self.root/'raced-context/native-manifest.json').exists())
        reference=self.root/'reference.json';reference.write_bytes(canonical(approval(pointer)));adopt(work,pointer['contract_sha256'],reference);reference.unlink()
        with self.assertRaisesRegex(IntentlineError,'not ready'):export(work,'proofline-native',self.root/'stale-adoption',product)

    def test_inspection_zero_writes_and_order_independent_file_map(self):
        if not self.setup_work(): return
        propose(self.work,self.draft_path)
        out=self.root/'readonly-native';export(self.work,'proofline-native',out)
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        original=os.open
        def reading(path,flags,*args,**kwargs):
            self.assertFalse(flags & (os.O_CREAT|os.O_WRONLY|os.O_RDWR|os.O_TRUNC))
            return original(path,flags,*args,**kwargs)
        with patch('os.open',reading),patch('os.supports_dir_fd',os.supports_dir_fd|{reading}),patch('subprocess.Popen',side_effect=AssertionError('exec')),patch('socket.socket',side_effect=AssertionError('egress')):
            first=inspect_native(out)
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        marker=parse((out/'native-manifest.json').read_bytes());marker['files']=dict(reversed(list(marker['files'].items())))
        (out/'native-manifest.json').write_bytes(canonical(marker))
        self.assertEqual(inspect_native(out),first)
