import copy
import io
import json
import os
from pathlib import Path
from unittest.mock import patch

from intentline.cli import main
from intentline.contracts import propose
from intentline.continuity import reconcile
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical,sha
from intentline.slice_audits import audit_record
from intentline.slice_export import export,inspect
from intentline.slice_impact import impact
from intentline.slice_records import preview,record,status,subject
from tests.test_amendments import SuccessorCase
from tests.test_slicing_audits import report
from tests.test_slicing_coverage import CoverageCase,split_plan
from tests.test_slicing_nosplit import no_split


class SlicingIntegration(CoverageCase,SuccessorCase):
    def test_complete_manual_optional_flow_and_parent_unproven(self):
        if not self.setup_split():return
        split=copy.deepcopy(self.plan);self.plan=no_split(self.parent,self.draft['requirements'][0]['source_refs'])
        first=self.save_record();split['supersedes_sha256']=first['plan_sha256'];self.plan=split
        self.assertEqual(self.save_record()['status'],'SPLIT_PROPOSED')
        audit=report(self.plan);audit['actor']='PRIVATE SELF-CHECK IDENTITY';audit['coverage']='PRIVATE INTERNAL REVIEW TEXT'
        path=self.root/'private-audit.json';path.write_bytes(canonical(audit));audit_record(self.work,path)
        out=self.root/'child';export(self.work,'S1',out)
        for p in out.iterdir():
            self.assertNotIn(b'PRIVATE SELF-CHECK IDENTITY',p.read_bytes());self.assertNotIn(b'PRIVATE INTERNAL REVIEW TEXT',p.read_bytes())
        second,draft,mapping,dp,mp=self.successor();reconcile(second,dp,mp)
        self.assertEqual(impact(self.work,second)['authorization'],'not_transferred')
        with self.assertRaises(IntentlineError):preview(second,self.plan_path)
        with Directory(second) as directory:parent=subject(directory)[-1]
        new_plan=split_plan(parent,draft);path=self.root/'new-plan.json';path.write_bytes(canonical(new_plan))
        record(second,path,parent['contract_sha256']);second_out=self.root/'successor-child';export(second,'S2',second_out)
        self.assertEqual(inspect(second_out)['child_acceptance'],'not_established')
        self.assertEqual(status(second)['semantics'],'unverified')
        from intentline.contracts import inspect as inspect_parent
        self.assertNotIn('ADOPTED_ASSERTED',inspect_parent(second)[0]['flags'])

    def test_all_readonly_commands_zero_effect_and_deterministic_envelopes(self):
        if not self.setup_split():return
        self.save_record();out=self.root/'child';export(self.work,'S1',out)
        commands=[['preview','--work',str(self.work),'--proposal',str(self.plan_path)],
                  ['status','--work',str(self.work)],['render','--work',str(self.work)],
                  ['impact','--work',str(self.work),'--successor-work',str(self.work)],['inspect','--bundle',str(out)]]
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        original=os.open
        def reading(path,flags,*args,**kwargs):
            self.assertFalse(flags & (os.O_CREAT|os.O_WRONLY|os.O_RDWR|os.O_TRUNC))
            return original(path,flags,*args,**kwargs)
        with patch('os.open',reading),patch('os.supports_dir_fd',os.supports_dir_fd|{reading}),patch('subprocess.Popen',side_effect=AssertionError('spawn')),patch('socket.socket',side_effect=AssertionError('egress')):
            for command in commands:
                results=[]
                for args in (['--json','slice']+command,['slice']+command+['--json']):
                    with patch('sys.stdout',new_callable=io.StringIO) as stdout:
                        self.assertEqual(main(args),0);results.append(stdout.getvalue())
                self.assertEqual(*results)
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_record_and_audit_marker_races_restore_prior_publication(self):
        if not self.setup_split():return
        first=self.save_record();original=Directory.write
        self.plan['supersedes_sha256']=first['plan_sha256'];self.plan['rationale']['uncertainties']=['New review evidence']
        def race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name=='current.json' and directory.path.name=='slicing':self.source.write_bytes(b'Changed at publication')
            return result
        with patch.object(Directory,'write',race):
            with self.assertRaises(IntentlineError):self.save_record()
        self.source.write_bytes((self.work/'source/S1.txt').read_bytes());self.assertEqual(status(self.work)['plan_sha256'],first['plan_sha256'])
        self.plan=json.loads((self.work/'slicing'/(first['plan_sha256']+'.json')).read_bytes())
        audit=report(self.plan);path=self.root/'audit.json';path.write_bytes(canonical(audit))
        def audit_race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name=='index.json':self.source.write_bytes(b'Changed at audit publication')
            return result
        with patch.object(Directory,'write',audit_race):
            with self.assertRaises(IntentlineError):audit_record(self.work,path)
        self.source.write_bytes((self.work/'source/S1.txt').read_bytes());self.assertEqual(status(self.work)['audit_records'],0)

    def test_source_deletion_reintroduction_does_not_revive_plan(self):
        if not self.setup_split():return
        self.save_record();before=self.source.read_bytes();other=self.root/'replacement.md';other.write_bytes(before)
        self.source.unlink();other.rename(self.source)
        self.assertEqual(status(self.work)['status'],'STALE_PARENT')
        with self.assertRaises(IntentlineError):export(self.work,'S1',self.root/'stale-output')

    def test_windows_every_new_command_refuses_before_io(self):
        commands=[['preview','--work','C:/unsafe','--proposal','C:/proposal'],['record','--work','C:/unsafe','--proposal','C:/proposal','--expected-parent-sha256','0'*64],
                  ['status','--work','C:/unsafe'],['render','--work','C:/unsafe'],['audit-record','--work','C:/unsafe','--report','C:/report'],
                  ['impact','--work','C:/unsafe','--successor-work','C:/new'],['export','--work','C:/unsafe','--child','S1','--out','C:/out'],['inspect','--bundle','C:/bundle']]
        with patch('intentline.paths.os.name','nt'),patch('os.open',side_effect=AssertionError('filesystem I/O')),patch('sys.stderr',new_callable=io.StringIO),patch('sys.stdout',new_callable=io.StringIO):
            for command in commands:self.assertEqual(main(['--json','slice']+command),3)
