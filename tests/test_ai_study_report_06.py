"""Authored three-task qualification controls; no actual AI or host observations."""
import copy
import json
import os
import unittest
from unittest.mock import patch

from evaluation import ai_development_06 as ai
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import parse
from tests.support import WorkCase
from tests import test_ai_judging_06 as judging


def read(case, ref):
    return parse((case.root / ref['path']).read_bytes())


def qualified_fixture(case):
    original = case.scored()
    template_task = original['tasks'][0]
    template_run = original['assignments'][0]
    old_source = template_task['request']
    control_templates = read(case, original['judge_calibration']['protocol'])['controls']
    source_text = (case.root / old_source['path']).read_text()
    s = copy.deepcopy(original)
    s.update(tasks=[], population=[], assignments=[])
    config = {k: s['arms']['ordinary'][k] for k in ('model_id', 'version', 'reasoning')}
    rules = read(case, original['judge_calibration']['protocol'])['rules']
    controls, calibration_inputs, hosts = [], [rules], []
    policies = []

    def host(environment, inputs, tested='2026-10-12T17:45:00Z', tools=None):
        hosts.append(environment)
        policy = case.ref('receipts/policy-' + environment + '.json',
                          {'environment_id': environment, 'read_sha256s': [r['sha256'] for r in inputs],
                           'write_scope': 'own_scratch', 'tools': tools or [], 'egress': 'denied',
                           'session_visibility': 'own_only', 'operator_separated': True}, 'host_policy')
        witness = case.ref('receipts/witness-' + environment + '.txt',
                           'AUTHORED UNIT FIXTURE: no actual host witness', 'host_witness')
        policies.append(case.ref('receipts/host-' + environment + '.json',
                                 {'environment_id': environment, 'tested_at': tested,
                                  'canaries': dict.fromkeys(ai.CANARIES, 'denied'),
                                  'permissions': policy, 'witness': witness}, 'host_receipt'))

    for ti in range(3):
        tid = 'synthetic' + str(ti)
        source = case.ref('visible/' + tid + '.txt', source_text + '\nAuthored fixture ' + str(ti), 'source')

        def replace(value):
            if value == old_source:
                return copy.deepcopy(source)
            if isinstance(value, dict):
                return {k: replace(v) for k, v in value.items()}
            if isinstance(value, list):
                return [replace(v) for v in value]
            return source['sha256'] if value == old_source['sha256'] else value

        task = replace(copy.deepcopy(template_task))
        task.update(id=tid, repository='authored/project' + str(ti), kind='historical',
                    source_decision='checked', contamination=[])
        ledger = replace(read(case, template_task['reference']))
        ledger['task'] = tid
        task['reference'] = case.ref('restricted/gold/' + tid + '.json', ledger, 'reference')
        task['critique'] = case.ref('restricted/critiques/' + tid + '.json',
                                   {'task': tid, 'reference_sha256': task['reference']['sha256'],
                                    'input_sha256s': [source['sha256']], 'findings': []}, 'critique')
        task['agents'] = [case.agent('oracle', tid + '-oracle', tid + '-oracle', [source], task['reference']),
                          case.agent('critic', tid + '-critic', tid + '-critic', [source, task['reference']], task['critique'])]
        host(tid + '-oracle', [source])
        host(tid + '-critic', [source, task['reference']])
        s['tasks'].append(task)
        calibration_inputs.append(source)
        for ci, template in enumerate(control_templates):
            control = replace(copy.deepcopy(template))
            control.update(id=tid + '-c' + str(ci), task=tid)
            plan = replace(read(case, template['plan']))
            control['plan'] = case.ref('judging/inputs/' + control['id'] + '.json', plan, 'neutral')
            controls.append(control)
            calibration_inputs.append(control['plan'])
        for ai_index, arm in enumerate(ai.ARMS):
            key = tid + '-' + arm
            run = replace(copy.deepcopy(template_run))
            run.update(task=tid, arm=arm, blind_id='%032x' % (ti * 3 + ai_index + 100), scores=[])
            neutral = replace(read(case, template_run['neutral']))
            neutral['blind_id'] = run['blind_id']
            run['neutral'] = case.ref('judging/inputs/' + key + '.json', neutral, 'neutral')
            run['output'] = case.ref('runs/' + key + '/output.json',
                                     {'branding': arm, **{k: v for k, v in neutral.items() if k != 'blind_id'}}, 'output')
            run['mapping'] = case.ref('restricted/mappings/' + key + '.json',
                                      {k: run[k] for k in ('blind_id', 'task', 'arm')} |
                                      {'raw_sha256': run['output']['sha256'], 'neutral_sha256': run['neutral']['sha256'],
                                       'removed_fields': ['branding']}, 'mapping')
            run['prompt'] = case.ref('runs/' + key + '/prompt.txt', 'Authored prompt ' + key, 'prompt')
            run['transcript'] = case.ref('runs/' + key + '/transcript.txt', 'Authored transcript ' + key, 'transcript')
            execution = ({k: run[k] for k in ('task', 'arm', 'blind_id', 'state')} |
                        {'input_sha256s': [source['sha256']], 'output_sha256': run['output']['sha256'],
                         'prompt_sha256': run['prompt']['sha256'], 'transcript_sha256': run['transcript']['sha256'],
                         **config, 'session_id': key, 'environment_id': key,
                         'started_at': '2026-10-12T18:01:00Z', 'finished_at': '2026-10-12T18:02:00Z',
                         'transport': 'operator_import'})
            run['execution'] = case.ref('receipts/' + key + '.json', execution, 'execution')
            host(key, [source, s['arms'][arm]['instructions']], tools=s['arms'][arm]['tools'])
            for ji in range(2):
                score = replace(read(case, template_run['scores'][ji]))
                score.update(blind_id=run['blind_id'], neutral_sha256=run['neutral']['sha256'])
                context = read(case, score['context'])
                context.update(session_id=key + '-score' + str(ji), environment_id=key + '-score' + str(ji),
                               inputs=[source, run['neutral'], rules])
                score['context'] = case.ref('receipts/' + context['session_id'] + '.json', context, 'agent_receipt')
                run['scores'].append(case.ref('judging/results/' + context['session_id'] + '.json', score, 'score'))
                host(context['environment_id'], context['inputs'], tested='2026-10-12T18:02:00Z')
            s['population'].append({k: run[k] for k in ('task', 'arm', 'blind_id')})
            s['assignments'].append(run)
    protocol = read(case, original['judge_calibration']['protocol'])
    protocol['controls'] = controls
    protocol_ref = case.ref('restricted/calibration/three-task.json', protocol, 'protocol')
    judges = [case.agent('judge', 'j' + str(i), 'judge' + str(i), calibration_inputs) for i in range(2)]
    receipts = []
    for judge in judges:
        host(judge['environment_id'], calibration_inputs)
        predictions = []
        for control in controls:
            counts = control['expected_dimensions']
            predictions.append({'control_id': control['id'], 'dimensions': counts, 'critical': control['critical'],
                                'citations': [{'source': control['anchors'][0], 'output_ids': [], 'dimension': dim,
                                               'finding': 'Authored prediction', 'severity': ('critical' if control['critical'] else 'material') if counts[dim] else 'coverage',
                                               'counterexample': 'Authored counterexample' if counts[dim] else None}
                                              for dim in ai.DIMENSIONS]})
        receipts.append(case.ref('judging/calibration/' + judge['run_or_session_id'] + '.json',
                                 {'judge_session_id': judge['run_or_session_id'], 'protocol_sha256': protocol_ref['sha256'],
                                  'timestamp': '2026-10-12T17:55:00Z', 'predictions': predictions}, 'calibration'))
    s['judge_calibration'].update(protocol=protocol_ref, judges=judges, receipts=receipts)
    s['isolation'] = {'mode': 'host-enforced', 'receipts': policies}
    grant = read(case, s['authorization'])
    grant.update(host_ids=hosts, source_sha256s=[t['request']['sha256'] for t in s['tasks']])
    s['authorization'] = case.rewrite(s['authorization'], grant)
    s['blockers'] = []
    case.register(s)
    return s


@unittest.skipUnless(os.name == 'posix', 'Secure study storage requires POSIX')
class AIStudyReport(WorkCase):
    ref = judging.AIJudging.ref
    register = judging.AIJudging.register
    fixture = judging.AIJudging.fixture
    calibration = judging.AIJudging.calibration
    scored = judging.AIJudging.scored
    agent = judging.AIJudging.agent
    rewrite = judging.AIJudging.rewrite
    check = judging.AIJudging.check

    def test_unresolved_source_challenge_and_recorded_time_limits(self):
        study = qualified_fixture(self)
        task = study['tasks'][0]
        critique = read(self, task['critique'])
        critique['findings'] = ['Unresolved critical source-authority challenge']
        task['critique'] = self.rewrite(task['critique'], critique)
        critic = task['agents'][1]; critic['output'] = task['critique']
        critic['record'] = self.rewrite(critic['record'], {k:v for k,v in critic.items() if k!='record'})
        self.register(study)
        result = self.check(study)
        self.assertEqual(result['status'], 'ai_development_unqualified')
        self.assertIsNone(result['arms']['ordinary']['clean_fraction'])
        study = qualified_fixture(self)
        for arm in study['arms'].values(): arm['seconds'] = None
        self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'time horizon'): self.check(study)
        study = qualified_fixture(self)
        for arm in study['arms'].values(): arm['seconds'] = 1
        self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'arm horizon'): self.check(study)
        study = qualified_fixture(self)
        grant = read(self, study['authorization']); grant['max_seconds'] = 1
        study['authorization'] = self.rewrite(study['authorization'], grant); self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'granted time'): self.check(study)

    def test_authored_qualified_branch_remains_private_and_unknown_usage_null(self):
        study = qualified_fixture(self)
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(Directory, 'write', side_effect=AssertionError('write')), \
                patch('subprocess.Popen', side_effect=AssertionError('dispatch')), \
                patch('socket.socket', side_effect=AssertionError('network')):
            report = self.check(study)
        self.assertEqual(report['status'], 'ai_development_observed')  # authored branch control only
        self.assertTrue(all(report['gates'].values()))
        self.assertEqual(report['actual_attempts'], 9)
        self.assertEqual(report['formal_eligible_tasks'], 0)
        self.assertEqual(report['human_independence'], 'unverified')
        self.assertIsNone(report['all_in_usage']['cost'])
        for arm in ai.ARMS:
            self.assertEqual(report['arms'][arm]['qualified_scored'], 3)
            self.assertEqual(report['arms'][arm]['clean_fraction']['numerator'], 3)
            self.assertEqual(report['arms'][arm]['clean_fraction']['denominator'], 3)
            self.assertIsNone(report['arms'][arm]['usage_all_attempts']['tokens'])
        for private in ('synthetic0', 'authored/project', str(self.root), 'original retry count'):
            self.assertNotIn(private, json.dumps(report))
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_timeout_remains_in_qualified_denominator(self):
        study = qualified_fixture(self)
        run = study['assignments'][0]
        run.update(state='timeout', neutral=None, mapping=None, scores=[])
        execution = read(self, run['execution']); execution['state'] = 'timeout'
        run['execution'] = self.rewrite(run['execution'], execution)
        result = self.check(study)
        self.assertEqual(result['status'], 'ai_development_observed')
        arm = result['arms']['ordinary']
        self.assertEqual(arm['states']['timeout'], 1)
        self.assertEqual(arm['assignments'], 3)
        self.assertEqual(arm['qualified_scored'], 2)
        self.assertEqual(arm['clean_fraction']['numerator'], 2)
        self.assertEqual(arm['clean_fraction']['denominator'], 3)
        self.assertIsNone(arm['usage_all_attempts']['cost'])

    def test_unscored_attempts_do_not_publish_comparative_zeroes(self):
        study = qualified_fixture(self)
        for run in study['assignments']:
            run['scores'] = []
        report = self.check(study)
        self.assertEqual(report['status'], 'ai_development_unqualified')
        self.assertTrue(all(a['qualified_scored'] == 0 and a['adverse_counts'] is None
                            and a['clean_fraction'] is None for a in report['arms'].values()))

    def test_support_and_critical_disagreements_remain_unresolved(self):
        study = qualified_fixture(self); run = study['assignments'][0]
        for i, ref in enumerate(run['scores']):
            score = read(self, ref)
            score['dimensions']['invented_obligations'] = 1
            citation = next(c for c in score['citations'] if c['dimension'] == 'invented_obligations')
            citation.update(severity='critical' if i else 'material', counterexample='Authored invented promise')
            score.update(critical=bool(i), adjudication={'state': 'source_certain' if i else 'clear', 'reason': 'Authored disagreement'})
            if i: score['row_support'][0].update(status='unsupported', source=None)
            run['scores'][i] = self.rewrite(ref, score)
        paired = self.check(study)['paired'][0]['arms']['ordinary']
        self.assertEqual(paired['dimension_disagreements'], 0)
        self.assertEqual(paired['support_disagreements'], 1)
        self.assertTrue(paired['critical_disagreement'])
        self.assertTrue(paired['unresolved'])
        self.assertFalse(paired['clean'])

    def test_extra_readable_host_hash_stops_comparative_reporting(self):
        study = qualified_fixture(self)
        environment = read(self, study['assignments'][0]['execution'])['environment_id']
        for index, ref in enumerate(study['isolation']['receipts']):
            receipt = read(self, ref)
            if receipt['environment_id'] == environment:
                policy = read(self, receipt['permissions'])
                policy['read_sha256s'].append(study['tasks'][0]['reference']['sha256'])
                receipt['permissions'] = self.rewrite(receipt['permissions'], policy)
                study['isolation']['receipts'][index] = self.rewrite(ref, receipt)
                break
        result = self.check(study)
        self.assertEqual(result['status'], 'ai_development_unqualified')
        self.assertFalse(result['gates']['isolation'])
        self.assertTrue(all(a['adverse_counts'] is None and a['clean_fraction'] is None for a in result['arms'].values()))

    def test_scoring_environment_outside_declared_grant_refuses(self):
        study = qualified_fixture(self)
        environment = read(self, read(self, study['assignments'][0]['scores'][0])['context'])['environment_id']
        grant = read(self, study['authorization']); grant['host_ids'].remove(environment)
        study['authorization'] = self.rewrite(study['authorization'], grant); self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'grant'):
            self.check(study)

    def test_unknown_or_unapproved_preparation_cannot_qualify(self):
        for change in ('unknown_version', 'unapproved_model', 'unapproved_host'):
            with self.subTest(change=change):
                study = qualified_fixture(self); actor = study['tasks'][0]['agents'][0]
                if change == 'unapproved_host':
                    grant = read(self, study['authorization'])
                    grant['host_ids'].remove(actor['environment_id'])
                    study['authorization'] = self.rewrite(study['authorization'], grant)
                else:
                    actor['version' if change == 'unknown_version' else 'model_id'] = None if change == 'unknown_version' else 'unapproved-model'
                    actor['record'] = self.rewrite(actor['record'], {k: v for k, v in actor.items() if k != 'record'})
                self.register(study)
                report = self.check(study)
                self.assertEqual(report['status'], 'ai_development_unqualified')
                self.assertFalse(report['gates']['sources'])
                self.assertEqual(report['actual_attempts'], 9)

    def test_failed_host_receipt_cannot_be_replaced_by_passing_duplicate(self):
        study = qualified_fixture(self)
        failed = read(self, study['isolation']['receipts'][0])
        failed['canaries']['gold'] = 'accessible'
        study['isolation']['receipts'].insert(0, self.ref('receipts/failed-duplicate.json', failed, 'host_receipt'))
        with self.assertRaisesRegex(IntentlineError, 'Duplicate environment'):
            self.check(study)

    def test_resolved_critical_omission_cannot_be_downgraded(self):
        study = qualified_fixture(self); run = study['assignments'][0]
        score = read(self, run['scores'][0])
        score['coverage'][0].update(status='omitted', output_ids=[])
        score['dimensions']['material_omissions'] = 1
        citation = next(c for c in score['citations'] if c['dimension'] == 'material_omissions')
        citation.update(output_ids=[], severity='material', counterexample='Drops critical retry promise')
        run['scores'][0] = self.rewrite(run['scores'][0], score)
        with self.assertRaisesRegex(IntentlineError, 'Critical omission downgraded'):
            self.check(study)
