import copy
import os
import subprocess
import sys
from unittest.mock import patch

from intentline.continuity import reconcile
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical,parse,sha
from intentline.slice_export import export,inspect
from intentline.slice_records import record,subject
from tests.test_amendments import SuccessorCase
from tests.test_slicing_coverage import CoverageCase,split_plan


class SliceExport(CoverageCase,SuccessorCase):
    def test_portable_full_parent_and_no_private_reports_or_native_admission(self):
        if not self.setup_split():return
        self.save_record();out=self.root/'child';first=export(self.work,'S1',out)
        self.assertEqual(first,export(self.work,'S1',out))
        self.assertEqual(first['child_view']['constraints'],self.draft['constraints'])
        self.assertEqual(first['child_view']['out_of_scope'],self.draft['out_of_scope'])
        self.assertEqual(first['child_view']['qualified_criterion_ids'],['S1:C1'])
        self.assertFalse(any((out/name).exists() for name in ('source.md','brief.md','native-manifest.json')))
        with patch('subprocess.Popen',side_effect=AssertionError('exec')),patch('socket.socket',side_effect=AssertionError('egress')),patch.object(Directory,'write',side_effect=AssertionError('write')):
            self.assertEqual(inspect(out)['child_acceptance'],'not_established')
        result=subprocess.run([sys.executable,'-I','-B',str(out/'inspect_child.py'),str(out)],cwd=self.root,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(parse(result.stdout),inspect(out))
        from tests.compatibility.proofline_native_input import inspect_intentline
        with self.assertRaises((ValueError,OSError)):inspect_intentline(out)
        from tests.compatibility.proofline_direct_parser import criterion_ids,InputGap
        with self.assertRaises(InputGap):criterion_ids((out/'child.json').read_text())

    def test_successor_archives_and_advisory_evidence_gap(self):
        if not self.setup_split():return
        self.save_record();second,draft,mapping,dp,mp=self.successor();reconcile(second,dp,mp)
        with Directory(second) as directory:parent=subject(directory)[-1]
        plan=split_plan(parent,draft);plan['children'][0]['requirements'][0].update(plan_state='gap',gap_reason='Public observation not yet available')
        path=self.root/'next-slice.json';path.write_bytes(canonical(plan));record(second,path,parent['contract_sha256'])
        out=self.root/'successor-child';export(second,'S2',out)
        self.assertTrue(any(p.name.startswith('archive-') for p in out.iterdir()))
        self.assertEqual(inspect(out)['parent']['source_chain_sha256'],parent['source_chain_sha256'])
        archive=next(p for p in out.iterdir() if p.name.startswith('archive-') and p.suffix=='.json');archive.unlink()
        with self.assertRaises(IntentlineError):inspect(out)

    def test_tamper_rehashed_lost_exclusion_and_extra_files_refuse(self):
        if not self.setup_split():return
        self.save_record();out=self.root/'tamper';export(self.work,'S1',out)
        marker=parse((out/'slice-manifest.json').read_bytes());child=(out/'child.json').read_bytes()
        for name in ('source-S1.txt','plan.json','contract.json','child.json','history.json'):
            path=out/name;before=path.read_bytes();path.write_bytes(before+b'changed')
            with self.assertRaises(IntentlineError):inspect(out)
            path.write_bytes(before)
        view=parse(child);view['out_of_scope']=[];(out/'child.json').write_bytes(canonical(view))
        bad=copy.deepcopy(marker);bad['files']['child.json']=sha(canonical(view));(out/'slice-manifest.json').write_bytes(canonical(bad))
        with self.assertRaisesRegex(IntentlineError,'exclusions'):inspect(out)
        (out/'child.json').write_bytes(child);(out/'slice-manifest.json').write_bytes(canonical(marker))
        extra=out/'unrelated.txt';extra.write_bytes(b'extra')
        with self.assertRaises(IntentlineError):inspect(out)
        extra.unlink()
        for key,value in (('authorization','approved'),('child_acceptance','accepted'),('child_id','S99')):
            bad=copy.deepcopy(marker);bad[key]=value;(out/'slice-manifest.json').write_bytes(canonical(bad))
            with self.assertRaises(IntentlineError):inspect(out)
        bad=copy.deepcopy(marker);bad['files']['../escape']=sha(b'');(out/'slice-manifest.json').write_bytes(canonical(bad))
        with self.assertRaises(IntentlineError):inspect(out)

    def test_partial_source_race_unsafe_output_and_hardlinks(self):
        if not self.setup_split():return
        self.save_record();original=Directory.write;out=self.root/'partial'
        def race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name=='child.json':self.source.write_bytes(b'changed during export')
            return result
        with patch.object(Directory,'write',race):
            with self.assertRaises(IntentlineError):export(self.work,'S1',out)
        self.assertFalse((out/'slice-manifest.json').exists())
        with self.assertRaises(IntentlineError):inspect(out)
        self.source.write_bytes((self.work/'source/S1.txt').read_bytes())
        export(self.work,'S1',out)
        alias=self.root/'alias';os.link(out/'child.json',alias)
        with self.assertRaises(IntentlineError):inspect(out)
        alias.unlink()
        with self.assertRaises(IntentlineError):export(self.work,'S99',self.root/'unknown')
        self.assertFalse((self.root/'unknown').exists())
        with self.assertRaises(IntentlineError):export(self.work,'S1',self.work/'unsafe')

    def test_source_change_during_marker_removes_aborted_marker(self):
        if not self.setup_split():return
        self.save_record();original=Directory.write;out=self.root/'marker-race'
        def race(directory,name,data,replace=False):
            result=original(directory,name,data,replace)
            if name=='slice-manifest.json':self.source.write_bytes(b'Changed while marker published')
            return result
        with patch.object(Directory,'write',race):
            with self.assertRaises(IntentlineError):export(self.work,'S1',out)
        self.assertFalse((out/'slice-manifest.json').exists())
        with self.assertRaises(IntentlineError):inspect(out)
