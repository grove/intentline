"""Bounded source generations with portable, immutable predecessor evidence."""
from pathlib import Path

from .errors import IntentlineError
from .paths import Directory, MAX_FILE, absolute, text
from .records import canonical, digest, fields, immutable, integer, parse, sha
from .sources import capture, freshness

MAX_DEPTH = 8
MAX_ARCHIVE = 32 * 1024 * 1024


def validate_v2(manifest):
    fields(manifest, ['manifest', 'schema_version', 'root', 'sources', 'predecessor', 'ancestors'])
    if manifest['manifest'] != 'intentline.sources' or type(manifest['schema_version']) is not int or manifest['schema_version'] != 2:
        raise IntentlineError('Unsupported successor source manifest')
    absolute(manifest['root'])
    ancestors = manifest['ancestors']
    if not isinstance(ancestors, list) or not 1 <= len(ancestors) <= MAX_DEPTH or len(set(ancestors)) != len(ancestors):
        raise IntentlineError('Unsupported ancestor chain: at most eight distinct generations; no truncation')
    for value in ancestors: digest(value)
    predecessor = manifest['predecessor']
    fields(predecessor, ['contract_id', 'revision', 'contract_sha256', 'source_bundle_sha256', 'snapshot_sha256'])
    digest(predecessor['contract_sha256']); digest(predecessor['source_bundle_sha256'])
    integer(predecessor['revision'])
    if predecessor['snapshot_sha256'] != ancestors[0]:
        raise IntentlineError('Predecessor snapshot identity mismatch')
    rows = manifest['sources']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 64:
        raise IntentlineError('Invalid successor source count')
    context_seen = False
    current_amendments = 0
    current_seen = False
    current_identities = set()
    for i, row in enumerate(rows, 1):
        fields(row, ['source_id', 'role', 'relative_path', 'original_location', 'identity', 'declared_authority', 'sha256', 'bytes', 'provenance'], ['predecessor_source_bundle_sha256', 'predecessor_source_id'])
        role = row['role']
        if row['source_id'] != f'S{i}' or role not in ('request', 'amendment', 'context') or (i == 1) != (role == 'request') or (context_seen and role != 'context'):
            raise IntentlineError('Invalid ordered successor sources')
        context_seen |= role == 'context'
        authority = {'request': 'user_request', 'amendment': 'operator_asserted_amendment', 'context': 'unverified_context'}[role]
        if row['declared_authority'] != authority:
            raise IntentlineError('Unsupported source authority')
        digest(row['sha256']); integer(row['bytes'], 0)
        if row['bytes'] > MAX_FILE: raise IntentlineError('Source exceeds 2 MiB')
        if row['provenance'] == 'frozen_historical':
            if current_seen: raise IntentlineError('Historical request/amendments must precede current inputs')
            if role == 'context': raise IntentlineError('Current context must be explicitly recaptured')
            if row.get('predecessor_source_bundle_sha256') != predecessor['source_bundle_sha256']:
                raise IntentlineError('Frozen source predecessor mismatch')
            if not isinstance(row.get('predecessor_source_id'), str): raise IntentlineError('Missing frozen source link')
        elif row['provenance'] == 'current':
            current_seen = True
            if role == 'request' or 'predecessor_source_id' in row or 'predecessor_source_bundle_sha256' in row:
                raise IntentlineError('Invalid current successor source')
            if role == 'amendment': current_amendments += 1
        else: raise IntentlineError('Unsupported source provenance')
        if row['original_location'] is None:
            if row['provenance'] != 'frozen_historical' or row['relative_path'] is not None or row['identity'] is not None:
                raise IntentlineError('Invalid frozen stdin identity')
        else:
            origin = absolute(row['original_location'])
            # Frozen locations are historical labels; their root belongs to the archive.
            if row['provenance'] == 'current' and origin.relative_to(Path(manifest['root'])).as_posix() != row['relative_path']:
                raise IntentlineError('Current source path identity mismatch')
            fields(row['identity'], ['device', 'inode'])
            integer(row['identity']['device'], 0); integer(row['identity']['inode'], 0)
            if row['provenance'] == 'current':
                key = (row['identity']['device'], row['identity']['inode'])
                if key in current_identities: raise IntentlineError('Duplicate current source identity')
                current_identities.add(key)
        if row['relative_path'] is not None:
            path = row['relative_path']
            if not isinstance(path, str) or path.startswith('/') or '\\' in path or any(p in ('', '.', '..') for p in path.split('/')):
                raise IntentlineError('Unsafe source relative path')
    if current_amendments > 1: raise IntentlineError('A generation accepts one new exact amendment')


def validate_archived_v1(manifest):
    fields(manifest, ['manifest', 'schema_version', 'root', 'sources'])
    if manifest['manifest'] != 'intentline.sources' or type(manifest['schema_version']) is not int or manifest['schema_version'] != 1:
        raise IntentlineError('Unsupported archived original manifest')
    root = absolute(manifest['root'])
    if not isinstance(manifest['sources'], list) or not 1 <= len(manifest['sources']) <= 64:
        raise IntentlineError('Invalid archived source count')
    for i, row in enumerate(manifest['sources'], 1):
        fields(row, ['source_id', 'role', 'relative_path', 'original_location', 'identity', 'declared_authority', 'sha256', 'bytes'])
        if row['source_id'] != f'S{i}' or row['role'] != ('request' if i == 1 else 'context') or row['declared_authority'] != ('user_request' if i == 1 else 'unverified_context'):
            raise IntentlineError('Invalid archived original role/identity')
        digest(row['sha256']); integer(row['bytes'], 0)
        if row['bytes'] > MAX_FILE: raise IntentlineError('Archived source exceeds 2 MiB')
        if row['original_location'] is None:
            if i != 1 or row['relative_path'] is not None or row['identity'] is not None:
                raise IntentlineError('Invalid archived stdin source')
        else:
            if absolute(row['original_location']).relative_to(root).as_posix() != row['relative_path']:
                raise IntentlineError('Archived source path mismatch')
            fields(row['identity'], ['device', 'inode'])
            integer(row['identity']['device'], 0); integer(row['identity']['inode'], 0)


def archives(work, manifest):
    """Validate all ancestors from oldest to newest, never following live origins."""
    from .contracts import contract_check, revision_check
    from .continuity import continuity_check, validate_new_identity
    snapshots, files = [], {}
    with Directory(work.path / 'archive') as archive:
        for index, digest_value in enumerate(manifest['ancestors']):
            name = digest_value + '.json'
            raw, _ = archive.read(name)
            if sha(raw) != digest_value: raise IntentlineError('Tampered predecessor snapshot')
            snapshot = parse(raw)
            if canonical(snapshot) != raw: raise IntentlineError('Noncanonical predecessor')
            fields(snapshot, ['record', 'schema_version', 'manifest', 'history', 'continuity'])
            if snapshot['record'] != 'intentline.predecessor' or type(snapshot['schema_version']) is not int or snapshot['schema_version'] != 1:
                raise IntentlineError('Unsupported predecessor snapshot')
            previous = snapshot['manifest']
            if previous.get('schema_version') == 2:
                validate_v2(previous)
                if previous['ancestors'] != manifest['ancestors'][index + 1:]:
                    raise IntentlineError('Missing or unrelated historical continuity chain')
            elif previous.get('schema_version') == 1:
                fields(previous, ['manifest', 'schema_version', 'root', 'sources'])
                if previous.get('manifest') != 'intentline.sources' or index != len(manifest['ancestors']) - 1:
                    raise IntentlineError('Invalid original predecessor')
                validate_archived_v1(previous)
            else: raise IntentlineError('Unsupported archived source schema')
            blobs = {}
            for row in previous['sources']:
                digest(row['sha256'])
                source_name = row['sha256'] + '.txt'
                data, _ = archive.read(source_name)
                if sha(data) != row['sha256'] or len(data) != row['bytes']:
                    raise IntentlineError('Tampered predecessor source capture')
                text(data); blobs[row['source_id']] = data
                files[source_name] = data
            if sum(map(len, blobs.values())) > 8 * 1024 * 1024 or not blobs.get('S1', b'').strip():
                raise IntentlineError('Invalid archived active source bundle')
            files[name] = raw
            if sum(map(len, files.values())) > MAX_ARCHIVE:
                raise IntentlineError('Ancestor snapshot exceeds 32 MiB; no silent truncation')
            history = snapshot['history']
            if not isinstance(history, list) or not history: raise IntentlineError('Missing predecessor contract history')
            for n, c in enumerate(history, 1):
                contract_check(c, previous, blobs, sha(canonical(previous)))
                if c['revision'] != n: raise IntentlineError('Invalid predecessor revision history')
                if n > 1: revision_check(history[n - 2], c, history[:n - 1])
            snapshots.append((snapshot, blobs))
    for index in range(len(snapshots) - 1, -1, -1):
        snapshot, blobs = snapshots[index]
        previous = snapshot['manifest']
        if previous['schema_version'] == 2:
            ancestor, ancestor_blobs = snapshots[index + 1]
            validate_link(previous, blobs, ancestor)
            validate_new_identity(snapshot['history'][0], ancestor['history'][-1], [older['history'] for older, _ in snapshots[index + 1:]])
            continuity_check(snapshot['continuity'], ancestor['history'][-1], snapshot['history'][0], previous, blobs, ancestor['manifest'])
        elif snapshot['continuity'] is not None: raise IntentlineError('Unexpected original continuity')
    first = snapshots[0][0]
    if identity(first) != manifest['predecessor']:
        raise IntentlineError('Sealed predecessor identity mismatch')
    for index, (snapshot, _) in enumerate(snapshots):
        historical_ids = {c['contract_id'] for older, _ in snapshots[index + 1:] for c in older['history']}
        if snapshot['history'][-1]['contract_id'] in historical_ids:
            raise IntentlineError('Reused ancestor contract ID')
    return first, files


def identity(snapshot):
    c = snapshot['history'][-1]
    return {'contract_id': c['contract_id'], 'revision': c['revision'],
            'contract_sha256': sha(canonical(c)), 'source_bundle_sha256': sha(canonical(snapshot['manifest'])),
            'snapshot_sha256': sha(canonical(snapshot))}


def validate_link(manifest, blobs, predecessor):
    if identity(predecessor) != manifest['predecessor']:
        raise IntentlineError('Unrelated predecessor identity')
    old_rows = [r for r in predecessor['manifest']['sources'] if r['role'] in ('request', 'amendment')]
    frozen = [r for r in manifest['sources'] if r['provenance'] == 'frozen_historical']
    if len(frozen) != len(old_rows): raise IntentlineError('Original request/amendment chain omitted')
    for old, row in zip(old_rows, frozen):
        if row['predecessor_source_id'] != old['source_id'] or any(row[k] != old[k] for k in
                ('role', 'sha256', 'bytes', 'declared_authority', 'relative_path', 'original_location', 'identity')):
            raise IntentlineError('Frozen source lineage changed')


def successor_bundle(work, manifest, raw):
    validate_v2(manifest)
    blobs = {}
    with Directory(work.path / 'source') as source:
        for row in manifest['sources']:
            data, _ = source.read(row['source_id'] + '.txt')
            if sha(data) != row['sha256'] or len(data) != row['bytes']: raise IntentlineError('Successor source snapshot hash mismatch')
            text(data); blobs[row['source_id']] = data
    if sum(map(len, blobs.values())) > 8 * 1024 * 1024 or not blobs['S1'].strip():
        raise IntentlineError('Invalid successor source bundle')
    predecessor, _ = archives(work, manifest)
    validate_link(manifest, blobs, predecessor)
    return manifest, blobs, sha(raw)


def amend_source(work_path, amendment, contexts, root, out, expected, refresh_context=False):
    from .contracts import current
    from .sources import bundle
    digest(expected)
    if bool(amendment) == bool(refresh_context): raise IntentlineError('Choose one amendment or --refresh-context')
    root, target, old_path = absolute(root), absolute(out), absolute(work_path)
    if target == old_path or target in old_path.parents or old_path in target.parents:
        raise IntentlineError('Successor must use a separate new work directory')
    with Directory(old_path) as old, old.lock():
        previous, previous_blobs, _ = bundle(old)
        c, pointer, history = current(old, previous, previous_blobs, sha(canonical(previous)))
        if expected != pointer['contract_sha256']: raise IntentlineError('Expected predecessor contract digest mismatch')
        prior_files = {}
        if previous['schema_version'] == 2:
            _, prior_files = archives(old, previous)
            continuity = parse(old.read('continuity.json')[0])
        else: continuity = None
        snapshot = {'record': 'intentline.predecessor', 'schema_version': 1,
                    'manifest': previous, 'history': history, 'continuity': continuity}
        snapshot_raw = canonical(snapshot)
        if len(snapshot_raw) > MAX_FILE: raise IntentlineError('Predecessor metadata exceeds 2 MiB snapshot limit; no truncation')
        ancestor_ids = [sha(snapshot_raw)] + previous.get('ancestors', [])
        if len(ancestor_ids) > MAX_DEPTH: raise IntentlineError('Successor exceeds eight ancestor generations; no truncation')
        prior_files[sha(snapshot_raw) + '.json'] = snapshot_raw
        for data in previous_blobs.values(): prior_files[sha(data) + '.txt'] = data
        if sum(map(len, prior_files.values())) > MAX_ARCHIVE: raise IntentlineError('Ancestor archive exceeds 32 MiB; no truncation')
        rows, blobs = [], {}
        for row in previous['sources']:
            if row['role'] not in ('request', 'amendment'): continue
            sid = f'S{len(rows) + 1}'
            rows.append({**{k: v for k, v in row.items() if k not in ('provenance', 'predecessor_source_bundle_sha256', 'predecessor_source_id')},
                         'source_id': sid, 'provenance': 'frozen_historical',
                         'predecessor_source_bundle_sha256': pointer['source_bundle_sha256'], 'predecessor_source_id': row['source_id']})
            blobs[sid] = previous_blobs[row['source_id']]
        selected = ([amendment] if amendment else []) + contexts
        if selected:
            fresh, fresh_blobs = capture(selected[0], selected[1:], root)
            for i, row in enumerate(fresh['sources']):
                sid = f'S{len(rows) + 1}'
                role = 'amendment' if amendment and i == 0 else 'context'
                rows.append({**row, 'source_id': sid, 'role': role, 'provenance': 'current',
                             'declared_authority': 'operator_asserted_amendment' if role == 'amendment' else 'unverified_context'})
                blobs[sid] = fresh_blobs[row['source_id']]
        if refresh_context:
            old_context = [(r['relative_path'], r['sha256'], r['identity']) for r in previous['sources'] if r['role'] == 'context']
            new_context = [(r['relative_path'], r['sha256'], r['identity']) for r in rows if r['role'] == 'context']
            if old_context == new_context: raise IntentlineError('Context refresh requires changed sources or explicit replacement context')
        manifest = {'manifest': 'intentline.sources', 'schema_version': 2, 'root': str(root),
                    'sources': rows, 'predecessor': identity(snapshot), 'ancestors': ancestor_ids}
        validate_v2(manifest)
        if sum(map(len, blobs.values())) > 8 * 1024 * 1024: raise IntentlineError('Source bundle exceeds 8 MiB')
        # All validation precedes output creation; predecessor changes are rechecked before publication.
        with Directory(target, create=True) as work, work.lock():
            try: existing = work.read('source-manifest.json')[0]
            except FileNotFoundError: existing = None
            if existing is not None and existing != canonical(manifest):
                raise IntentlineError('Successor output already binds different inputs; use a new directory')
            with Directory(target / 'archive', create=True) as archive:
                for name, data in prior_files.items():
                    try: before = archive.read(name)[0]
                    except FileNotFoundError: archive.write(name, data)
                    else:
                        if before != data: raise IntentlineError('Conflicting archived evidence', 3)
            with Directory(target / 'source', create=True) as source:
                for sid, data in blobs.items():
                    try: before = source.read(sid + '.txt')[0]
                    except FileNotFoundError: source.write(sid + '.txt', data)
                    else:
                        if before != data: raise IntentlineError('Conflicting successor capture', 3)
            if freshness(manifest): raise IntentlineError('Source changed before successor capture publication')
            if current(old)[1] != pointer or bundle(old)[0] != previous:
                raise IntentlineError('Predecessor changed before successor publication', 3)
            immutable(work, 'source-manifest.json', manifest)
    return {'work': str(target), 'source_bundle_sha256': sha(canonical(manifest)), 'sources': rows,
            'predecessor': manifest['predecessor'], 'summary': 'Successor sources captured; reconciliation and new external adoption required'}
