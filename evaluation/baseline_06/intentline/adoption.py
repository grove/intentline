"""Explicit operator-supplied adoption assertions, not actor authentication."""
from .audits import readiness, subject, timestamp
from .errors import IntentlineError
from .paths import Directory, absolute, read_file, text
from .records import canonical, digest, immutable, parse, sha
from .schemas import ADOPTION, APPROVAL, validate
from .sources import freshness


def validate_adoption(record):
    validate(record, ADOPTION)
    timestamp(record['timestamp'])
    original = record['approval_file_bytes_utf8'].encode('utf-8')
    if sha(original) != record['approval_file_sha256']:
        raise IntentlineError('Adoption reference bytes mismatch', 3)
    approval = parse(original)
    validate(approval, APPROVAL)
    for key in approval:
        if key not in ('record',) and record.get(key) != approval[key]:
            raise IntentlineError('Adoption approval binding mismatch', 3)


def approval_fresh(record):
    try:
        raw, identity = read_file(record['approval_file_path'])
        return sha(raw) == record['approval_file_sha256'] and identity == record['approval_file_identity']
    except (OSError, IntentlineError):
        return False


def adopt(work_path, expected, approval_path):
    digest(expected)
    raw, identity = read_file(approval_path)
    approval = parse(raw)
    validate(approval, APPROVAL)
    timestamp(approval['timestamp'])
    with Directory(work_path) as work, work.lock():
        manifest, blobs, c, pointer = subject(work)
        if expected != pointer['contract_sha256']:
            raise IntentlineError('Expected contract digest mismatch')
        for key in ('contract_sha256','source_bundle_sha256'):
            if approval[key] != pointer[key]:
                raise IntentlineError('Approval subject identity mismatch')
        flags, _ = readiness(work, c, pointer, manifest, blobs)
        if c['open_decisions'] or 'BLOCKED' in flags:
            raise IntentlineError('BLOCKED: unresolved decision or adverse audit')
        record = {**approval, 'record':'intentline.adoption', 'assertion':'operator_asserted',
                  'authentication':'unverified', 'approval_file_sha256':sha(raw),
                  'approval_file_bytes_utf8':text(raw), 'approval_file_path':str(absolute(approval_path)),
                  'approval_file_identity':identity}
        validate_adoption(record)
        if freshness(manifest):
            raise IntentlineError('STALE: source changed before adoption recording')
        if not approval_fresh(record):
            raise IntentlineError('STALE: approval reference changed before recording')
        with Directory(work.path / 'adoptions', create=True) as adoptions:
            value_digest = immutable(adoptions, sha(canonical(record)) + '.json', record)
    return {'summary':'ADOPTED_ASSERTED: explicit operator assertion; actor is not authenticated',
            'adoption_sha256':value_digest, 'assertion':'operator_asserted', 'authentication':'unverified', **pointer}
