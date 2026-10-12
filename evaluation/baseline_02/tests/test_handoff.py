import copy
from pathlib import Path
from unittest.mock import patch

from evaluation.handoff_02 import inspect_handoff, record_evidence
from intentline.contracts import propose
from intentline.errors import IntentlineError
from intentline.export import export
from intentline.paths import Directory
from intentline.records import canonical, sha
from intentline.sources import prepare
from tests.support import WorkCase


class Handoff(WorkCase):
    def test_complete_bundle_tampering_stale_and_unsupported_controls(self):
        if not self.setup_work():
            return
        propose(self.work,self.draft_path)
        out=self.root/'handoff'; export(self.work,'proofline-direct',out,self.root)
        with patch('subprocess.Popen',side_effect=AssertionError),patch('socket.socket',side_effect=AssertionError):
            result=inspect_handoff(out,self.work,self.root)
        self.assertEqual(result['criterion_ids'],['R1'])
        self.assertEqual(result['source_sha256'],sha(self.source.read_bytes()))
        self.assertEqual(result['live_delivery'],'not_observed')
        for name in ('source.md','brief.md','export-manifest.json','source-manifest.json','contract.json','source-S1.txt'):
            path=out/name; before=path.read_bytes();path.write_bytes(before+b'changed')
            with self.assertRaises(IntentlineError):
                inspect_handoff(out,self.work,self.root)
            path.write_bytes(before)
        with self.assertRaisesRegex(IntentlineError,'Unsupported'):
            inspect_handoff(out,self.work,self.root,shape='parent/prerequisite')
        self.source.write_bytes(b'Changed original promise')
        with self.assertRaisesRegex(IntentlineError,'Stale'):
            inspect_handoff(out,self.work,self.root)

    def test_downstream_context_race_blocks_completion(self):
        if not self.setup_work():
            return
        policy=self.root/'policy.md';policy.write_text('Keep existing behavior\n')
        downstream=self.root/'product';downstream.mkdir();(downstream/'policy.md').write_bytes(policy.read_bytes())
        work=self.root/'context-work';capture=prepare(str(self.source),[str(policy)],str(self.root),str(work))
        self.draft['source_bundle_sha256']=capture['source_bundle_sha256']
        self.draft['constraints']=[{'statement':'Keep existing behavior','basis':'project_constraint','scope':'Existing public behavior',
                                  'source_refs':[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Keep existing behavior'}]}]
        propose(work,self.write_draft(self.draft));out=self.root/'raced-export'
        write=Directory.write
        def race(directory,name,data,replace=False):
            result=write(directory,name,data,replace)
            if name == 'brief.md':
                (downstream/'policy.md').write_text('Different policy\n')
            return result
        with patch.object(Directory,'write',race),self.assertRaisesRegex(IntentlineError,'binding project reference'):
            export(work,'proofline-direct',out,downstream)
        self.assertFalse((out/'export-manifest.json').exists())

    def test_external_evidence_recorder_is_immutable_not_authenticated(self):
        if not self.setup_work():
            return
        evidence={'record':'intentline.handoff-evidence','schema_version':1,'state':'not_run',
                  'blockers':['No externally authorized spending or qualified native execution'],
                  'inspection':None,'external_records':[],'candidate_commit':None,'coverage':[],
                  'usage':{'cost':None,'tokens':None,'elapsed_seconds':None}}
        out=self.root/'evidence'
        first=record_evidence(evidence,self.root,out)
        self.assertEqual(first,record_evidence(evidence,self.root,out))
        self.assertEqual(first['authentication'],'unverified')
        bad=copy.deepcopy(evidence);bad['state']='completed'
        with self.assertRaises(IntentlineError):
            record_evidence(bad,self.root,out)

    def test_actual_pinned_clean_tracked_checkout_admission(self):
        if not self.setup_work():
            return
        import ast
        import json
        import shutil
        from tests.compatibility import proofline_checkout as pinned
        if shutil.which('git') is None:
            self.skipTest('Optional Git checkout qualification unavailable; no CLI dependency')
        code=Path(pinned.__file__).read_text()
        identity=json.loads((Path(pinned.__file__).parent/'checkout-identity.json').read_bytes())
        for node in ast.parse(code).body:
            if isinstance(node,ast.FunctionDef):
                self.assertEqual(sha(ast.get_source_segment(code,node).encode()),identity['functions'][node.name])
        product=self.root/'product';product.mkdir()
        (product/'entry.py').write_bytes(b'print("original")\n')
        (product/'policy.md').write_bytes(b'Keep existing behavior\n')
        (product/'request.md').write_bytes(self.source.read_bytes())
        pinned.host.git(product,'init','--quiet','--template=')
        pinned.host.git(product,'add','--all');pinned.host.git(product,'commit','--quiet','-m','Offline source')
        capture=prepare(str(product/'request.md'),[str(product/'policy.md')],str(product),str(self.root/'tracked-work'))
        self.draft['source_bundle_sha256']=capture['source_bundle_sha256']
        self.draft['constraints']=[{'statement':'Keep existing behavior','basis':'project_constraint','scope':'Existing behavior',
                                  'source_refs':[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Keep existing behavior'}]}]
        propose(self.root/'tracked-work',self.write_draft(self.draft))
        export(self.root/'tracked-work','proofline-direct',self.root/'tracked-handoff',product)
        inspect_handoff(self.root/'tracked-handoff',self.root/'tracked-work',product)
        before=pinned.git_bytes(product,'rev-parse','HEAD')
        source,base=pinned.capture_base(product,self.root/'frozen')
        self.assertEqual(source,before.decode().strip())
        self.assertEqual(pinned.git_bytes(product,'rev-parse','HEAD^{tree}'),
                         pinned.git_bytes(self.root/'frozen','rev-parse','HEAD^{tree}'))
        self.assertEqual((self.root/'frozen/policy.md').read_bytes(),(product/'policy.md').read_bytes())
        (product/'policy.md').write_text('Uncommitted changed policy')
        with self.assertRaisesRegex(pinned.InputGap,'local changes'):
            pinned.capture_base(product,self.root/'dirty')
        pinned.host.git(product,'add','--all');pinned.host.git(product,'commit','--quiet','-m','Retained change')
        (product/'external').symlink_to('../request.md')
        pinned.host.git(product,'add','--all');pinned.host.git(product,'commit','--quiet','-m','Hostile alias')
        unsafe_head=pinned.git_bytes(product,'rev-parse','HEAD')
        with self.assertRaisesRegex(pinned.InputGap,'Symlink'):
            pinned.capture_base(product,self.root/'unsafe')
        self.assertEqual(pinned.git_bytes(product,'rev-parse','HEAD'),unsafe_head)
