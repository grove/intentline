import copy
from unittest.mock import patch

from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical,sha
from intentline.slice_audits import audit_record
from intentline.slice_records import status
from tests.test_slicing_coverage import CoverageCase


def report(plan,outcome='NO_MATERIAL_FINDINGS'):
    return {'record':'intentline.slice-audit','schema_version':1,
            'contract_sha256':plan['parent']['contract_sha256'],'source_bundle_sha256':plan['parent']['source_bundle_sha256'],
            'plan_sha256':sha(canonical(plan)),'actor':'Authored development self-check',
            'timestamp':'2026-10-12T13:00:00+00:00','reported_independence':'self_check',
            'authentication':'unverified','outcome':outcome,'coverage':'Authored structural and semantic probe; no independent reviewer',
            'findings':[] if outcome=='NO_MATERIAL_FINDINGS' else [{'id':'A1','requirement_ids':['R1'],
                'source_refs':copy.deepcopy(plan['rationale']['source_refs']),
                'evidence':'Two username variations do not independently justify delivery boundaries',
                'consequence':'An extra verification cycle without benefit','correction':'Use NO SPLIT for the coherent validation outcome'}]}


class SliceAudits(CoverageCase):
    def test_optional_disagreements_favorable_does_not_erase(self):
        if not self.setup_split():return
        self.save_record();path=self.root/'audit.json';adverse=report(self.plan,'CHANGES_NEEDED');path.write_bytes(canonical(adverse))
        first=audit_record(self.work,path);self.assertEqual(first,audit_record(self.work,path))
        path.write_bytes(canonical(report(self.plan)));audit_record(self.work,path)
        data=status(self.work);self.assertEqual(data['status'],'BLOCKED');self.assertEqual(len(data['audit_disputes']),1)
        self.assertEqual(data['current_audits'],2)
        self.plan['supersedes_sha256']=sha(canonical(self.plan));self.plan['rationale']['uncertainties']=['Reassess disputed boundary with new exact evidence'];self.save_record()
        self.assertEqual(len(status(self.work)['historical_disputes']),1)

    def test_binding_validation_and_read_only_status(self):
        if not self.setup_split():return
        self.save_record();path=self.root/'audit.json';good=report(self.plan,'CHANGES_NEEDED')
        for key,value in (('authentication','verified'),('plan_sha256','0'*64),('timestamp','no offset'),('findings',[])):
            bad=copy.deepcopy(good);bad[key]=value;path.write_bytes(canonical(bad))
            with self.assertRaises(IntentlineError):audit_record(self.work,path)
        path.write_bytes(canonical(good));audit_record(self.work,path)
        with patch.object(Directory,'write',side_effect=AssertionError('write')),patch('subprocess.Popen',side_effect=AssertionError('spawn')),patch('socket.socket',side_effect=AssertionError('network')):
            self.assertEqual(status(self.work)['status'],'BLOCKED')
        record_path=self.work/'slicing/audits'/(sha(canonical(good))+'.json');record_path.write_bytes(canonical(good)+b' ')
        with self.assertRaises(IntentlineError):status(self.work)

    def test_interruption_before_index_does_not_publish(self):
        if not self.setup_split():return
        self.save_record();path=self.root/'audit.json';path.write_bytes(canonical(report(self.plan)))
        original=Directory.write
        def interrupt(directory,name,data,replace=False):
            if name=='index.json':raise KeyboardInterrupt()
            return original(directory,name,data,replace)
        with patch.object(Directory,'write',interrupt):
            with self.assertRaises(KeyboardInterrupt):audit_record(self.work,path)
        self.assertEqual(status(self.work)['audit_records'],0)
        audit_record(self.work,path);self.assertEqual(status(self.work)['audit_records'],1)
