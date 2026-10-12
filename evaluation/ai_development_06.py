"""Read-only AI-only development artifact inspection; never dispatches an arm."""
import argparse
from collections import Counter
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys

from evaluation.planning_02 import ARMS, DIMENSIONS, METRICS, STATES, interval, number, require, snapshot
from intentline.audits import timestamp
from intentline.errors import IntentlineError
from intentline.paths import Directory, MAX_FILE, absolute, text
from intentline.records import canonical, digest, fields, integer, load, parse, sha, string

KINDS = {'source': 'visible/', 'license': 'sources/', 'provenance': 'sources/',
         'reference': 'restricted/gold/', 'critique': 'restricted/critiques/',
         'instructions': 'instructions/', 'registration': 'receipts/',
         'agent_receipt': 'receipts/', 'host_receipt': 'receipts/',
         'prompt': 'runs/', 'output': 'runs/', 'transcript': 'runs/',
         'execution': 'receipts/', 'neutral': 'judging/inputs/',
         'mapping': 'restricted/mappings/', 'score': 'judging/results/',
         'protocol': 'restricted/calibration/', 'calibration': 'judging/calibration/',
         'grant': 'receipts/', 'host_policy': 'receipts/', 'host_witness': 'receipts/'}
USAGE = METRICS + ('input_tokens', 'cached_input_tokens', 'output_tokens',
                   'reasoning_tokens', 'manual_interventions')
BLOCKERS = ('budget', 'host', 'isolation', 'sources', 'calibration')
DECISIONS = ('fix_specific_defect', 'simplify_overhead',
             'insufficient_or_unqualified_evidence', 'expand_new_tasks')
ROLES = ('researcher', 'drafter', 'oracle', 'critic', 'judge')
CANARIES = ('gold', 'other_arm', 'operator_answers', 'network', 'connected_apps')
RUBRIC_SHA256 = '6f18178d3eec040e7072c98ed8c6875cc73055c84b369a44d31460c26461ecdd'
CONTROL_DIMENSIONS = {'omission': 'material_omissions', 'invention': 'invented_obligations',
                      'exception': 'constraint_losses', 'authority': 'decision_errors',
                      'oracle': 'weak_oracles', 'gap': 'missing_gap_disclosures',
                      'blocker': 'unnecessary_blockers', 'exclusion': 'constraint_losses'}
CONTROL_CATEGORIES = ('positive_a', 'positive_b', *CONTROL_DIMENSIONS)


def items(value, maximum=100):
    require(isinstance(value, list) and len(value) <= maximum, 'Invalid bounded array')
    return value


def token(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value), 'Invalid opaque ID')


def strings(value, maximum=100):
    for item in items(value, maximum):
        string(item)


def version(value):
    require(type(value) is int and value == 1, 'Unsupported record version')


def date(value):
    timestamp(value)
    return datetime.fromisoformat(value)


def artifact(root, ref, kind=None):
    fields(ref, ('path', 'sha256', 'size', 'kind'))
    require(isinstance(ref['kind'], str) and ref['kind'] in KINDS and (kind is None or ref['kind'] == kind), 'Artifact kind mismatch')
    integer(ref['size'])
    require(ref['size'] <= MAX_FILE, 'Oversize artifact')
    string(ref['path'])
    require(ref['path'].startswith(KINDS[ref['kind']]), 'Artifact compartment mismatch')
    raw = snapshot(root, {k: ref[k] for k in ('path', 'sha256')})
    require(len(raw) == ref['size'], 'Artifact size mismatch')
    return raw


def document(root, ref, kind):
    raw = artifact(root, ref, kind)
    value = parse(raw)
    require(canonical(value) == raw, 'Noncanonical record')
    return value


def usage(value):
    fields(value, USAGE)
    for key, measurement in value.items():
        require(measurement is None or type(measurement) in (int, float) and 0 <= measurement <= 10**12,
                'Measurement outside supported bound')
        number(measurement, nullable=True)
        if key not in ('elapsed_seconds', 'cost') and measurement is not None:
            require(type(measurement) is int, 'Counts must be integers')
    for subset, total in (('cached_input_tokens', 'input_tokens'), ('reasoning_tokens', 'output_tokens')):
        if value[subset] is not None and value[total] is not None:
            require(value[subset] <= value[total], 'Token subset exceeds total')
    if all(value[k] is not None for k in ('tokens', 'input_tokens', 'output_tokens')):
        require(value['tokens'] == value['input_tokens'] + value['output_tokens'], 'Token categories disagree')


def totals(values):
    return {m: sum(v[m] for v in values) if values and all(v[m] is not None for v in values) else None
            for m in USAGE}


def anchor(value, sources):
    fields(value, ('sha256', 'line_start', 'line_end', 'quote'))
    require(value['sha256'] in sources, 'Unknown citation source')
    integer(value['line_start']); integer(value['line_end'])
    lines = text(sources[value['sha256']]).splitlines(keepends=True)
    string(value['quote'])
    require(value['line_start'] <= value['line_end'] <= len(lines), 'Citation lines outside source')
    exact = ''.join(lines[value['line_start']-1:value['line_end']])
    require(value['quote'] in (exact, exact.removesuffix('\n').removesuffix('\r')), 'Citation quote mismatch')


def actor(value, root, role=None):
    fields(value, ('agent_role', 'model_id', 'run_or_session_id', 'environment_id',
                   'context_access', 'timestamp', 'output', 'record'))
    require(value['agent_role'] in ROLES and (role is None or value['agent_role'] == role), 'Invalid AI role')
    for key in ('model_id', 'run_or_session_id'):
        string(value[key])
    if value['environment_id'] is not None:
        token(value['environment_id'])
    date(value['timestamp'])
    for ref in items(value['context_access'], 64):
        artifact(root, ref)
    if value['output'] is not None:
        artifact(root, value['output'])
    receipt = document(root, value['record'], 'agent_receipt')
    require(receipt == {k: v for k, v in value.items() if k != 'record'}, 'AI receipt identity mismatch')


def ledger(task, root, sources):
    if task['reference'] is None:
        require(task['critique'] is None, 'Critique without reference')
        return []
    value = document(root, task['reference'], 'reference')
    fields(value, ('record', 'schema_version', 'task', 'input_sha256s', 'obligations'))
    require(value['record'] == 'intentline.ai-obligation-ledger', 'Invalid AI ledger')
    version(value['schema_version'])
    require(value['task'] == task['id'] and value['input_sha256s'] == list(sources), 'Reference subject mismatch')
    ids = set()
    for obligation in items(value['obligations'], 256):
        fields(obligation, ('id', 'source', 'scope', 'severity', 'observable', 'counterexample', 'uncertainty', 'binding'))
        token(obligation['id'])
        require(obligation['id'] not in ids, 'Duplicate obligation')
        ids.add(obligation['id'])
        anchor(obligation['source'], sources)
        for key in ('scope', 'observable', 'counterexample'):
            string(obligation[key])
        require(obligation['severity'] in ('material', 'critical') and
                obligation['uncertainty'] in ('resolved', 'contested') and type(obligation['binding']) is bool,
                'Invalid obligation classification')
    if task['critique'] is not None:
        critique = document(root, task['critique'], 'critique')
        fields(critique, ('task', 'reference_sha256', 'input_sha256s', 'findings'))
        require(critique['task'] == task['id'] and critique['reference_sha256'] == task['reference']['sha256']
                and critique['input_sha256s'] == list(sources), 'Challenge subject mismatch')
        strings(critique['findings'])
    return value['obligations']


def sealed(study):
    return {**{k: study[k] for k in ('registered_at', 'arms', 'tasks', 'population')},
            'judge_protocol': study['judge_calibration']['protocol'],
            'isolation_policy': study['isolation']['mode'], 'authorization': study['authorization']}


def host_gate(study, root):
    isolation = study['isolation']
    fields(isolation, ('mode', 'receipts'))
    require(isolation['mode'] in ('host-enforced', 'shared', 'unverified'), 'Invalid isolation')
    environments, seen = {}, set()
    for ref in items(isolation['receipts'], 100):
        record = document(root, ref, 'host_receipt')
        fields(record, ('environment_id', 'tested_at', 'canaries', 'permissions', 'witness'))
        token(record['environment_id'])
        policy = document(root, record['permissions'], 'host_policy')
        fields(policy, ('environment_id', 'read_sha256s', 'write_scope', 'tools', 'egress', 'session_visibility', 'operator_separated'))
        require(policy['environment_id'] == record['environment_id'], 'Host policy subject mismatch')
        for identity in items(policy['read_sha256s'], 128): digest(identity)
        strings(policy['tools'], 64)
        require(policy['write_scope'] in ('own_scratch', 'unverified') and policy['egress'] in ('denied', 'unverified')
                and policy['session_visibility'] in ('own_only', 'unverified') and type(policy['operator_separated']) is bool,
                'Invalid host policy')
        artifact(root, record['witness'], 'host_witness')
        date(record['tested_at'])
        fields(record['canaries'], CANARIES)
        require(all(v in ('denied', 'accessible', 'untested') for v in record['canaries'].values()), 'Invalid canary state')
        require(record['environment_id'] not in seen, 'Duplicate environment receipt')
        seen.add(record['environment_id'])
        if all(v == 'denied' for v in record['canaries'].values()) and policy['write_scope'] == 'own_scratch' and policy['egress'] == 'denied' and policy['session_visibility'] == 'own_only' and policy['operator_separated']:
            environments[record['environment_id']] = policy
    return environments if isolation['mode'] == 'host-enforced' else {}


def validate(study, root, registration_sha256):
    root = absolute(root)
    fields(study, ('record', 'schema_version', 'mode', 'phase', 'registered_at', 'registration',
                   'arms', 'tasks', 'population', 'assignments', 'judge_calibration', 'isolation',
                   'preparation', 'blockers', 'decision', 'authorization'))
    version(study['schema_version'])
    require(study['record'] == 'intentline.ai-development-study' and study['mode'] == 'ai_only_development'
            and study['phase'] == 'development', 'Unsupported AI-only study')
    date(study['registered_at']); digest(registration_sha256)
    with Directory(root) as directory:
        require(not study['tasks'] or directory.identity.st_uid == os.getuid()
                and not directory.identity.st_mode & 0o077, 'Study root must be owner-only')
    require(study['registration']['sha256'] == registration_sha256, 'External registration pin mismatch')
    require(document(root, study['registration'], 'registration') == sealed(study), 'Registration changed')
    fields(study['arms'], ARMS)
    common = None
    for arm in study['arms'].values():
        fields(arm, ('model_id', 'version', 'reasoning', 'seconds', 'tools', 'differences', 'instructions'))
        for key in ('model_id', 'version', 'reasoning'):
            if arm[key] is not None:
                string(arm[key])
        number(arm['seconds'], nullable=True); strings(arm['tools'], 64); strings(arm['differences'], 64)
        artifact(root, arm['instructions'], 'instructions')
        config = {k: v for k, v in arm.items() if k not in ('instructions', 'differences')}
        require(common is None or common == config, 'Planning configuration differs across arms')
        common = config
    require(study['decision'] in DECISIONS, 'Invalid development decision')
    require(len(items(study['blockers'], len(BLOCKERS))) == len(set(study['blockers']))
            and all(b in BLOCKERS for b in study['blockers']), 'Invalid blockers')
    usage(study['preparation'])
    grant = None
    if study['authorization'] is not None:
        grant = document(root, study['authorization'], 'grant')
        fields(grant, ('provider', 'models', 'max_cost_usd', 'subscription_limit', 'max_calls', 'max_seconds',
                       'host_ids', 'source_sha256s', 'issued_at', 'authority'))
        string(grant['provider']); string(grant['authority'])
        number(grant['max_cost_usd'], nullable=True)
        require(grant['max_cost_usd'] is not None or grant['subscription_limit'] is not None, 'Missing spending/subscription bound')
        if grant['subscription_limit'] is not None: string(grant['subscription_limit'])
        integer(grant['max_calls']); integer(grant['max_seconds'])
        for config in items(grant['models'], 8):
            fields(config, ('model_id', 'version', 'reasoning'))
            for value in config.values(): string(value)
        require(grant['models'], 'No authorized model')
        for host in items(grant['host_ids'], 100): token(host)
        for identity in items(grant['source_sha256s'], 6400): digest(identity)
        require(date(grant['issued_at']) <= date(study['registered_at']), 'Late authorization')
    environments = host_gate(study, root)
    tasks, sources, obligations, private, visible, request_hashes = {}, {}, {}, [], [], set()
    for task in items(study['tasks'], 100):
        fields(task, ('id', 'kind', 'repository', 'commit', 'license', 'provenance', 'request', 'context',
                      'reference', 'critique', 'agents', 'source_decision', 'contamination'))
        token(task['id']); require(task['id'] not in tasks, 'Duplicate task')
        require(task['kind'] in ('historical', 'authored_control'), 'Invalid task kind')
        require(isinstance(task['repository'], str) and re.fullmatch(r'[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+', task['repository']), 'Invalid repository')
        require(isinstance(task['commit'], str) and re.fullmatch('[0-9a-f]{40}', task['commit']), 'Full source commit required')
        artifact(root, task['license'], 'license'); artifact(root, task['provenance'], 'provenance')
        inputs = [task['request']] + items(task['context'], 64)
        source = {r['sha256']: artifact(root, r, 'source') for r in inputs}
        require(all(text(raw).strip() for raw in source.values()), 'Blank visible source')
        require(len(source) == len(inputs) and task['request']['sha256'] not in request_hashes, 'Duplicate corpus source key')
        request_hashes.add(task['request']['sha256']); visible.extend(inputs)
        for agent in items(task['agents'], 10):
            actor(agent, root)
            require(date(agent['timestamp']) <= date(study['registered_at']), 'Preparation must precede registration')
            private.append(agent['record'])
            if agent['agent_role'] in ('oracle', 'critic'):
                expected = inputs if agent['agent_role'] == 'oracle' else inputs + ([task['reference']] if task['reference'] else [])
                require(agent['context_access'] == expected, 'Preparation role input boundary mismatch')
                require(agent['output'] == task['reference' if agent['agent_role'] == 'oracle' else 'critique']
                        and agent['output'] is not None, 'Preparation role output mismatch')
        require(task['source_decision'] in ('checked', 'unreviewed'), 'Invalid source decision')
        strings(task['contamination'], 64)
        obligations[task['id']] = ledger(task, root, source)
        private.extend(task[k] for k in ('reference', 'critique') if task[k] is not None)
        tasks[task['id']], sources[task['id']] = task, source
        if grant:
            require(set(source) <= set(grant['source_sha256s']), 'Source outside grant')
    population, blinds = {}, set()
    for entry in items(study['population'], 300):
        fields(entry, ('task', 'arm', 'blind_id'))
        key = (entry['task'], entry['arm'])
        require(entry['task'] in tasks and entry['arm'] in ARMS and key not in population, 'Invalid population')
        require(isinstance(entry['blind_id'], str) and re.fullmatch('[0-9a-f]{32}', entry['blind_id'])
                and entry['blind_id'] not in blinds, 'Invalid opaque blind ID')
        population[key] = entry['blind_id']; blinds.add(entry['blind_id'])
    require(set(population) == {(t, a) for t in tasks for a in ARMS}, 'Incomplete registered population')
    attempts, sessions, seen = [], set(), set()
    for run in items(study['assignments'], 300):
        fields(run, ('task', 'arm', 'blind_id', 'state', 'inputs', 'output', 'neutral', 'mapping',
                     'prompt', 'transcript', 'execution', 'scores', 'metrics'))
        key = (run['task'], run['arm'])
        require(key in population and key not in seen and run['blind_id'] == population[key], 'Assignment identity swap')
        seen.add(key); task = tasks[run['task']]
        require(run['state'] in STATES and run['inputs'] == [task['request']] + task['context'], 'Invalid assignment inputs/state')
        usage(run['metrics']); items(run['scores'], 2)
        for name in ('output', 'neutral', 'mapping', 'prompt', 'transcript', 'execution'):
            if run[name] is not None:
                artifact(root, run[name], name)
        if run['state'] == 'not_run':
            require(all(run[k] is None for k in ('output', 'neutral', 'mapping', 'prompt', 'transcript', 'execution'))
                    and not run['scores'] and study['blockers'] and all(v is None for v in run['metrics'].values()),
                    'Unattempted assignment has results/usage')
        else:
            require(grant is not None, 'Attempt requires bounded operator grant')
            require(all(run[k] is not None for k in ('prompt', 'transcript', 'execution')), 'Attempt requires execution receipts')
            execution = document(root, run['execution'], 'execution')
            fields(execution, ('task', 'arm', 'blind_id', 'state', 'input_sha256s', 'output_sha256', 'prompt_sha256',
                               'transcript_sha256', 'model_id', 'version', 'reasoning', 'session_id', 'environment_id',
                               'started_at', 'finished_at', 'transport'))
            require(all(execution[k] == run[k] for k in ('task', 'arm', 'blind_id', 'state'))
                    and execution['input_sha256s'] == list(sources[run['task']]), 'Execution subject mismatch')
            for k in ('output', 'prompt', 'transcript'):
                require(execution[k+'_sha256'] == (run[k]['sha256'] if run[k] else None), 'Execution artifact mismatch')
            for k in ('model_id', 'version', 'reasoning'):
                require(execution[k] is not None and execution[k] == study['arms'][run['arm']][k], 'Execution configuration mismatch')
            require({k: execution[k] for k in ('model_id', 'version', 'reasoning')} in grant['models']
                    and execution['environment_id'] in grant['host_ids'], 'Execution outside grant')
            token(execution['session_id']); token(execution['environment_id'])
            require(execution['session_id'] not in sessions, 'Planning arms need fresh sessions')
            sessions.add(execution['session_id'])
            require(date(study['registered_at']) <= date(execution['started_at']) <= date(execution['finished_at']), 'Invalid execution chronology')
            require(execution['transport'] in ('native_host', 'operator_import'), 'Invalid execution transport')
            attempts.append(execution)
        require(run['state'] != 'completed' or run['output'] is not None, 'Completed output missing')
        private.extend(run[k] for k in ('mapping',) if run[k] is not None)
    require(seen == set(population), 'Missing assignment: retain all failures/not_run')
    visible.extend(a['instructions'] for a in study['arms'].values())
    visible.extend(r['prompt'] for r in study['assignments'] if r['prompt'] is not None)
    if study['judge_calibration']['protocol'] is not None:
        private.append(study['judge_calibration']['protocol'])
    # Reuse the formal evaluator's corpus-wide byte identity guard without its eligibility semantics.
    from evaluation.planning_02 import private_inputs
    private_inputs({'arms': study['arms'], 'tasks': [{'reference': None, 'reviews': [{'record': r} for r in private],
                                                    'request': r, 'context': []} for r in visible]})
    calibration = calibration_check(study, root)
    judged = scores_check(study, root, sources, obligations, calibration)
    if grant:
        measures = [study['preparation'], study['judge_calibration']['metrics'], study['judge_calibration']['judging_metrics']]
        measures += [r['metrics'] for r in study['assignments']]
        for metric, cap in (('model_calls', 'max_calls'), ('elapsed_seconds', 'max_seconds'), ('cost', 'max_cost_usd')):
            require(grant[cap] is None or sum(v[metric] for v in measures if v[metric] is not None) <= grant[cap], 'Known usage exceeds grant')
    if not tasks:
        require(study['blockers'], 'Empty study requires blockers')
    return {'tasks': tasks, 'sources': sources, 'obligations': obligations, 'attempts': attempts,
            'environments': environments, 'calibration': calibration, 'judged': judged}


def plan(value, sources, blind_id=None):
    fields(value, ('blind_id', 'content', 'rows', 'exclusions', 'uncertainty'))
    require(blind_id is None or value['blind_id'] == blind_id, 'Neutral subject mismatch')
    require(isinstance(value['blind_id'], str) and re.fullmatch('[0-9a-f]{32}', value['blind_id']), 'Invalid neutral ID')
    string(value['content']); strings(value['exclusions'], 256); strings(value['uncertainty'], 256)
    require(not re.search(r'intentline|p2p_plan_only|plan-acceptance|\bp2p\b', json.dumps(value), re.I), 'Visible approach branding')
    rows = {}
    for row in items(value['rows'], 256):
        fields(row, ('id', 'text', 'binding', 'sources'))
        token(row['id']); string(row['text'])
        require(row['id'] not in rows and type(row['binding']) is bool, 'Invalid plan row')
        for citation in items(row['sources'], 64): anchor(citation, sources)
        rows[row['id']] = row
    require(rows, 'Blank neutral output')
    return rows


def citations(value, sources, rows, dimensions):
    fields(dimensions, DIMENSIONS)
    for count in dimensions.values():
        require(type(count) is int and 0 <= count <= 256, 'Invalid adverse count')
    seen, counts, critical = set(), Counter(), False
    for entry in items(value, 1792):
        fields(entry, ('source', 'output_ids', 'dimension', 'finding', 'severity', 'counterexample'))
        anchor(entry['source'], sources)
        require(entry['dimension'] in DIMENSIONS and entry['severity'] in ('coverage', 'material', 'critical'), 'Invalid citation finding')
        ids = items(entry['output_ids'], 256)
        require(len(ids) == len(set(ids)) and set(ids) <= set(rows), 'Unknown output citation ID')
        string(entry['finding'])
        if entry['severity'] != 'coverage':
            string(entry['counterexample']); counts[entry['dimension']] += 1
        else:
            require(entry['counterexample'] is None, 'Coverage is not a defect')
        critical |= entry['severity'] == 'critical'
        seen.add(entry['dimension'])
    require(seen == set(DIMENSIONS) and all(counts[d] == dimensions[d] for d in DIMENSIONS), 'Citation/count coverage mismatch')
    return critical


def calibration_check(study, root):
    value = study['judge_calibration']
    fields(value, ('status', 'protocol', 'judges', 'receipts', 'metrics', 'judging_metrics'))
    require(value['status'] in ('not_run', 'observed', 'failed'), 'Invalid calibration state')
    usage(value['metrics']); usage(value['judging_metrics'])
    judges, receipts = items(value['judges'], 2), items(value['receipts'], 2)
    empty = {'qualified': False, 'controls': 0, 'critical_misses': None, 'false_rejections': None,
             'secondary_errors': None, 'disagreements': None, 'per_control': []}
    if value['protocol'] is None:
        require(value['status'] == 'not_run' and not judges and not receipts, 'Calibration protocol missing')
        require(all(v is None for v in value['metrics'].values()) and all(v is None for v in value['judging_metrics'].values()), 'Unrun judging has usage')
        return empty
    protocol = document(root, value['protocol'], 'protocol')
    fields(protocol, ('record', 'schema_version', 'control_version', 'registered_at', 'rubric_sha256', 'rules', 'judge_config', 'controls'))
    require(protocol['record'] == 'intentline.ai-judge-protocol', 'Invalid judge protocol'); version(protocol['schema_version'])
    token(protocol['control_version'])
    require(protocol['rubric_sha256'] == RUBRIC_SHA256, 'Changed rubric requires a new adapter protocol')
    require(date(protocol['registered_at']) <= date(study['registered_at']), 'Late control registration')
    artifact(root, protocol['rules'], 'instructions')
    fields(protocol['judge_config'], ('model_id', 'version', 'reasoning'))
    for v in protocol['judge_config'].values(): string(v)
    controls, categories, allowed = {}, {}, [protocol['rules']]
    for control in items(protocol['controls'], 1000):
        fields(control, ('id', 'task', 'category', 'inputs', 'plan', 'expected_dimensions', 'critical', 'anchors'))
        token(control['id']); token(control['task'])
        require(control['id'] not in controls and control['task'] in {t['id'] for t in study['tasks']}, 'Invalid control subject')
        require(control['category'] in CONTROL_CATEGORIES and type(control['critical']) is bool, 'Invalid control category')
        inputs = items(control['inputs'], 65)
        task = next(t for t in study['tasks'] if t['id'] == control['task'])
        require(inputs == [task['request']] + task['context'], 'Control corpus differs from task')
        sources = {r['sha256']: artifact(root, r, 'source') for r in inputs}
        rows = plan(document(root, control['plan'], 'neutral'), sources)
        fields(control['expected_dimensions'], DIMENSIONS)
        for count in control['expected_dimensions'].values():
            require(type(count) is int and 0 <= count <= 256, 'Invalid expected control count')
        if control['category'].startswith('positive'):
            require(not control['critical'] and not any(control['expected_dimensions'].values()), 'Positive must be a correct alternative')
        else:
            require(control['expected_dimensions'][CONTROL_DIMENSIONS[control['category']]] > 0, 'Control has no seeded target fault')
        require(control['anchors'], 'Control needs source anchors')
        for citation in items(control['anchors'], 64): anchor(citation, sources)
        controls[control['id']] = (control, sources, rows)
        categories.setdefault(control['task'], set()).add(control['category'])
        allowed.extend(inputs + [control['plan']])
    population_ready = bool(study['tasks']) and all(categories.get(t['id']) == set(CONTROL_CATEGORIES) for t in study['tasks'])
    for task in study['tasks']:
        for category in ('omission', 'authority', 'exception', 'exclusion'):
            population_ready &= any(c['task'] == task['id'] and c['category'] == category and c['critical'] for c, _, _ in controls.values())
    sessions, environments = {}, set()
    grant = document(root, study['authorization'], 'grant') if study['authorization'] else None
    for judge in judges:
        actor(judge, root, 'judge')
        sid = judge['run_or_session_id']
        require(sid not in sessions and judge['environment_id'] not in environments and judge['environment_id'] is not None, 'Judges need distinct sessions/environments')
        require(judge['model_id'] == protocol['judge_config']['model_id'], 'Judge configuration mismatch')
        require(date(protocol['registered_at']) <= date(judge['timestamp']) <= date(study['registered_at']), 'Judge calibration chronology mismatch')
        require(all(ref in allowed for ref in judge['context_access']), 'Judge can access hidden answers/labels')
        require(protocol['rules'] in judge['context_access'], 'Judge rules absent from context')
        require(grant and protocol['judge_config'] in grant['models'] and judge['environment_id'] in grant['host_ids'], 'Judge outside bounded grant')
        sessions[sid] = judge; environments.add(judge['environment_id'])
    predictions, seen = {}, set()
    for ref in receipts:
        receipt = document(root, ref, 'calibration')
        fields(receipt, ('judge_session_id', 'protocol_sha256', 'timestamp', 'predictions'))
        sid = receipt['judge_session_id']
        require(sid in sessions and sid not in seen and receipt['protocol_sha256'] == value['protocol']['sha256'], 'Calibration identity swap')
        seen.add(sid)
        require(date(protocol['registered_at']) <= date(receipt['timestamp']) <= date(study['registered_at']), 'Calibration must precede planning')
        by_control = {}
        for prediction in items(receipt['predictions'], 1000):
            fields(prediction, ('control_id', 'dimensions', 'critical', 'citations'))
            cid = prediction['control_id']
            require(cid in controls and cid not in by_control and type(prediction['critical']) is bool, 'Invalid prediction population')
            control, sources, rows = controls[cid]
            require(citations(prediction['citations'], sources, rows, prediction['dimensions']) == prediction['critical'], 'Prediction critical state contradicts citations')
            require(all(r in sessions[sid]['context_access'] for r in control['inputs'] + [control['plan']]), 'Judge missing actual calibration inputs')
            by_control[cid] = prediction
        predictions[sid] = by_control
    if value['status'] == 'not_run':
        require(not judges and not receipts and all(v is None for v in value['metrics'].values())
                and all(v is None for v in value['judging_metrics'].values()), 'Unrun calibration has results/usage')
    full = len(predictions) == 2 and all(set(p) == set(controls) for p in predictions.values())
    misses, rejections, errors, disagreements, per_control = 0, 0, 0, 0, []
    for i, (cid, (control, _, _)) in enumerate(controls.items()):
        actual = [p[cid] for p in predictions.values() if cid in p]
        miss = sum(control['critical'] and (not p['critical'] or any(control['expected_dimensions'][d] and not p['dimensions'][d] for d in DIMENSIONS)) for p in actual)
        reject = sum(control['category'].startswith('positive') and (p['critical'] or any(p['dimensions'].values())) for p in actual)
        error = sum(p['dimensions'] != control['expected_dimensions'] for p in actual)
        dissent = len(actual) == 2 and (actual[0]['dimensions'] != actual[1]['dimensions'] or actual[0]['critical'] != actual[1]['critical'])
        misses += miss; rejections += reject; errors += error; disagreements += dissent
        per_control.append({'number': i+1, 'predictions': len(actual), 'critical_misses': miss, 'false_rejections': reject,
                            'secondary_errors': error, 'disagreement': bool(dissent)})
    qualified = value['status'] == 'observed' and population_ready and full and not misses and not rejections
    return {'qualified': qualified, 'controls': len(controls), 'critical_misses': misses if predictions else None,
            'false_rejections': rejections if predictions else None, 'secondary_errors': errors if predictions else None,
            'disagreements': disagreements if predictions else None, 'per_control': per_control}


def scores_check(study, root, sources, obligations, calibration):
    judges = {j['run_or_session_id']: j for j in study['judge_calibration']['judges']}
    all_scores, scoring_sessions = {}, set()
    for run in study['assignments']:
        if run['neutral'] is None:
            require(not run['scores'] and run['mapping'] is None, 'Score without neutral output')
            continue
        require(run['output'] and run['mapping'] and run['state'] == 'completed', 'Neutral output requires completed original and mapping')
        source = sources[run['task']]
        neutral = document(root, run['neutral'], 'neutral')
        rows = plan(neutral, source, run['blind_id'])
        raw = document(root, run['output'], 'output')
        fields(raw, ('branding', 'content', 'rows', 'exclusions', 'uncertainty'))
        require(raw['branding'] in ARMS and {k: v for k, v in neutral.items() if k != 'blind_id'} == {k: v for k, v in raw.items() if k != 'branding'}, 'Normalization changed material content')
        mapping = document(root, run['mapping'], 'mapping')
        fields(mapping, ('blind_id', 'task', 'arm', 'raw_sha256', 'neutral_sha256', 'removed_fields'))
        require(all(mapping[k] == run[k] for k in ('blind_id', 'task', 'arm')) and mapping['raw_sha256'] == run['output']['sha256']
                and mapping['neutral_sha256'] == run['neutral']['sha256'] and mapping['removed_fields'] == ['branding'], 'Normalization mapping mismatch')
        scores, scorers = [], set()
        for ref in run['scores']:
            score = document(root, ref, 'score')
            fields(score, ('blind_id', 'neutral_sha256', 'judge_session_id', 'timestamp', 'dimensions', 'critical',
                           'adjudication', 'citations', 'coverage', 'row_support', 'context'))
            sid = score['judge_session_id']
            require(sid in judges and sid not in scorers and score['blind_id'] == run['blind_id']
                    and score['neutral_sha256'] == run['neutral']['sha256'], 'Score subject/session mismatch')
            scorers.add(sid)
            judge = judges[sid]
            require(sid != document(root, run['execution'], 'execution')['session_id'], 'Planner cannot judge its own output')
            require(all(r in judge['context_access'] for r in run['inputs']), 'Judge missing original sources')
            context = document(root, score['context'], 'agent_receipt')
            fields(context, ('session_id', 'environment_id', 'judge_session_id', 'model_config', 'inputs', 'fresh_context', 'started_at'))
            protocol = document(root, study['judge_calibration']['protocol'], 'protocol')
            require(context['judge_session_id'] == sid and context['model_config'] == protocol['judge_config']
                    and context['inputs'] == run['inputs'] + [run['neutral'], protocol['rules']]
                    and context['fresh_context'] is True, 'Judge scoring context exposes hidden labels/history')
            token(context['session_id']); token(context['environment_id'])
            require(context['session_id'] not in scoring_sessions and context['session_id'] not in judges
                    and context['session_id'] not in {document(root, r['execution'], 'execution')['session_id']
                                                      for r in study['assignments'] if r['execution']}, 'Scoring session reused')
            scoring_sessions.add(context['session_id'])
            require(date(score['timestamp']) >= date(document(root, run['execution'], 'execution')['finished_at']), 'Score precedes output')
            require(date(document(root, run['execution'], 'execution')['finished_at']) <= date(context['started_at']) <= date(score['timestamp']), 'Scoring context chronology mismatch')
            require(type(score['critical']) is bool and citations(score['citations'], source, rows, score['dimensions']) == score['critical'], 'Critical adjudication contradicts findings')
            fields(score['adjudication'], ('state', 'reason')); string(score['adjudication']['reason'])
            require(score['adjudication']['state'] in ('clear', 'source_certain', 'contested')
                    and (score['adjudication']['state'] == 'clear') == (not score['critical']), 'Invalid critical adjudication state')
            expected = {o['id']: o for o in obligations[run['task']]}
            coverage = {}
            for entry in items(score['coverage'], 256):
                fields(entry, ('obligation_id', 'output_ids', 'status', 'source'))
                oid = entry['obligation_id']; ids = items(entry['output_ids'], 256)
                require(oid in expected and oid not in coverage and entry['source'] == expected[oid]['source'], 'Coverage obligation mismatch')
                require(set(ids) <= set(rows) and len(ids) == len(set(ids)) and entry['status'] in ('covered', 'omitted', 'contested'), 'Invalid coverage mapping')
                require((entry['status'] != 'covered' or bool(ids)) and (entry['status'] != 'omitted' or not ids), 'Coverage polarity mismatch')
                require(expected[oid]['uncertainty'] != 'contested' or entry['status'] == 'contested', 'Contested gold cannot become decisive')
                if entry['status'] == 'covered':
                    require(any(entry['source'] in rows[rid]['sources'] for rid in ids), 'Covered obligation lacks row citation')
                if entry['status'] == 'omitted':
                    require(any(c['severity'] != 'coverage' and not c['output_ids'] and c['source'] == entry['source']
                                and c['dimension'] in ('material_omissions', 'constraint_losses') for c in score['citations']), 'Omission scored clean')
                coverage[oid] = entry
            require(set(coverage) == set(expected), 'Missing source-to-plan coverage')
            support = {}
            for entry in items(score['row_support'], 256):
                fields(entry, ('output_id', 'status', 'source'))
                rid = entry['output_id']
                require(rid in rows and rows[rid]['binding'] and rid not in support and entry['status'] in ('supported', 'unsupported', 'contested'), 'Invalid binding-row support')
                if entry['status'] == 'supported':
                    require(entry['source'] in rows[rid]['sources'], 'Unsupported row cannot be clean')
                    anchor(entry['source'], source)
                else:
                    require(entry['source'] is None, 'Unsupported/contested support must remain explicit')
                    if entry['status'] == 'unsupported':
                        require(any(c['dimension'] == 'invented_obligations' and c['severity'] != 'coverage'
                                    and rid in c['output_ids'] for c in score['citations']), 'Invention scored clean')
                support[rid] = entry
            require(set(support) == {r for r in rows if rows[r]['binding']}, 'Missing plan-to-source coverage')
            scores.append(score)
        all_scores[run['blind_id']] = scores
    return all_scores


def assess(study, root, registration_sha256):
    checked = validate(study, root, registration_sha256)
    tasks, attempts = checked['tasks'], checked['attempts']
    source_ready = len(tasks) >= 3 and len({t['repository'] for t in tasks.values()}) >= 3 and all(
        t['kind'] == 'historical' and t['source_decision'] == 'checked' and t['reference'] and t['critique']
        and checked['obligations'][t['id']] and {'oracle', 'critic'} <= {a['agent_role'] for a in t['agents']}
        and len({a['run_or_session_id'] for a in t['agents']}) == len(t['agents'])
        and not t['contamination']
        for t in tasks.values())
    def permitted(environment, identities, tools, started):
        policy = checked['environments'].get(environment)
        if not policy or set(policy['read_sha256s']) != set(identities) or policy['tools'] != tools:
            return False
        return any(document(absolute(root), ref, 'host_receipt')['environment_id'] == environment
                   and date(document(absolute(root), ref, 'host_receipt')['tested_at']) <= date(started)
                   for ref in study['isolation']['receipts'])
    host_ready = bool(attempts) and len({a['environment_id'] for a in attempts}) == len(attempts) and all(
        permitted(a['environment_id'], a['input_sha256s'] + [study['arms'][a['arm']]['instructions']['sha256']],
                  study['arms'][a['arm']]['tools'], a['started_at']) for a in attempts)
    if study['judge_calibration']['protocol']:
        protocol = document(absolute(root), study['judge_calibration']['protocol'], 'protocol')
        host_ready &= all(permitted(j['environment_id'], [r['sha256'] for r in j['context_access']], [], j['timestamp'])
                          for j in study['judge_calibration']['judges'])
    judge_environments = [j['environment_id'] for j in study['judge_calibration']['judges']]
    score_environments = []
    for scores in checked['judged'].values():
        for score in scores:
            context = document(absolute(root), score['context'], 'agent_receipt')
            score_environments.append(context['environment_id'])
            host_ready &= permitted(context['environment_id'], [r['sha256'] for r in context['inputs']], [], context['started_at'])
    envs = [a['environment_id'] for a in attempts] + judge_environments + score_environments
    host_ready &= len(envs) == len(set(envs))
    qualified = source_ready and host_ready and checked['calibration']['qualified']
    status = ('ai_development_observed' if qualified else 'ai_development_unqualified') if attempts else (
        'offline_prepared' if tasks else 'not_run')
    arms = {}
    for arm in ARMS:
        runs = [r for r in study['assignments'] if r['arm'] == arm]
        arms[arm] = {'assignments': len(runs), 'states': {s: sum(r['state'] == s for r in runs) for s in STATES},
                     'attempted': sum(r['state'] != 'not_run' for r in runs),
                     'usage_all_attempts': totals([r['metrics'] for r in runs]),
                     'usage_completed': totals([r['metrics'] for r in runs if r['state'] == 'completed']),
                     'qualified_scored': sum(len(checked['judged'].get(r['blind_id'], [])) == 2 for r in runs) if qualified else 0,
                     'unqualified_scored': sum(bool(checked['judged'].get(r['blind_id'])) for r in runs) if not qualified else 0,
                     'adverse_counts': {d: sum(max(s['dimensions'][d] for s in checked['judged'][r['blind_id']])
                                              for r in runs if len(checked['judged'].get(r['blind_id'], [])) == 2)
                                        for d in DIMENSIONS} if qualified else None}
    report = {'record': 'intentline.ai-development-assessment', 'schema_version': 1,
              'mode': 'ai_only_development', 'status': status, 'human_independence': 'unverified',
              'formal_eligible_tasks': 0, 'tasks': len(tasks), 'repositories': len({t['repository'] for t in tasks.values()}),
              'registered_assignments': len(study['population']), 'actual_attempts': len(attempts),
              'gates': {'sources': bool(source_ready), 'isolation': host_ready, 'calibration': checked['calibration']['qualified']},
              'calibration': checked['calibration'], 'arms': arms, 'paired': [],
              'preparation': study['preparation'], 'calibration_usage': study['judge_calibration']['metrics'],
              'judging_usage': study['judge_calibration']['judging_metrics'],
              'all_in_usage': totals([study['preparation'], study['judge_calibration']['metrics'],
                                      study['judge_calibration']['judging_metrics']] + [r['metrics'] for r in study['assignments']]),
              'blockers': study['blockers'], 'decision': study['decision'],
              'limitations': ['AI-only development; AI-derived gold and critics are not human-independent.',
                              'Captured hashes and host receipts do not authenticate model execution or effective isolation.',
                              'Authored controls and offline tests are not measured planning usefulness.',
                              'Unknown usage is null; failures and not_run remain in registered denominators.',
                              'Semantic leakage, public pretrained knowledge and correlated AI errors remain possible.']}
    for i, task in enumerate(tasks.values()):
        paired = {'task_number': i+1, 'arms': {}}
        for arm in ARMS:
            run = next(r for r in study['assignments'] if r['task'] == task['id'] and r['arm'] == arm)
            scores = checked['judged'].get(run['blind_id'], [])
            complete = qualified and len(scores) == 2
            disagreements = sum(scores[0]['dimensions'][d] != scores[1]['dimensions'][d] for d in DIMENSIONS) if len(scores) == 2 else None
            coverage_disputes = (sum(a['status'] != b['status'] for a, b in zip(sorted(scores[0]['coverage'], key=lambda x: x['obligation_id']),
                                                                            sorted(scores[1]['coverage'], key=lambda x: x['obligation_id']))) if len(scores) == 2 else None)
            support_disputes = (sum(a['status'] != b['status'] for a, b in zip(sorted(scores[0]['row_support'], key=lambda x: x['output_id']),
                                                                           sorted(scores[1]['row_support'], key=lambda x: x['output_id']))) if len(scores) == 2 else None)
            critical_disputes = (scores[0]['critical'] != scores[1]['critical'] or scores[0]['adjudication']['state'] != scores[1]['adjudication']['state']) if len(scores) == 2 else None
            unresolved = any(s['adjudication']['state'] == 'contested' or any(c['status'] == 'contested' for c in s['coverage'])
                             or any(c['status'] == 'contested' for c in s['row_support']) for s in scores) or bool(disagreements or coverage_disputes or support_disputes or critical_disputes)
            clean = complete and not unresolved and all(not any(s['dimensions'].values()) for s in scores)
            paired['arms'][arm] = {'state': run['state'], 'judges': len(scores), 'qualified': complete,
                                  'dimension_disagreements': disagreements, 'coverage_disagreements': coverage_disputes,
                                  'support_disagreements': support_disputes, 'critical_disagreement': critical_disputes,
                                  'unresolved': unresolved, 'clean': clean if complete else None,
                                  'adverse_counts': {d: max(s['dimensions'][d] for s in scores) for d in DIMENSIONS} if complete else None}
        report['paired'].append(paired)
    # All registered assignments remain in the descriptive denominator, including stopped attempts.
    for arm in ARMS:
        clean = sum(p['arms'][arm]['clean'] is True for p in report['paired'])
        arms[arm]['clean_fraction'] = {'numerator': clean, 'denominator': arms[arm]['assignments'],
                                       'wilson_95': interval(clean, arms[arm]['assignments'])} if qualified else None
    if qualified and not any(a['qualified_scored'] for a in arms.values()):
        report['status'] = 'ai_development_unqualified'
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('validate', 'assess', 'report'))
    parser.add_argument('study'); parser.add_argument('--private-root', required=True)
    parser.add_argument('--registration-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        root, path = absolute(args.private_root), absolute(args.study)
        require(root in path.parents, 'Study must be inside secure root')
        with Directory(root) as directory:
            require(directory.identity.st_uid == os.getuid() and not directory.identity.st_mode & 0o077,
                    'Study root must be owner-only')
        study = load(path)
        require(canonical(study) == snapshot(root, {'path': str(path.relative_to(root)), 'sha256': sha(canonical(study))}), 'Noncanonical study')
        result = assess(study, root, args.registration_sha256)
        if args.operation == 'validate':
            result = {'valid': True, 'mode': 'ai_only_development', 'human_independence': 'unverified'}
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (IntentlineError, OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError, OverflowError):
        print('Invalid or unsafe AI development packet; inspect it privately.', file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
