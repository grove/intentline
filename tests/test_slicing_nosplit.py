import copy
import io
import json
import os
from pathlib import Path
from unittest.mock import patch

from intentline.cli import main
from intentline.contracts import propose
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical, sha
from intentline.slice_records import preview, record, status, subject
from tests.support import WorkCase


def no_split(parent, refs):
    return {'record':'intentline.slicing','schema_version':1,'parent':parent,'decision':'no_split',
            'rationale':{'why_not_one_delivery':'One coherent public validation outcome fits direct delivery',
                         'why_these_boundaries':'No independently useful delivery boundary',
                         'basis':'advisory_plan_not_proof','source_refs':refs,
                         'uncertainties':[],'next_action':'Continue with the complete parent agreement'},
            'children':[],'allocations':[],'prerequisites':[],'parent_final_checks':[], 'supersedes_sha256':None}


class SliceCase(WorkCase):
    def setup_slice(self):
        if not self.setup_work(): return False
        self.pointer=propose(self.work,self.draft_path)
        with Directory(self.work) as work: self.parent=subject(work)[-1]
        self.plan=no_split(self.parent,self.draft['requirements'][0]['source_refs'])
        self.plan_path=self.root/'slice.json';self.save_plan()
        return True

    def save_plan(self):
        self.plan_path.write_bytes(canonical(self.plan))
        return self.plan_path

    def save_record(self):
        return record(self.work,self.save_plan(),self.parent['contract_sha256'])


class NoSplit(SliceCase):
    def test_full_path_idempotence_and_no_effect_inspection(self):
        if not self.setup_slice(): return
        self.assertEqual(status(self.work)['status'],'NO_PLAN')
        self.assertFalse((self.work/'slicing').exists())
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(Directory,'write',side_effect=AssertionError('write')),patch('subprocess.Popen',side_effect=AssertionError('spawn')),patch('socket.socket',side_effect=AssertionError('network')):
            self.assertEqual(preview(self.work,self.plan_path)['status'],'NO_SPLIT')
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        first=self.save_record();self.assertEqual(first,self.save_record())
        self.assertEqual(status(self.work)['history_count'],1)
        self.assertFalse((self.work/'slicing/children').exists())
        self.assertEqual((self.work/'current.json').read_bytes(),canonical({k:self.pointer[k] for k in ('contract_id','revision','contract_sha256','source_bundle_sha256')}))
        with patch.object(Directory,'write',side_effect=AssertionError('write')):
            self.assertIn('NO_SPLIT',status(self.work,True)['markdown'])

    def test_stale_revision_source_and_expected_before(self):
        if not self.setup_slice(): return
        self.save_record()
        with self.assertRaisesRegex(IntentlineError,'Expected parent'):record(self.work,self.plan_path,'0'*64)
        old=self.source.read_bytes();self.source.write_bytes(old+b'changed')
        self.assertEqual(status(self.work)['status'],'STALE_PARENT')
        with self.assertRaisesRegex(IntentlineError,'STALE_PARENT'):self.save_record()
        self.source.write_bytes(old)
        new=self.revision(self.draft);propose(self.work,self.write_draft(new))
        self.assertEqual(status(self.work)['status'],'STALE_PARENT')
        with self.assertRaisesRegex(IntentlineError,'identity'):preview(self.work,self.plan_path)

    def test_strict_input_and_explicit_replacement(self):
        if not self.setup_slice(): return
        first=self.save_record()
        self.plan['rationale']['uncertainties']=['New documentary uncertainty']
        with self.assertRaisesRegex(IntentlineError,'supersedes'):self.save_record()
        self.plan['supersedes_sha256']=first['plan_sha256'];self.save_record()
        self.assertEqual(status(self.work)['history_count'],2)
        original=self.plan_path.read_bytes()
        for raw in (original.replace(b'"record":',b'"record":"x","record":'),json.dumps(self.plan).encode()):
            self.plan_path.write_bytes(raw)
            with self.assertRaises(IntentlineError):preview(self.work,self.plan_path)
        self.save_plan()
        for key,value in (('approval',True),('children',[{}])):
            mutant=copy.deepcopy(self.plan);mutant[key]=value;self.plan_path.write_bytes(canonical(mutant))
            with self.assertRaises(IntentlineError):preview(self.work,self.plan_path)
        self.save_plan();self.plan['rationale']['next_action']='x\u202ey';self.save_plan()
        with self.assertRaisesRegex(IntentlineError,'Unicode'):preview(self.work,self.plan_path)

    def test_unsafe_files_and_corrupt_history(self):
        if not self.setup_slice(): return
        saved=self.save_record();path=self.work/'slicing'/(saved['plan_sha256']+'.json')
        original=path.read_bytes();path.write_bytes(original+b' ')
        with self.assertRaises(IntentlineError):status(self.work)
        path.write_bytes(original)
        alias=self.root/'linked.json';os.link(self.plan_path,alias)
        with self.assertRaises(IntentlineError):preview(self.work,alias)
        alias.unlink();alias.symlink_to(self.plan_path)
        with self.assertRaises(IntentlineError):preview(self.work,alias)
        alias.unlink();os.mkfifo(alias)
        with self.assertRaises(IntentlineError):preview(self.work,alias)

    def test_interruption_race_and_writer_conflict(self):
        if not self.setup_slice(): return
        original=Directory.write
        def interrupt(directory,name,data,replace=False):
            if name=='current.json' and directory.path.name=='slicing':raise KeyboardInterrupt()
            return original(directory,name,data,replace)
        with patch.object(Directory,'write',interrupt):
            with self.assertRaises(KeyboardInterrupt):self.save_record()
        self.assertEqual(status(self.work)['status'],'NO_PLAN')
        self.save_record()
        with Directory(self.work) as work, work.lock():
            with self.assertRaisesRegex(IntentlineError,'writer'):self.save_record()
        self.plan['supersedes_sha256']=sha(canonical(self.plan));self.plan['rationale']['uncertainties']=['New evidence']
        def race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name.endswith('.json') and name!='current.json' and directory.path.name=='slicing':self.source.write_bytes(b'changed')
            return result
        with patch.object(Directory,'write',race):
            with self.assertRaisesRegex(IntentlineError,'STALE_PARENT'):self.save_record()
        self.assertEqual(status(self.work)['history_count'],1)

    def test_cli_json_positions_and_windows_no_io(self):
        if not self.setup_slice(): return
        for argv in (['--json','slice','preview'],['slice','--json','preview'],['slice','preview','--json']):
            with patch('sys.stdout',new_callable=io.StringIO) as output:
                self.assertEqual(main(argv+['--work',str(self.work),'--proposal',str(self.plan_path)]),0)
                self.assertEqual(json.loads(output.getvalue())['result'],'intentline.result')
        with patch('intentline.paths.os.name','nt'),patch('os.open',side_effect=AssertionError('I/O')),patch('sys.stderr',new_callable=io.StringIO),patch('sys.stdout',new_callable=io.StringIO):
            self.assertEqual(main(['slice','status','--work',str(self.work),'--json']),3)
