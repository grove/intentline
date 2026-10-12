import copy
import json
import os
from pathlib import Path

from intentline.audits import audit_record
from intentline.contracts import inspect, propose
from intentline.records import canonical, sha
from intentline.sources import prepare
from tests.support import WorkCase


class SemanticProbes(WorkCase):
    def test_bound_adverse_and_corrected_authored_probes(self):
        probes=json.loads((Path(__file__).resolve().parents[1]/'evaluation/semantic-probes.json').read_bytes())['probes']
        for probe in probes:
            self.assertEqual(sha(probe['request'].encode()),probe['request_sha256'])
            for kind in ('before','after'):
                self.assertEqual(sha(canonical(probe[kind])),probe[kind+'_template_sha256'])
        if os.name != 'posix':
            self.setup_work()
            return
        for probe in probes:
            with self.subTest(probe=probe['id']):
                root=self.root/probe['id']; root.mkdir()
                source=root/'request.md'; source.write_text(probe['request'])
                contexts=[]
                if probe['context']:
                    policy=root/'policy.md'; policy.write_text(probe['context']); contexts=[str(policy)]
                    self.assertEqual(sha(policy.read_bytes()),probe['context_sha256'])
                for kind in ('before','after'):
                    work=root/kind
                    captured=prepare(str(source),contexts,str(root),str(work))
                    draft=copy.deepcopy(probe[kind]); draft['source_bundle_sha256']=captured['source_bundle_sha256']
                    pointer=propose(work,self.write_draft(draft))
                    if kind == 'before':
                        report={'record':'intentline.audit','schema_version':1,
                                'contract_sha256':pointer['contract_sha256'],
                                'source_bundle_sha256':pointer['source_bundle_sha256'],
                                'actor':'synthetic probe checker','timestamp':'2026-10-12T00:00:00+00:00',
                                'reported_independence':'self_check','authentication':'unverified',
                                'outcome':'CHANGES_NEEDED','coverage':'Authored probe only, not independent semantic evaluation',
                                'findings':[{'id':'A1','requirement_ids':['R1'],
                                             'source_refs':draft['requirements'][0]['source_refs'],
                                             'evidence':probe['finding'],'consequence':'Source promise is inadequately planned',
                                             'correction':probe['correction']}]}
                        path=root/'audit.json';path.write_bytes(canonical(report));audit_record(work,path)
                        self.assertEqual(inspect(work)[0]['status'],'BLOCKED')
                    else:
                        self.assertEqual(inspect(work)[0]['status'],'STRUCTURALLY_VALID')
                        self.assertEqual(inspect(work)[0]['audit_records'],0)
