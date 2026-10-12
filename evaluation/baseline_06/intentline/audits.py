"""Bind externally supplied reports; never invent reviews or independence."""
from datetime import datetime
import os
import re

from .contracts import contract_check, current, references
from .errors import IntentlineError
from .paths import Directory
from .records import canonical, immutable, load, parse, sha
from .schemas import AUDIT, validate
from .sources import bundle, freshness


def timestamp(value):
    try:
        date = datetime.fromisoformat(value)
        if date.tzinfo is None or date.utcoffset() is None:
            raise ValueError('missing offset')
    except ValueError as exc:
        raise IntentlineError('Timestamp must be ISO-8601 with timezone offset') from exc


def subject(work):
    manifest, blobs, source_digest = bundle(work)
    c, pointer, _ = current(work, manifest, blobs, source_digest)
    if freshness(manifest):
        raise IntentlineError('STALE: source identity changed')
    return manifest, blobs, c, pointer


def validate_audit(report, c, manifest, blobs):
    validate(report, AUDIT)
    timestamp(report['timestamp'])
    ids = {r['id'] for r in c['requirements']}
    finding_ids = set()
    for finding in report['findings']:
        if finding['id'] in finding_ids or not set(finding['requirement_ids']) <= ids:
            raise IntentlineError('Invalid/duplicate audit finding identity')
        finding_ids.add(finding['id'])
        references(finding, blobs, manifest)
    if report['outcome'] == 'READY_FOR_ADOPTION' and (report['findings'] or c['open_decisions']):
        raise IntentlineError('A ready audit cannot retain material findings or decisions')
    if report['outcome'] != 'READY_FOR_ADOPTION' and not report['findings']:
        raise IntentlineError('Nonready audit needs a specific evidenced finding')


def audit_record(work_path, report_path):
    report = load(report_path)
    with Directory(work_path) as work, work.lock():
        manifest, blobs, c, pointer = subject(work)
        validate_audit(report, c, manifest, blobs)
        for key in ('contract_sha256', 'source_bundle_sha256'):
            if report[key] != pointer[key]:
                raise IntentlineError('Audit subject identity mismatch')
        if freshness(manifest):
            raise IntentlineError('STALE: source changed before audit recording')
        with Directory(work.path / 'audits', create=True) as audits:
            digest = immutable(audits, sha(canonical(report)) + '.json', report)
    return {'summary':'Audit recorded; actor and reported independence remain unverified',
            'audit_sha256':digest, 'authentication':'unverified', 'reported_independence':report['reported_independence']}


def reports(work, category, schema):
    try:
        directory = Directory(work.path / category)
    except IntentlineError:
        # Absence is normal; symlinks, denied or damaged directories are not.
        try:
            os.stat(category, dir_fd=work.fd, follow_symlinks=False)
        except FileNotFoundError:
            return []
        raise
    result = []
    with directory:
        for name in sorted(os.listdir(directory.fd)):
            if name.startswith('.stage-'):
                continue  # Unpublished interrupted staging bytes are never current records.
            if not re.fullmatch('[0-9a-f]{64}\\.json', name):
                raise IntentlineError('Unexpected immutable record filename', 3)
            raw, _ = directory.read(name)
            value = parse(raw)
            validate(value, schema)
            timestamp(value['timestamp'])
            if canonical(value) != raw or sha(raw) + '.json' != name:
                raise IntentlineError('Immutable audit/adoption identity mismatch', 3)
            result.append(value)
    return result


def readiness(work, c, pointer, manifest, blobs):
    from .adoption import approval_fresh, validate_adoption
    from .schemas import ADOPTION
    audits = reports(work, 'audits', AUDIT)
    adoptions = reports(work, 'adoptions', ADOPTION)
    matching = lambda r: all(r[k] == pointer[k] for k in ('contract_sha256','source_bundle_sha256'))
    active_audits = [r for r in audits if matching(r)]
    active_adoptions = [r for r in adoptions if matching(r)]
    for r in active_audits:
        validate_audit(r, c, manifest, blobs)
    for r in adoptions:
        validate_adoption(r)
    flags = []
    # Disagreement is a material review conflict until explicitly resolved in a new revision.
    adverse = any(r['outcome'] != 'READY_FOR_ADOPTION' for r in active_audits)
    if adverse:
        flags.append('BLOCKED')
    elif active_audits:
        flags.append('READY_FOR_ADOPTION')
    if any(not approval_fresh(r) for r in active_adoptions):
        flags.append('STALE')
    elif active_adoptions and not adverse and not c['open_decisions']:
        flags.append('ADOPTED_ASSERTED')
    return flags, {'audit_records':len(audits), 'current_audits':len(active_audits),
                   'adoption_records':len(adoptions), 'current_adoptions':len(active_adoptions),
                   'authentication':'unverified'}
