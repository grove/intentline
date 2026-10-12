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
         'protocol': 'restricted/calibration/', 'calibration': 'judging/calibration/'}
USAGE = METRICS + ('input_tokens', 'cached_input_tokens', 'output_tokens',
                   'reasoning_tokens', 'manual_interventions')
BLOCKERS = ('budget', 'host', 'isolation', 'sources', 'calibration')
DECISIONS = ('fix_specific_defect', 'simplify_overhead',
             'insufficient_or_unqualified_evidence', 'expand_new_tasks')
ROLES = ('researcher', 'drafter', 'oracle', 'critic', 'judge')
CANARIES = ('gold', 'other_arm', 'operator_answers', 'network', 'connected_apps')


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
    require(ref['kind'] in KINDS and (kind is None or ref['kind'] == kind), 'Artifact kind mismatch')
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
    lines = text(sources[value['sha256']]).splitlines()
    require(value['line_start'] <= value['line_end'] <= len(lines), 'Citation lines outside source')
    require(value['quote'] == '\n'.join(lines[value['line_start']-1:value['line_end']]), 'Citation quote mismatch')


def actor(value, root, role=None):
    fields(value, ('agent_role', 'model_id', 'run_or_session_id', 'environment_id',
                   'context_access', 'timestamp', 'record'))
    require(value['agent_role'] in ROLES and (role is None or value['agent_role'] == role), 'Invalid AI role')
    for key in ('model_id', 'run_or_session_id'):
        string(value[key])
    if value['environment_id'] is not None:
        token(value['environment_id'])
    date(value['timestamp'])
    for ref in items(value['context_access'], 64):
        artifact(root, ref)
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
            'isolation_policy': study['isolation']['mode']}


def host_gate(study, root):
    isolation = study['isolation']
    fields(isolation, ('mode', 'receipts'))
    require(isolation['mode'] in ('host-enforced', 'shared', 'unverified'), 'Invalid isolation')
    environments = set()
    for ref in items(isolation['receipts'], 100):
        record = document(root, ref, 'host_receipt')
        fields(record, ('environment_id', 'tested_at', 'canaries', 'permissions_sha256', 'witness'))
        token(record['environment_id']); digest(record['permissions_sha256']); string(record['witness'])
        require(date(record['tested_at']) <= date(study['registered_at']), 'Host checks must precede registration')
        fields(record['canaries'], CANARIES)
        require(all(v in ('denied', 'accessible', 'untested') for v in record['canaries'].values()), 'Invalid canary state')
        require(record['environment_id'] not in environments, 'Duplicate environment receipt')
        if all(v == 'denied' for v in record['canaries'].values()):
            environments.add(record['environment_id'])
    return environments if isolation['mode'] == 'host-enforced' else set()


def validate(study, root, registration_sha256):
    root = absolute(root)
    fields(study, ('record', 'schema_version', 'mode', 'phase', 'registered_at', 'registration',
                   'arms', 'tasks', 'population', 'assignments', 'judge_calibration', 'isolation',
                   'preparation', 'blockers', 'decision'))
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
        require(len(source) == len(inputs) and task['request']['sha256'] not in request_hashes, 'Duplicate corpus source key')
        request_hashes.add(task['request']['sha256']); visible.extend(inputs)
        for agent in items(task['agents'], 10):
            actor(agent, root)
            require(date(agent['timestamp']) <= date(study['registered_at']), 'Preparation must precede registration')
            private.append(agent['record'])
        require(task['source_decision'] in ('checked', 'unreviewed'), 'Invalid source decision')
        strings(task['contamination'], 64)
        obligations[task['id']] = ledger(task, root, source)
        private.extend(task[k] for k in ('reference', 'critique') if task[k] is not None)
        tasks[task['id']], sources[task['id']] = task, source
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
    # Reuse the formal evaluator's corpus-wide byte identity guard without its eligibility semantics.
    from evaluation.planning_02 import private_inputs
    private_inputs({'arms': study['arms'], 'tasks': [{'reference': None, 'reviews': [{'record': r} for r in private],
                                                    'request': r, 'context': []} for r in visible]})
    calibration = calibration_check(study, root)
    judged = scores_check(study, root, sources, obligations, calibration)
    if not tasks:
        require(study['blockers'], 'Empty study requires blockers')
    return {'tasks': tasks, 'sources': sources, 'obligations': obligations, 'attempts': attempts,
            'environments': environments, 'calibration': calibration, 'judged': judged}


def calibration_check(study, root):
    value = study['judge_calibration']
    fields(value, ('status', 'protocol', 'judges', 'receipts', 'metrics', 'judging_metrics'))
    require(value['status'] in ('not_run', 'observed', 'failed'), 'Invalid calibration state')
    require(value['protocol'] is None, 'Judging protocol not supported until qualification extension')
    require(not items(value['judges'], 2) and not items(value['receipts'], 2), 'Judging not qualified')
    usage(value['metrics']); usage(value['judging_metrics'])
    require(value['status'] == 'not_run' and all(v is None for v in value['metrics'].values())
            and all(v is None for v in value['judging_metrics'].values()), 'Unrun judging has usage')
    return {'qualified': False, 'controls': 0, 'critical_misses': None, 'false_rejections': None, 'disagreements': None}


def scores_check(study, root, sources, obligations, calibration):
    require(not any(r['scores'] or r['neutral'] or r['mapping'] for r in study['assignments']), 'Scoring extension required')
    return {}


def assess(study, root, registration_sha256):
    checked = validate(study, root, registration_sha256)
    tasks, attempts = checked['tasks'], checked['attempts']
    source_ready = len(tasks) >= 3 and len({t['repository'] for t in tasks.values()}) >= 3 and all(
        t['kind'] == 'historical' and t['source_decision'] == 'checked' and t['reference'] and t['critique']
        and checked['obligations'][t['id']] and {'oracle', 'critic'} <= {a['agent_role'] for a in t['agents']}
        for t in tasks.values())
    host_ready = bool(attempts) and len({a['environment_id'] for a in attempts}) == len(attempts) and all(
        a['environment_id'] in checked['environments'] for a in attempts)
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
                     'qualified_scored': 0, 'adverse_counts': None}
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
        study = load(path)
        require(canonical(study) == snapshot(root, {'path': str(path.relative_to(root)), 'sha256': sha(canonical(study))}), 'Noncanonical study')
        result = assess(study, root, args.registration_sha256)
        if args.operation == 'validate':
            result = {'valid': True, 'mode': 'ai_only_development', 'human_independence': 'unverified'}
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (IntentlineError, OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError):
        print('Invalid or unsafe AI development packet; inspect it privately.', file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
