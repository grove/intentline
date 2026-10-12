import copy
import json
import os
from pathlib import Path
from unittest.mock import patch

from evaluation.slicing_04 import ARMS,DIMENSIONS,METRICS,assess,validate
from intentline.errors import IntentlineError
from intentline.export import export as export_parent
from intentline.records import canonical,sha,parse
from tests.test_slicing_coverage import CoverageCase


class SlicingEvaluation(CoverageCase):
    def fixture(self):
        # All identities/reviews/outputs here are authored development test data.
        def ref(name,value):
            raw=value.encode() if isinstance(value,str) else canonical(value)
            (self.root/name).write_bytes(raw);return {'path':name,'sha256':sha(raw)}
        out=self.root/'parent-payload';export_parent(self.work,'proofline-native',out)
        envelope=parse((out/'native-manifest.json').read_bytes())
        parent=ref('parent.json',{'envelope':envelope,'files_utf8':{n:(out/n).read_bytes().decode() for n in envelope['files']}})
        request=ref('request.txt',self.source.read_bytes().decode())
        task={'id':'authored-development','kind':'development','repository':'https://example.invalid/authored-fixture','commit':'a'*40,
              'license':'Apache-2.0','request':request,'context':[],'parent':parent,'scope':'Authored retry/validation boundaries',
              'author':'Fixture author','checker':'Fixture checker','reviews':[], 'reference':ref('gold.txt','PRIVATE AUTHOR-CONTEXT EXPECTATION'),'eligible':False}
        arms={a:{'model':None,'version':None,'reasoning':None,'seconds':None,'tools':[],'differences':[],
                 'instructions':ref(a+'.txt','Authored evaluation instruction')} for a in ARMS}
        assignments=[]
        for index,arm in enumerate(ARMS):
            output=ref(arm+'-output.txt','Authored NO SPLIT example')
            score=ref(arm+'-score.json',{'blind_id':str(index),'output_sha256':output['sha256'],'reviewer':'Authored fixture scorer',
                 'timestamp':'2026-10-12T13:00:00+00:00','blinded':True,'conflicts':[],
                 'dimensions':dict.fromkeys(DIMENSIONS,0),'citations':[{'source_sha256':request['sha256'],'source_lines':'1-2','output_ids':['R1','R2'],
                                                                         'dimension':d,'finding':'Authored mechanics only'} for d in DIMENSIONS]})
            assignments.append({'task':task['id'],'arm':arm,'state':'completed','blind_id':str(index),'inputs':[request,parent],
                                'output':output,'scores':[score],'metrics':dict.fromkeys(METRICS,None),
                                'provenance':[ref(arm+'-receipt.txt','Authored provenance; no authenticated reviewer or model run')]})
        study={'record':'intentline.slicing-study','schema_version':1,'phase':'development','registered_at':'2026-10-12T13:00:00+00:00',
               'arms':arms,'tasks':[task],'assignments':assignments,'blockers':[],'preparation':dict.fromkeys(METRICS,None)}
        study['registration']=ref('registration.json',{k:study[k] for k in ('phase','registered_at','arms','tasks')})
        return study

    def test_authored_development_is_not_empirical_and_read_only(self):
        if not self.setup_split():return
        study=self.fixture();before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch('subprocess.Popen',side_effect=AssertionError('exec')),patch('socket.socket',side_effect=AssertionError('network')):result=assess(study,self.root)
        self.assertEqual(result['eligible_tasks'],0);self.assertEqual(result['authentication'],'unverified')
        self.assertNotIn('PRIVATE',json.dumps(result));self.assertIsNone(result['arms']['ordinary']['adverse_counts'])
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        for state in ('failed','refused','timeout','interrupted','not_run'):
            changed=copy.deepcopy(study);changed['blockers']=['Authored unattempted state'];changed['assignments'][0].update(state=state,output=None,scores=[])
            self.assertEqual(assess(changed,self.root)['arms']['ordinary']['states'],{state:1})

    def test_parent_parity_private_gold_and_registration_refuse(self):
        if not self.setup_split():return
        study=self.fixture()
        for change in ('missing_parent','gold_input','missing_arm','parent_tamper','registration','development_eligible'):
            bad=copy.deepcopy(study)
            if change=='missing_parent':bad['assignments'][0]['inputs'].pop()
            if change=='gold_input':bad['assignments'][0]['inputs'].append(bad['tasks'][0]['reference'])
            if change=='missing_arm':bad['assignments'].pop()
            if change=='parent_tamper':bad['tasks'][0]['parent']['sha256']='0'*64
            if change=='registration':bad['registered_at']='2026-10-13T13:00:00+00:00'
            if change=='development_eligible':bad['tasks'][0]['eligible']=True
            if change!='registration':
                data=canonical({k:bad[k] for k in ('phase','registered_at','arms','tasks')});(self.root/'registration.json').write_bytes(data);bad['registration']['sha256']=sha(data)
            with self.subTest(change=change),self.assertRaises(IntentlineError):validate(bad,self.root)

    def test_dated_not_run_denominators_and_receipt_digests(self):
        root=Path(__file__).resolve().parents[1]/'evaluation'
        for name in ('slicing-04-not-run','slice-consumer-04-not-run'):
            data=(root/'results'/(name+'.json')).read_bytes()
            self.assertEqual(sha(data),(root/'results'/(name+'.sha256')).read_text().strip())
        if os.name!='posix':self.setup_work();return
        result=assess(parse((root/'results/slicing-04-not-run.json').read_bytes()),root)
        self.assertEqual(result['eligible_tasks'],0)
        self.assertTrue(all(a['assignments']==0 and a['usage']['cost'] is None for a in result['arms'].values()))
