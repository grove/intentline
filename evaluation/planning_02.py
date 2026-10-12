"""Read-only validation of external planning studies. Never executes an arm."""
import argparse
from collections import Counter
from datetime import datetime
import json
import math
from pathlib import Path
import sys

from intentline.audits import timestamp
from intentline.errors import IntentlineError
from intentline.paths import absolute, read_file
from intentline.records import digest, fields, load, parse, sha, string

ARMS = ('ordinary', 'intentline', 'p2p_plan_only')
STATES = ('completed', 'failed', 'refused', 'timeout', 'interrupted', 'not_run')
DIMENSIONS = ('material_omissions', 'invented_obligations', 'constraint_losses',
              'decision_errors', 'weak_oracles', 'missing_gap_disclosures',
              'unnecessary_blockers')
METRICS = ('elapsed_seconds', 'model_calls', 'tokens', 'cost', 'agent_actions', 'user_actions')


def require(condition, message):
    if not condition:
        raise IntentlineError(message)


def number(value, nullable=False):
    require(value is None and nullable or type(value) in (int, float) and math.isfinite(value) and value >= 0,
            'Expected nonnegative finite measurement or explicitly allowed null')


def snapshot(root, ref):
    fields(ref, ['path', 'sha256'])
    digest(ref['sha256'])
    string(ref['path'])
    require(not Path(ref['path']).is_absolute(), 'Snapshot path must be relative to private root')
    path = absolute(root / ref['path'])
    require(root in path.parents, 'Snapshot outside private root')
    raw, _ = read_file(path)
    require(sha(raw) == ref['sha256'], 'Snapshot identity mismatch')
    return raw


def private_inputs(study):
    """Compare content identities across the whole corpus, including renamed copies."""
    private = {ref['sha256'] for task in study['tasks']
               for ref in ([task['reference']] if task['reference'] is not None else [])
               + [review['record'] for review in task['reviews']]}
    visible = [arm['instructions'] for arm in study['arms'].values()]
    visible += [ref for task in study['tasks'] for ref in [task['request']] + task['context']
                + ([task['parent']] if 'parent' in task else [])]
    require(not private.intersection(ref['sha256'] for ref in visible),
            'Private reference/review content leaked into model-visible inputs')
    return private


def chronology(value, registered_at, review=False):
    timestamp(value)
    date, registered = datetime.fromisoformat(value), datetime.fromisoformat(registered_at)
    require(date <= registered if review else date >= registered,
            'Task review must precede registration' if review else 'Scoring must follow registration')


def validate(study, root):
    root = absolute(root)
    fields(study, ['record', 'schema_version', 'phase', 'registered_at', 'registration',
                   'arms', 'tasks', 'assignments', 'blockers', 'preparation'])
    require(study['record'] == 'intentline.planning-study' and type(study['schema_version']) is int
            and study['schema_version'] == 1, 'Unsupported study')
    require(study['phase'] in ('development', 'pilot', 'holdout'), 'Unknown study phase')
    timestamp(study['registered_at'])
    registration = parse(snapshot(root, study['registration']))
    require(registration == {k: study[k] for k in ('phase', 'registered_at', 'arms', 'tasks')},
            'Registration differs from declared experiment')
    require(isinstance(study['arms'], dict) and set(study['arms']) == set(ARMS), 'Three declared arms required')
    common = None
    for arm in study['arms'].values():
        fields(arm, ['model', 'version', 'reasoning', 'seconds', 'tools', 'differences', 'instructions'])
        for key in ('model', 'version', 'reasoning'):
            if arm[key] is not None:
                string(arm[key])
        number(arm['seconds'], nullable=True)
        require(isinstance(arm['tools'], list) and isinstance(arm['differences'], list), 'Declare host tools and differences')
        snapshot(root, arm['instructions'])
        matched = {k: arm[k] for k in ('model', 'version', 'reasoning', 'seconds', 'tools')}
        require(common is None or common == matched or arm['differences'], 'Unattributed arm differences')
        if common is None:
            common = matched
    require(isinstance(study['blockers'], list) and all(isinstance(x, str) and x.strip() for x in study['blockers']), 'Invalid blockers')
    require(isinstance(study['tasks'], list) and len(study['tasks']) <= 100, 'Invalid task list')
    tasks = {}
    for task in study['tasks']:
        fields(task, ['id', 'kind', 'repository', 'commit', 'license', 'request', 'context', 'scope',
                      'author', 'checker', 'reviews', 'reference', 'eligible'])
        string(task['id'])
        require(task['id'] not in tasks, 'Duplicate task')
        require(task['kind'] in ('real', 'development'), 'Unknown task kind')
        string(task['repository'])
        require(isinstance(task['commit'], str) and len(task['commit']) == 40
                and all(c in '0123456789abcdef' for c in task['commit']), 'Full source commit required')
        string(task['license'])
        string(task['scope'])
        snapshot(root, task['request'])
        require(isinstance(task['context'], list) and len(task['context']) <= 64, 'Invalid task context')
        for ref in task['context']:
            snapshot(root, ref)
        require(type(task['eligible']) is bool, 'Eligibility must be explicit')
        require(isinstance(task['reviews'], list), 'Review records required')
        actors = [task['author'], task['checker']]
        for actor in actors:
            string(actor)
        for review in task['reviews']:
            fields(review, ['actor', 'timestamp', 'conflicts', 'corrections', 'record'])
            string(review['actor'])
            chronology(review['timestamp'], study['registered_at'], review=True)
            require(isinstance(review['conflicts'], list) and isinstance(review['corrections'], list), 'Review disclosures required')
            snapshot(root, review['record'])
            actors.append(review['actor'])
        if task['reference'] is not None:
            snapshot(root, task['reference'])
            require(task['reference'] not in [task['request']] + task['context'], 'Private reference leaked into task inputs')
        require(not any(r['record'] in [task['request']] + task['context'] for r in task['reviews']),
                'Private review leaked into task inputs')
        if task['eligible']:
            require(study['phase'] != 'development' and task['kind'] == 'real', 'Development tasks cannot count as real evidence')
            require(len(task['reviews']) >= 2 and len(actors) == len(set(actors))
                    and not any(r['conflicts'] for r in task['reviews']) and task['reference'] is not None,
                    'Eligible task needs distinct author/checker/two reviewers and reference')
        tasks[task['id']] = task
    private_inputs(study)
    require(isinstance(study['assignments'], list), 'Assignments must include every arm, including failures')
    assignments, blind_ids = set(), set()
    for run in study['assignments']:
        fields(run, ['task', 'arm', 'state', 'blind_id', 'inputs', 'output', 'scores', 'metrics', 'provenance'])
        key = (run['task'], run['arm'])
        require(run['task'] in tasks and run['arm'] in ARMS and key not in assignments, 'Unknown/duplicate assignment')
        assignments.add(key)
        string(run['blind_id'])
        require(run['blind_id'] not in blind_ids, 'Blind IDs must be unique')
        blind_ids.add(run['blind_id'])
        task = tasks[run['task']]
        expected_inputs = [task['request']] + task['context']
        require(run['inputs'] == expected_inputs, 'Every arm must receive the same original sources, without private gold')
        require(run['state'] in STATES, 'Unknown attempt state')
        fields(run['metrics'], METRICS)
        for value in run['metrics'].values():
            number(value, nullable=True)
        require(isinstance(run['provenance'], list), 'Provenance records required')
        for ref in run['provenance']:
            snapshot(root, ref)
        require(isinstance(run['scores'], list), 'Scores must be explicitly listed')
        if run['output'] is not None:
            snapshot(root, run['output'])
        if run['state'] == 'completed':
            require(run['output'] is not None and run['provenance'], 'Completed attempt needs output and execution provenance')
        if run['state'] == 'not_run':
            require(run['output'] is None and not run['scores'] and study['blockers'], 'not_run must not contain output/scores')
            require(all(v is None for v in run['metrics'].values()), 'Unattempted usage is unknown, not zero')
        scorers = set()
        for ref in run['scores']:
            score = parse(snapshot(root, ref))
            fields(score, ['blind_id', 'output_sha256', 'reviewer', 'timestamp', 'blinded', 'conflicts', 'dimensions', 'citations'])
            require(run['output'] is not None and score['output_sha256'] == run['output']['sha256']
                    and score['blind_id'] == run['blind_id'], 'Score subject mismatch')
            chronology(score['timestamp'], study['registered_at'])
            string(score['reviewer'])
            require(score['blinded'] is True and score['conflicts'] == [], 'Unblinded/conflicted score')
            require(score['reviewer'] not in (task['author'], task['checker']) and score['reviewer'] not in scorers,
                    'Score reviewer conflict or duplicate')
            scorers.add(score['reviewer'])
            fields(score['dimensions'], DIMENSIONS)
            for value in score['dimensions'].values():
                require(type(value) is int and value >= 0, 'Dimensions are adverse finding counts')
            require(isinstance(score['citations'], list) and score['citations'], 'Source-to-output scoring coverage required')
            require({c.get('dimension') for c in score['citations'] if isinstance(c, dict)} == set(DIMENSIONS),
                    'Citation coverage required for every dimension')
            for citation in score['citations']:
                fields(citation, ['source_sha256', 'source_lines', 'output_ids', 'dimension', 'finding'])
                require(citation['source_sha256'] in {x['sha256'] for x in expected_inputs}, 'Unknown scoring source')
                require(citation['dimension'] in DIMENSIONS, 'Unknown scoring dimension')
                string(citation['source_lines'])
                require(isinstance(citation['output_ids'], list), 'Output mapping required')
                string(citation['finding'])
        if run['state'] == 'completed' and task['eligible']:
            require(len(scorers) >= 2, 'Completed eligible output needs two blinded scores')
    require(assignments == {(t, a) for t in tasks for a in ARMS}, 'Missing assignment (retain failed/timeout/not_run)')
    fields(study['preparation'], METRICS)
    for value in study['preparation'].values():
        number(value, nullable=True)
    if not tasks:
        require(study['blockers'], 'Empty study requires precise blockers')
    return tasks


def interval(successes, total):
    """Wilson 95% interval for a descriptive proportion, not a superiority test."""
    if total == 0:
        return None
    z = 1.959963984540054
    p, d = successes / total, 1 + z*z / total
    center = (p + z*z / (2*total)) / d
    half = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total)) / d
    return [max(0, center-half), min(1, center+half)]


def assess(study, root):
    tasks = validate(study, root)
    root = absolute(root)
    arms = {}
    for arm in ARMS:
        runs = [r for r in study['assignments'] if r['arm'] == arm]
        eligible = [r for r in runs if tasks[r['task']]['eligible']]
        scores = [parse(snapshot(root, s)) for r in eligible for s in r['scores']]
        # Review disagreements remain visible; sum each dimension's worst reviewer count per assignment.
        counts = {d: sum(max(parse(snapshot(root, s))['dimensions'][d] for s in r['scores'])
                         for r in eligible if r['scores']) for d in DIMENSIONS}
        judged = [r for r in eligible if r['state'] == 'completed' and r['scores']]
        clean = sum(all(all(parse(snapshot(root, s))['dimensions'][d] == 0 for d in DIMENSIONS)
                        for s in r['scores']) for r in judged)
        usage = {m: sum(r['metrics'][m] for r in runs) if runs and all(r['metrics'][m] is not None for r in runs) else None
                 for m in METRICS}
        arms[arm] = {'assignments': len(runs), 'states': dict(Counter(r['state'] for r in runs)),
                     'eligible_assignments': len(eligible), 'judged_completed': len(judged),
                     'adverse_counts': counts if scores else None,
                     'clean_fraction': {'numerator': clean, 'denominator': len(eligible),
                                        'wilson_95': interval(clean, len(eligible))} if judged else None,
                     'usage': usage}
    validate(study, root)
    repos = {t['repository'] for t in tasks.values() if t['eligible']}
    return {'record': 'intentline.planning-assessment', 'schema_version': 1,
            'phase': study['phase'], 'eligible_tasks': sum(t['eligible'] for t in tasks.values()),
            'pilot_minimum_met': sum(t['eligible'] for t in tasks.values()) >= 6 and len(repos) >= 3,
            'authentication': 'unverified', 'arms': arms, 'preparation': study['preparation'],
            'limitations': ['Declared provenance is not authenticated independence.',
                            'Development fixtures are excluded from empirical counts.',
                            'A diagnostic pilot cannot establish broad superiority.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('validate', 'assess', 'report'))
    parser.add_argument('study')
    parser.add_argument('--private-root', required=True)
    args = parser.parse_args(argv)
    try:
        study = load(args.study)
        result = assess(study, args.private_root)
        if args.operation == 'validate':
            result = {'valid': True, 'authentication': 'unverified'}
        # report is a sanitized aggregate, never source text, IDs, paths, answers or actor names.
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (IntentlineError, OSError, ValueError, TypeError, KeyError) as exc:
        print('Invalid study: ' + str(exc), file=sys.stderr)
        return 2 if not isinstance(exc, IntentlineError) else exc.code


if __name__ == '__main__':
    sys.exit(main())
