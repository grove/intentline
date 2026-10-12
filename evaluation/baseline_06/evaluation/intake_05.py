"""Read-only candidate readiness diagnostic. Does not register, score or run tasks."""
import argparse
import json
import os
import re
import sys

from evaluation.planning_02 import private_inputs, require, snapshot
from intentline.audits import timestamp
from intentline.errors import IntentlineError
from intentline.paths import Directory, absolute
from intentline.records import fields, load, parse, sha, string


def inspect(intake, root):
    root = absolute(root)
    with Directory(root) as directory:
        require(directory.identity.st_uid == os.getuid() and not directory.identity.st_mode & 0o077,
                'Study root must be owner-only')
    fields(intake, ['record', 'schema_version', 'captured_at', 'tasks', 'registered_assignments',
                   'executed', 'model_authorization', 'host_isolation', 'blinding_ready', 'cost_permission'])
    require(intake['record'] == 'intentline.task-intake' and type(intake['schema_version']) is int
            and intake['schema_version'] == 1, 'Unsupported intake')
    timestamp(intake['captured_at'])
    require(isinstance(intake['tasks'], list) and len(intake['tasks']) <= 100, 'Invalid candidates')
    require(type(intake['registered_assignments']) is int and intake['registered_assignments'] == 0
            and type(intake['executed']) is int and intake['executed'] == 0,
            'Candidate intake cannot claim registered or executed assignments; use the existing evaluator')
    permissions = {}
    for key in ('model_authorization', 'host_isolation', 'blinding_ready', 'cost_permission'):
        if intake[key] is not None:
            snapshot(root, intake[key])
        permissions[key] = 'missing' if intake[key] is None else 'supplied_unverified'
    ids, projects, candidates = set(), set(), []
    for task in intake['tasks']:
        fields(task, ['id', 'status', 'repository', 'commit', 'license', 'license_capture', 'request',
                      'context', 'provenance', 'scope', 'author', 'checker', 'reviews', 'reference',
                      'slicing_parent', 'blockers'])
        string(task['id'])
        require(task['id'] not in ids, 'Duplicate candidate')
        ids.add(task['id'])
        require(task['status'] == 'candidate_unreviewed', 'Intake cannot assert independent eligibility')
        require(isinstance(task['repository'], str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*/[A-Za-z0-9][A-Za-z0-9_.-]*', task['repository']),
                'Expected upstream owner/repository')
        require(isinstance(task['commit'], str) and re.fullmatch(r'[0-9a-f]{40}', task['commit']), 'Full upstream commit required')
        string(task['license'])
        string(task['scope'])
        projects.add(task['repository'])
        for key in ('request', 'license_capture', 'provenance'):
            snapshot(root, task[key])
        require(isinstance(task['context'], list) and len(task['context']) <= 64, 'Invalid context')
        for ref in task['context']:
            snapshot(root, ref)
        require(isinstance(task['reviews'], list) and len(task['reviews']) <= 10, 'Invalid reviews')
        # These are evidence captures, not inferred identities or authenticated role claims.
        captures = [task[k] for k in ('author', 'checker', 'reference') if task[k] is not None] + task['reviews']
        for ref in captures:
            snapshot(root, ref)
        require(len({ref['sha256'] for ref in captures}) == len(captures), 'Duplicate role/reference captures')
        require(isinstance(task['blockers'], list) and task['blockers']
                and all(isinstance(x, str) and x.strip() for x in task['blockers']), 'Candidate blockers required')
        if task['slicing_parent'] is not None:
            from evaluation.slicing_04 import parent
            parent({**task, 'parent': task['slicing_parent']}, root)
        private = {ref['sha256'] for ref in captures}
        visible = [task['request']] + task['context'] + ([task['slicing_parent']] if task['slicing_parent'] else [])
        require(not private.intersection(ref['sha256'] for ref in visible), 'Private capture leaked into candidate inputs')
        missing = [key for key in ('author', 'checker', 'reference', 'slicing_parent') if task[key] is None]
        if len(task['reviews']) < 2:
            missing.append('two_independent_task_gold_reviews')
        candidates.append({'number': len(candidates) + 1, 'missing': missing,
                           'external_eligibility': 'unverified', 'unresolved_blockers': len(task['blockers'])})
    # Reuse the existing evaluator's corpus-wide hash guard; input aliases across tasks also refuse.
    private = private_inputs({'arms': {}, 'tasks': [{**task, **({'parent': task['slicing_parent']} if task['slicing_parent'] else {}),
                                         'reviews': [{'record': ref} for ref in task['reviews']]
                                         + [{'record': task[k]} for k in ('author', 'checker') if task[k] is not None]}
                                        for task in intake['tasks']]})
    for task in intake['tasks']:
        if task['slicing_parent'] is not None:
            payload = parse(snapshot(root, task['slicing_parent']))
            require(not private.intersection(sha(value.encode('utf-8')) for value in payload['files_utf8'].values()),
                    'Private capture leaked into candidate parent payload')
    return {'record': 'intentline.intake-readiness', 'schema_version': 1,
            'candidate_count': len(candidates), 'project_count': len(projects), 'eligible_count': 0,
            'registered_assignments': 0, 'executed': 0,
            'missing_authors': sum('author' in c['missing'] for c in candidates),
            'missing_checkers': sum('checker' in c['missing'] for c in candidates),
            'missing_independent_reviews': sum('two_independent_task_gold_reviews' in c['missing'] for c in candidates),
            **permissions, 'candidates': candidates, 'authentication': 'unverified',
            'limitations': ['Hashes establish captured byte identity, not upstream authenticity, license rights or independence.',
                            'Owner-only storage does not isolate planning arms sharing the same OS identity.',
                            'External review and a separately frozen existing study registration are required.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('intake')
    parser.add_argument('--private-root', required=True)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(inspect(load(args.intake), args.private_root), sort_keys=True, allow_nan=False))
        return 0
    except (IntentlineError, OSError, ValueError, TypeError, KeyError):
        print('Invalid or unsafe intake; inspect the private packet locally.', file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
