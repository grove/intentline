"""Structure and exact provenance, not semantic completeness."""
import os
import re

from .errors import IntentlineError
from .paths import Directory, text
from .records import canonical, fields, immutable, load, parse, sha
from .schemas import ACCEPTANCE, validate
from .sources import bundle, freshness


def references(row, blobs, manifest):
    roles = {s['source_id']: s['role'] for s in manifest['sources']}
    for ref in row['source_refs']:
        sid = ref['source_id']
        if sid not in blobs:
            raise IntentlineError('Unknown source reference')
        lines = text(blobs[sid]).splitlines(keepends=True)
        start, end = ref['line_start'], ref['line_end']
        if start > end or end > len(lines):
            raise IntentlineError('Invalid source line range')
        exact = ''.join(lines[start - 1:end])
        # Quotes may omit only the final line terminator, never interior bytes.
        if ref['quote'] not in (exact, exact.removesuffix('\n').removesuffix('\r')):
            raise IntentlineError('Quotation mismatch against saved source bytes')
    basis = row.get('basis')
    if basis in ('request', 'necessary_invariant') and not any(roles[r['source_id']] == 'request' for r in row['source_refs']):
        raise IntentlineError('Requested/inferred outcomes require original-request support')
    if basis == 'project_constraint' and not any(roles[r['source_id']] == 'context' for r in row['source_refs']):
        raise IntentlineError('Project constraint requires selected project context')


def contract_check(contract, manifest, blobs, bundle_digest):
    validate(contract, ACCEPTANCE)
    if contract['source_bundle_sha256'] != bundle_digest:
        raise IntentlineError('Source-bundle identity mismatch')
    ids = [r['id'] for r in contract['requirements']]
    if len(ids) != len(set(ids)):
        raise IntentlineError('Duplicate requirement ID')
    decision_ids = [r['id'] for r in contract['open_decisions']]
    if len(decision_ids) != len(set(decision_ids)):
        raise IntentlineError('Duplicate decision ID')
    for category in ('requirements', 'constraints', 'out_of_scope', 'open_decisions'):
        for row in contract[category]:
            references(row, blobs, manifest)
    gap_ids = set()
    for gap in contract['evidence_gaps']:
        if not set(gap['requirement_ids']) <= set(ids):
            raise IntentlineError('Gap refers to unknown requirement')
        gap_ids.update(gap['requirement_ids'])
    for row in contract['requirements']:
        if row['plan_state'] == 'gap' and row['id'] not in gap_ids:
            raise IntentlineError('Gap row requires an explicit evidence-gap reason')
    notes = contract['change_notes']
    if len(notes) != contract['revision'] or [n['revision'] for n in notes] != list(range(1, contract['revision'] + 1)):
        raise IntentlineError('Change notes must retain every numbered revision')
    if notes[0] != {'revision': 1, 'kind': 'initial'}:
        raise IntentlineError('Initial note must record initial creation only')
    for note in notes[1:]:
        if set(note) != {'revision', 'kind', 'reason', 'previous_contract_sha256', 'mappings', 'retired_ids', 'claimed_authority'} or note['kind'] != 'revision':
            raise IntentlineError('Revision needs reason, prior identity, mappings, retirement and claimed authority')
    return contract


def revision_check(previous, new, history):
    if new['contract_id'] != previous['contract_id'] or new['revision'] != previous['revision'] + 1:
        raise IntentlineError('One lineage; require next revision and unchanged contract ID')
    if new['change_notes'][:-1] != previous['change_notes']:
        raise IntentlineError('Historical change notes must remain unchanged')
    note = new['change_notes'][-1]
    if note['previous_contract_sha256'] != sha(canonical(previous)):
        raise IntentlineError('Expected-before contract digest mismatch')
    old = {r['id']: r for r in previous['requirements']}
    current = {r['id']: r for r in new['requirements']}
    all_ids = {r['id'] for c in history for r in c['requirements']}
    if (set(current) - set(old)) & all_ids:
        raise IntentlineError('Retired requirement IDs cannot be reused')
    retired = set(note['retired_ids'])
    if len(retired) != len(note['retired_ids']) or retired != set(old) - set(current):
        raise IntentlineError('Deleted obligations need exact retired-ID accounting')
    covered = set()
    for mapping in note['mappings']:
        origin, target = set(mapping['from']), set(mapping['to'])
        if len(origin) != len(mapping['from']) or len(target) != len(mapping['to']) or not origin <= set(old) or not target <= set(current) or covered & origin:
            raise IntentlineError('Invalid or duplicate revision mapping')
        covered.update(origin)
    changed = {i for i in old if i not in current or old[i] != current[i]}
    if not changed <= covered:
        raise IntentlineError('Changed/deleted obligations need explained revision mappings')


def current(work, manifest=None, blobs=None, source_digest=None):
    if manifest is None:
        manifest, blobs, source_digest = bundle(work)
    pointer_raw, _ = work.read('current.json')
    pointer = parse(pointer_raw)
    fields(pointer, ['contract_id', 'revision', 'contract_sha256', 'source_bundle_sha256'])
    if type(pointer['revision']) is not int or not 1 <= pointer['revision'] <= 999999:
        raise IntentlineError('Corrupt current revision', 3)
    history = []
    with Directory(work.path / 'revisions') as revisions:
        for index in range(1, pointer['revision'] + 1):
            data, _ = revisions.read(f'{index:06}.json')
            c = parse(data)
            if canonical(c) != data:
                raise IntentlineError('Noncanonical contract record', 3)
            contract_check(c, manifest, blobs, source_digest)
            if c['revision'] != index:
                raise IntentlineError('Revision identity mismatch', 3)
            if history:
                revision_check(history[-1], c, history)
            history.append(c)
    last = history[-1]
    expected = {'contract_id': last['contract_id'], 'revision': last['revision'],
                'contract_sha256': sha(canonical(last)), 'source_bundle_sha256': source_digest}
    if pointer != expected or canonical(pointer) != pointer_raw:
        raise IntentlineError('Current pointer hash/identity mismatch', 3)
    return last, pointer, history


def propose(work_path, draft_path):
    draft = load(draft_path)
    with Directory(work_path) as work, work.lock():
        manifest, blobs, source_digest = bundle(work)
        contract_check(draft, manifest, blobs, source_digest)
        if freshness(manifest):
            raise IntentlineError('STALE: original source identity changed; prepare a new work item')
        try:
            before, pointer, history = current(work, manifest, blobs, source_digest)
        except FileNotFoundError:
            # A pointer may be absent after interruption, but historical records remain immutable.
            try:
                work.read('current.json')
            except FileNotFoundError:
                before, pointer, history = None, None, []
            else:
                raise IntentlineError('Missing historical revision', 3)
        if before == draft:
            return {**pointer, 'summary': 'Unchanged proposal reused; no new revision'}
        if before is None:
            if draft['revision'] != 1:
                raise IntentlineError('Initial proposal must be revision 1')
        else:
            revision_check(before, draft, history)
        with Directory(work.path / 'revisions', create=True) as revisions:
            digest = immutable(revisions, f"{draft['revision']:06}.json", draft)
        if freshness(manifest):
            raise IntentlineError('STALE: source changed before publication')
        if pointer is not None and parse(work.read('current.json')[0]) != pointer:
            raise IntentlineError('Concurrent current-pointer change', 3)
        new_pointer = {'contract_id': draft['contract_id'], 'revision': draft['revision'],
                       'contract_sha256': digest, 'source_bundle_sha256': source_digest}
        work.write('current.json', canonical(new_pointer), replace=True)
    return {**new_pointer, 'summary': 'DRAFT saved; structural validation is not semantic approval'}


def inspect(work_path):
    with Directory(work_path) as work:
        manifest, blobs, digest = bundle(work)
        stale = freshness(manifest)
        try:
            c, pointer, _ = current(work, manifest, blobs, digest)
        except FileNotFoundError:
            return {'flags': ['STALE' if stale else 'BLOCKED'], 'status': 'STALE' if stale else 'BLOCKED',
                    'stale_sources': stale, 'exit_code': 2, 'summary': 'No complete current contract'}, None
        flags = ['DRAFT', 'STRUCTURALLY_VALID']
        if c['open_decisions']:
            flags.append('BLOCKED')
        if stale:
            flags.append('STALE')
        status = 'STALE' if stale else ('BLOCKED' if c['open_decisions'] else 'STRUCTURALLY_VALID')
        return {**pointer, 'flags': flags, 'status': status, 'stale_sources': stale,
                'exit_code': 2 if status in ('STALE', 'BLOCKED') else 0,
                'summary': status + ': structural checks do not establish semantic completeness',
                'evidence_gaps': c['evidence_gaps']}, c
