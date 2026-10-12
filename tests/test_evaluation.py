import copy
import contextlib
import io
import json
import os
from pathlib import Path
from unittest.mock import patch

from evaluation.planning_02 import ARMS, DIMENSIONS, METRICS, assess, interval, main, validate
from intentline.cli import main as cli
from intentline.contracts import contract_check
from intentline.errors import IntentlineError
from intentline.records import canonical, sha
from intentline.render import markdown
from tests.support import WorkCase


class Evaluation(WorkCase):
    def fixture(self):
        def ref(name, data):
            raw = data.encode() if isinstance(data, str) else canonical(data)
            (self.root / name).write_bytes(raw)
            return {'path': name, 'sha256': sha(raw)}
        request = ref('original.txt', 'Preserve existing retries\n')
        reference = ref('gold.txt', 'Private expected result')
        task = {'id': 't1', 'kind': 'real', 'repository': 'https://example.invalid/project',
                'commit': 'a'*40, 'license': 'Apache-2.0', 'request': request, 'context': [],
                'scope': 'Retry configuration', 'author': 'author', 'checker': 'checker',
                'reviews': [{'actor': actor, 'timestamp': '2026-10-12T00:00:00Z', 'conflicts': [],
                             'corrections': [], 'record': ref(actor+'.txt', 'Declared review')}
                            for actor in ('r1', 'r2')], 'reference': reference, 'eligible': True}
        arms = {a: {'model': None, 'version': None, 'reasoning': None, 'seconds': None,
                    'tools': [], 'differences': [], 'instructions': ref(a+'.txt', 'Plan acceptance')} for a in ARMS}
        runs=[]
        for i, a in enumerate(ARMS):
            output = ref(a+'-output.txt', 'R1 preserve retries')
            scores=[]
            for reviewer in ('s1', 's2'):
                scores.append(ref(a+reviewer+'.json', {'blind_id': str(i), 'output_sha256': output['sha256'],
                    'reviewer': reviewer, 'timestamp': '2026-10-12T00:00:00Z', 'blinded': True,
                    'conflicts': [], 'dimensions': dict.fromkeys(DIMENSIONS, 0),
                    'citations': [{'source_sha256': request['sha256'], 'source_lines':'1', 'output_ids':['R1'],
                                   'dimension':d, 'finding':'Covered'} for d in DIMENSIONS]}))
            runs.append({'task':'t1','arm':a,'state':'completed','blind_id':str(i), 'inputs':[request],
                         'output':output, 'scores':scores, 'metrics':dict.fromkeys(METRICS, None),
                         'provenance':[ref(a+'-run.txt','Synthetic mechanics only')]})
        study = {'record':'intentline.planning-study', 'schema_version':1, 'phase':'pilot',
                'registered_at':'2026-10-12T00:00:00Z','registration':ref('registration.txt','Synthetic mechanics only'),
                'arms':arms,'tasks':[task], 'assignments':runs,'blockers':[], 'preparation':dict.fromkeys(METRICS,None)}
        study['registration'] = ref('registration.txt', {k: study[k] for k in ('phase','registered_at','arms','tasks')})
        return study

    def test_frozen_baseline_bytes_render_and_envelope(self):
        root=Path(__file__).resolve().parents[1]/'evaluation/baseline'
        identity=json.loads((root/'identity.json').read_bytes())
        for name,digest in identity['files'].items():
            self.assertEqual(sha((root/name).read_bytes()),digest)
        c=json.loads((root/'contract.json').read_bytes())
        m=json.loads((root/'source-manifest.json').read_bytes())
        contract_check(c,m,{'S1':(root/'source.txt').read_bytes()},c['source_bundle_sha256'])
        status={'status':'STRUCTURALLY_VALID','contract_sha256':sha(canonical(c))}
        self.assertEqual(markdown(c,status,m).encode(),(root/'render.md').read_bytes())
        out=io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli(['--json','status']),2)
        self.assertEqual(json.loads(out.getvalue()),json.loads((root/'negative.json').read_bytes()))

    def test_bound_blinded_assessment_is_read_only_and_private(self):
        if os.name != 'posix':
            self.setup_work()
            return
        study=self.fixture()
        before={p.name:p.read_bytes() for p in self.root.iterdir()}
        with patch('subprocess.Popen',side_effect=AssertionError),patch('socket.socket',side_effect=AssertionError):
            result=assess(study,self.root)
        self.assertEqual(result['eligible_tasks'],1)  # synthetic test, never committed empirical results
        self.assertFalse(result['pilot_minimum_met'])
        self.assertEqual(result['authentication'],'unverified')
        self.assertIsNone(result['arms']['ordinary']['usage']['tokens'])
        self.assertNotIn('Private expected result',json.dumps(result))
        self.assertNotIn('author',json.dumps(result))
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})

    def test_negative_controls(self):
        if os.name != 'posix':
            self.setup_work()
            return
        original=self.fixture()
        mutations=[lambda s:s['tasks'][0].update(commit='abc'),
                   lambda s:s['tasks'][0].update(kind='development'),
                   lambda s:s['tasks'][0].update(checker='author'),
                   lambda s:s['tasks'][0]['reviews'][0].update(actor='checker'),
                   lambda s:s['assignments'].pop(),
                   lambda s:s['assignments'][0].update(inputs=[s['tasks'][0]['reference']]),
                   lambda s:s['assignments'][0]['metrics'].pop('tokens'),
                   lambda s:s['assignments'][0]['output'].update(sha256='0'*64),
                   lambda s:s['tasks'][0]['request'].update(path='../escape'),
                   lambda s:s['assignments'][0].update(state='not_run')]
        for mutate in mutations:
            study=copy.deepcopy(original); mutate(study)
            registration=canonical({k:study[k] for k in ('phase','registered_at','arms','tasks')})
            (self.root/'registration.txt').write_bytes(registration)
            study['registration']['sha256']=sha(registration)
            with self.assertRaises(IntentlineError):
                validate(study,self.root)
        (self.root/'registration.txt').write_bytes(canonical({k:original[k] for k in ('phase','registered_at','arms','tasks')}))
        score_path=self.root/original['assignments'][0]['scores'][0]['path']
        score=json.loads(score_path.read_bytes()); score['blinded']=False
        score_path.write_bytes(canonical(score))
        original['assignments'][0]['scores'][0]['sha256']=sha(score_path.read_bytes())
        with self.assertRaisesRegex(IntentlineError,'Unblinded'):
            validate(original,self.root)

    def test_failure_denominator_and_interval(self):
        self.assertIsNone(interval(0,0))
        self.assertAlmostEqual(interval(0,1)[1],0.7934506856)
        if os.name != 'posix':
            self.setup_work()
            return
        study=self.fixture(); run=study['assignments'][0]
        run.update(state='timeout',scores=[],output=None)
        result=assess(study,self.root)['arms']['ordinary']
        self.assertEqual(result['states'],{'timeout':1})
        self.assertEqual(result['eligible_assignments'],1)
        self.assertIsNone(result['adverse_counts'])

    def test_initial_not_run_receipt(self):
        if os.name != 'posix':
            self.setup_work()
            return
        root=Path(__file__).resolve().parents[1]/'evaluation'
        study=json.loads((root/'results/initial-not-run.json').read_bytes())
        self.assertEqual(assess(study,root)['eligible_tasks'],0)
