import copy
import json
from unittest.mock import patch

from intentline.lore_adapter import inspect_report
from intentline.paths import MAX_FILE
from intentline.errors import IntentlineError
from intentline.records import canonical, sha
from intentline.sources import prepare
from tests.support import WorkCase


class LoreReport(WorkCase):
    def report(self):
        return {'schema_version':5,'snapshot':{'project_id':'project','registry_revision':'a'*64},
                'capabilities':{'inspection':'not_granted','execution':False,'source_write':False,'hosted_egress':False},
                'intelligence':{'schema_version':4,'mode':'fast_fallback','fallback_reason':'unavailable inference',
                                'omissions':{'critical_groups':1},'inspection_status':'static_only',
                                'constraints':[{'status':'accepted','scope':'production','statement':'Three retries'},
                                               {'status':'proposed','scope':'all','statement':'Unlimited retries'}]},
                'source_relationships':{'relations':[{'reason':'staging exception only','active':True,
                                                     'upstream_status':'accepted','revision':'original'}]},'budget':{}}

    def test_qualification_preserves_complete_bytes_and_no_peer_effects(self):
        if not self.setup_work():
            return
        path=self.root/'report.json';report=self.report();path.write_bytes(canonical(report));raw=path.read_bytes()
        with patch('subprocess.Popen',side_effect=AssertionError),patch('socket.socket',side_effect=AssertionError):
            result=inspect_report(path)
            prepare(str(self.source),[str(path)],str(self.root),str(self.root/'with-lore'))
        self.assertEqual(result['envelope'],'initialized_schema_5')
        self.assertEqual(result['reported_mode'],'fast_fallback')
        self.assertEqual(result['authority'],'candidate_leads_only')
        self.assertEqual(result['freshness'],'unverified')
        self.assertEqual((self.root/'with-lore/source/S2.txt').read_bytes(),raw)
        self.assertEqual(path.read_bytes(),raw)
        manifest=json.loads((self.root/'with-lore/source-manifest.json').read_bytes())
        self.assertEqual(manifest['sources'][1]['declared_authority'],'unverified_context')

    def test_bootstrap_unknown_incomplete_and_adverse_reports(self):
        if not self.setup_work():
            return
        path=self.root/'report.json'
        bootstrap={'contract':'lore.bootstrap_context','schema_version':1,'mode':'bootstrap_source_only',
                   'source_snapshot_sha256':'a'*64,'evidence':[],'discovery':{'truncated':True},
                   'omitted_source_groups':1,'budget':{}}
        path.write_bytes(canonical(bootstrap));self.assertEqual(inspect_report(path)['envelope'],'bootstrap_schema_1')
        for report in ({'schema_version':6}, {'schema_version':5}, {'schema_version':True}):
            path.write_bytes(canonical(report));self.assertEqual(inspect_report(path)['envelope'],'unrecognized')
        for adverse in ('accepted_vs_proposed','narrow_supersession','source_reversion_A_B_A',
                        'omitted_critical_relationship','deleted_document','stale_registry','static_inspection',
                        'missing_evidence_witness','prompt_injection'):
            report=self.report();report['intelligence']['warnings']=[adverse]
            if adverse == 'omitted_critical_relationship':
                report.pop('source_relationships')
            report['intelligence']['evidence']=[{'path':'missing.md','qualification':adverse}]
            path.write_bytes(canonical(report));before=path.read_bytes()
            result=inspect_report(path)
            self.assertEqual(result['authority'],'candidate_leads_only')
            self.assertEqual(result['report_sha256'],sha(before))
            self.assertEqual(path.read_bytes(),before)
            self.assertNotIn('constraints',result)  # no constraint generation/promotion

    def test_unsafe_paths_sizes_and_no_lore_normal_path(self):
        if not self.setup_work():
            return
        path=self.root/'oversized.json';path.write_bytes(b' '* (MAX_FILE+1))
        with self.assertRaises(IntentlineError):
            inspect_report(path)
        link=self.root/'link.json';link.symlink_to(self.source)
        with self.assertRaises(IntentlineError):
            inspect_report(link)
        # Normal prepare needs no report, binary, registry or environmental model credentials.
        self.assertTrue((self.work/'source-manifest.json').exists())
