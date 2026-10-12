"""Authored calibration/scoring fixtures, never measured AI predictions."""
import copy
import os
from pathlib import Path
from unittest.mock import patch

from evaluation import ai_development_06 as ai
from intentline.errors import IntentlineError
from intentline.records import parse
from tests.support import WorkCase
from tests import test_ai_development_06 as base


class AIJudging(WorkCase):
    ref = base.AIDevelopment.ref
    register = base.AIDevelopment.register
    fixture = base.AIDevelopment.fixture
    check = base.AIDevelopment.check

    def agent(self, role, session, environment, inputs, output=None, time='2026-10-12T17:50:00Z'):
        value = {'agent_role': role, 'model_id': 'authored-test-model', 'version': 'fixture-v1', 'reasoning': 'fixture-only', 'run_or_session_id': session,
                 'environment_id': environment, 'context_access': inputs, 'started_at': time, 'timestamp': time, 'output': output}
        return {**value, 'record': self.ref('receipts/'+session+'.json', value, 'agent_receipt')}

    def calibration(self):
        study = self.fixture(); task = study['tasks'][0]
        public = Path(__file__).resolve().parents[1]/'evaluation/cases/ai_06'
        source = self.ref('visible/request.txt', (public/'control-source.txt').read_text(), 'source')
        task['request'] = source
        for run in study['assignments']: run['inputs'] = [source]
        controls = parse((public/'authored-controls.json').read_bytes())['controls']
        rules = self.ref('instructions/judge.txt', 'Authored seven-dimension judge fixture', 'instructions')
        config = {'model_id': 'authored-test-model', 'version': 'fixture-v1', 'reasoning': 'fixture-only'}
        for arm in study['arms'].values(): arm.update(config, seconds=600)
        protocol = {'record': 'intentline.ai-judge-protocol', 'schema_version': 1, 'control_version': 'authored-v1',
                    'registered_at': '2026-10-12T17:40:00Z', 'rubric_sha256': ai.RUBRIC_SHA256,
                    'rules': rules, 'judge_config': config, 'controls': []}
        visible = [source, rules]
        for control in controls:
            plan = self.ref('judging/inputs/'+control['id']+'.json', control['plan'], 'neutral')
            visible.append(plan)
            protocol['controls'].append({k: control[k] for k in ('id', 'category', 'expected_dimensions', 'critical', 'anchors')}
                                       | {'task': task['id'], 'inputs': [source], 'plan': plan})
        protocol_ref = self.ref('restricted/calibration/protocol.json', protocol, 'protocol')
        grant = {'provider': 'authored-provider', 'models': [config], 'max_cost_usd': 1,
                 'subscription_limit': None, 'max_calls': 100, 'max_seconds': 1000,
                 'host_ids': ['judgeA', 'judgeB', 'planner', 'scorerA', 'scorerB'],
                 'source_sha256s': [source['sha256']], 'issued_at': '2026-10-12T17:30:00Z',
                 'authority': 'Authored test grant; no actual inference authorization'}
        study['authorization'] = self.ref('receipts/grant.json', grant, 'grant')
        judges = [self.agent('judge', 'j'+str(i), 'judge'+suffix, visible) for i, suffix in enumerate(('A', 'B'))]
        receipts = []
        for judge in judges:
            predictions = []
            for control in controls:
                citations = []
                target_anchor = control['anchors'][0]
                for d in ai.DIMENSIONS:
                    citations.append({'source': target_anchor, 'output_ids': [], 'dimension': d,
                                      'finding': 'Authored predicted '+d,
                                      'severity': ('critical' if control['critical'] else 'material') if control['expected_dimensions'][d] else 'coverage',
                                      'counterexample': 'Authored source-violating alternative' if control['expected_dimensions'][d] else None})
                predictions.append({'control_id': control['id'], 'dimensions': control['expected_dimensions'],
                                    'critical': control['critical'], 'citations': citations})
            receipts.append(self.ref('judging/calibration/'+judge['run_or_session_id']+'.json',
                                     {'judge_session_id': judge['run_or_session_id'], 'protocol_sha256': protocol_ref['sha256'],
                                      'timestamp': '2026-10-12T17:55:00Z', 'predictions': predictions}, 'calibration'))
        study['judge_calibration'].update(status='observed', protocol=protocol_ref, judges=judges, receipts=receipts)
        self.register(study)
        return study

    def rewrite(self, ref, value):
        return self.ref(ref['path'], value, ref['kind'])

    def test_calibration_counts_critical_miss_and_valid_alternative_rejection(self):
        if os.name != 'posix': self.setup_work(); return
        study = self.calibration()
        result = self.check(study)
        self.assertTrue(result['calibration']['qualified'])  # authored mechanics, not live calibration
        self.assertEqual(result['calibration']['controls'], 10)
        self.assertEqual(result['calibration']['critical_misses'], 0)
        self.assertFalse(result['gates']['sources'])  # one authored task can never qualify a cohort
        ref = study['judge_calibration']['receipts'][0]
        receipt = parse((self.root/ref['path']).read_bytes())
        prediction = receipt['predictions'][2]
        prediction['dimensions'] = dict.fromkeys(ai.DIMENSIONS, 0); prediction['critical'] = False
        for c in prediction['citations']: c.update(severity='coverage', counterexample=None)
        study['judge_calibration']['receipts'][0] = self.rewrite(ref, receipt)
        result = self.check(study)
        self.assertEqual(result['calibration']['critical_misses'], 1)
        self.assertFalse(result['calibration']['qualified'])
        self.assertEqual(result['calibration']['disagreements'], 1)
        positive = receipt['predictions'][1]
        positive['critical'] = True; positive['dimensions']['decision_errors'] = 1
        positive['citations'][3].update(severity='critical', counterexample='Authored false positive')
        study['judge_calibration']['receipts'][0] = self.rewrite(ref, receipt)
        self.assertEqual(self.check(study)['calibration']['false_rejections'], 1)

    def test_changed_controls_missing_population_and_hidden_labels(self):
        if os.name != 'posix': self.setup_work(); return
        original = self.calibration()
        changed = copy.deepcopy(original); ref = changed['judge_calibration']['protocol']
        protocol = parse((self.root/ref['path']).read_bytes()); protocol['control_version'] = 'changed-v2'
        changed['judge_calibration']['protocol'] = self.rewrite(ref, protocol)
        with self.assertRaisesRegex(IntentlineError, 'Registration changed'): self.check(changed)
        original = self.calibration()
        ref = original['judge_calibration']['receipts'][0]; receipt = parse((self.root/ref['path']).read_bytes())
        receipt['predictions'].pop(); original['judge_calibration']['receipts'][0] = self.rewrite(ref, receipt)
        self.assertFalse(self.check(original)['calibration']['qualified'])
        original = self.calibration(); judge = original['judge_calibration']['judges'][0]
        judge['context_access'].append(original['judge_calibration']['protocol'])
        judge['record'] = self.rewrite(judge['record'], {k: v for k, v in judge.items() if k != 'record'})
        with self.assertRaisesRegex(IntentlineError, 'hidden answers'): self.check(original)

    def scored(self):
        study = self.calibration(); task = study['tasks'][0]; source = task['request']
        anchor = {'sha256': source['sha256'], 'line_start': 2, 'line_end': 2,
                  'quote': 'Accepted: Keep valid usernames and existing retries unchanged.'}
        ledger = {'record': 'intentline.ai-obligation-ledger', 'schema_version': 1, 'task': task['id'],
                  'input_sha256s': [source['sha256']], 'obligations': [{'id': 'O1', 'source': anchor,
                  'scope': 'Unchanged behavior', 'severity': 'critical', 'observable': 'Original retry count retained',
                  'counterexample': 'Deletes retries', 'uncertainty': 'resolved', 'binding': True}]}
        task['reference'] = self.ref('restricted/gold/ledger.json', ledger, 'reference')
        task['critique'] = self.ref('restricted/critiques/critique.json',
                                   {'task': task['id'], 'reference_sha256': task['reference']['sha256'],
                                    'input_sha256s': [source['sha256']], 'findings': ['Authored mechanical test only']}, 'critique')
        task['agents'] = [self.agent('oracle', 'oracle', 'oracle-env', [source], task['reference']),
                          self.agent('critic', 'critic', 'critic-env', [source, task['reference']], task['critique'])]
        run = study['assignments'][0]; run['state'] = 'completed'
        neutral = {'blind_id': run['blind_id'], 'content': 'Keep original retry count.',
                   'rows': [{'id': 'R1', 'text': 'Keep retries; deleting them fails.', 'binding': True, 'sources': [anchor]}],
                   'exclusions': [], 'uncertainty': []}
        run['output'] = self.ref('runs/ordinary/output.json', {'branding': 'ordinary', **{k: v for k, v in neutral.items() if k != 'blind_id'}}, 'output')
        run['neutral'] = self.ref('judging/inputs/neutral.json', neutral, 'neutral')
        run['mapping'] = self.ref('restricted/mappings/map.json',
                                 {k: run[k] for k in ('blind_id', 'task', 'arm')} | {'raw_sha256': run['output']['sha256'],
                                  'neutral_sha256': run['neutral']['sha256'], 'removed_fields': ['branding']}, 'mapping')
        run['prompt'] = self.ref('runs/ordinary/prompt.txt', 'Authored planner prompt', 'prompt')
        run['transcript'] = self.ref('runs/ordinary/transcript.txt', 'Authored transcript, not a model result', 'transcript')
        execution = {k: run[k] for k in ('task', 'arm', 'blind_id', 'state')} | {
            'input_sha256s': [source['sha256']], 'output_sha256': run['output']['sha256'],
            'prompt_sha256': run['prompt']['sha256'], 'transcript_sha256': run['transcript']['sha256'],
            **{k: study['arms']['ordinary'][k] for k in ('model_id', 'version', 'reasoning')},
            'session_id': 'planner', 'environment_id': 'planner', 'started_at': '2026-10-12T18:01:00Z',
            'finished_at': '2026-10-12T18:02:00Z', 'transport': 'operator_import'}
        run['execution'] = self.ref('receipts/execution.json', execution, 'execution')
        protocol = parse((self.root/study['judge_calibration']['protocol']['path']).read_bytes())
        for i, judge in enumerate(study['judge_calibration']['judges']):
            context = self.ref('receipts/score-context'+str(i)+'.json',
                               {'session_id': 'scoring'+str(i), 'environment_id': 'scorer'+('A','B')[i],
                                'judge_session_id': judge['run_or_session_id'], 'model_config': protocol['judge_config'],
                                'inputs': [source, run['neutral'], protocol['rules']], 'fresh_context': True,
                                'started_at': '2026-10-12T18:03:00Z'}, 'agent_receipt')
            score = {'blind_id': run['blind_id'], 'neutral_sha256': run['neutral']['sha256'],
                     'judge_session_id': judge['run_or_session_id'], 'timestamp': '2026-10-12T18:04:00Z',
                     'dimensions': dict.fromkeys(ai.DIMENSIONS, 0), 'critical': False,
                     'adjudication': {'state': 'clear', 'reason': 'Authored fixture'},
                     'citations': [{'source': anchor, 'output_ids': ['R1'], 'dimension': d, 'finding': 'Covered',
                                    'severity': 'coverage', 'counterexample': None} for d in ai.DIMENSIONS],
                     'coverage': [{'obligation_id': 'O1', 'output_ids': ['R1'], 'status': 'covered', 'source': anchor}],
                     'row_support': [{'output_id': 'R1', 'status': 'supported', 'source': anchor}], 'context': context}
            run['scores'].append(self.ref('judging/results/score'+str(i)+'.json', score, 'score'))
        self.register(study)
        return study

    def test_bound_normalization_coverage_dissent_and_readonly(self):
        if os.name != 'posix': self.setup_work(); return
        study = self.scored()
        with patch('subprocess.Popen', side_effect=AssertionError), patch('socket.socket', side_effect=AssertionError):
            result = self.check(study)
        self.assertEqual(result['status'], 'ai_development_unqualified')
        self.assertEqual(result['paired'][0]['arms']['ordinary']['judges'], 2)
        self.assertIsNone(result['arms']['ordinary']['adverse_counts'])
        self.assertIsNone(result['arms']['ordinary']['clean_fraction'])
        ref = study['assignments'][0]['scores'][1]; score = parse((self.root/ref['path']).read_bytes())
        score['coverage'][0].update(status='omitted', output_ids=[])
        with self.assertRaisesRegex(IntentlineError, 'Omission scored clean'):
            study['assignments'][0]['scores'][1] = self.rewrite(ref, score); self.check(study)
        score['dimensions']['material_omissions'] = 1
        score['citations'][0].update(severity='critical', output_ids=[], counterexample='Deletes retries')
        score['critical'] = True; score['adjudication'] = {'state': 'contested', 'reason': 'Authored dissent'}
        study['assignments'][0]['scores'][1] = self.rewrite(ref, score)
        observed = self.check(study)['paired'][0]['arms']['ordinary']
        self.assertTrue(observed['unresolved']); self.assertEqual(observed['dimension_disagreements'], 1)
        study = self.scored(); run = study['assignments'][0]
        neutral = parse((self.root/run['neutral']['path']).read_bytes()); neutral['exclusions'] = ['Deleted requirement']
        run['neutral'] = self.rewrite(run['neutral'], neutral)
        with self.assertRaisesRegex(IntentlineError, 'material content'): self.check(study)

    def test_known_budget_overrun_role_and_native_provenance_refusals(self):
        if os.name != 'posix': self.setup_work(); return
        study = self.scored(); study['assignments'][0]['metrics']['cost'] = 2
        with self.assertRaisesRegex(IntentlineError, 'usage exceeds'): self.check(study)
        study['assignments'][0]['metrics']['cost'] = None
        oracle = study['tasks'][0]['agents'][0]
        oracle['context_access'].append(study['tasks'][0]['reference'])
        oracle['record'] = self.rewrite(oracle['record'], {k:v for k,v in oracle.items() if k!='record'})
        self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'input boundary'): self.check(study)
        study = self.scored(); run = study['assignments'][0]
        run['execution'] = self.ref('receipts/execution.json', 'Opaque fake native PASS', 'execution')
        with self.assertRaises(IntentlineError): self.check(study)
        study = self.scored(); study['assignments'][0]['metrics']['tokens'] = 10**999
        with self.assertRaises(IntentlineError): self.check(study)
