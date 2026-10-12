"""Explicitly selected source capture; no discovery or inference."""
from pathlib import Path
import sys

from .errors import IntentlineError
from .paths import Directory, MAX_FILE, absolute, capability, read_file, text
from .records import canonical, digest, fields, integer, parse, sha, string


def capture(source, contexts, root, stdin=None):
    root = absolute(root)
    selected = [source] + contexts
    if len(selected) > 64:
        raise IntentlineError('At most 64 sources')
    rows, blobs, seen = [], {}, set()
    for index, selected_path in enumerate(selected, 1):
        if selected_path == '-':
            if index != 1:
                raise IntentlineError('Only the original request may use stdin')
            data = (sys.stdin.buffer if stdin is None else stdin).read(MAX_FILE + 1)
            origin, relative, identity = None, None, None
        else:
            path = absolute(selected_path)
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError as exc:
                raise IntentlineError('Selected source outside --root') from exc
            data, identity = read_file(path)
            origin = str(path)
            key = (identity['device'], identity['inode'])
            if key in seen:
                raise IntentlineError('Duplicate source file identity')
            seen.add(key)
        if len(data) > MAX_FILE:
            raise IntentlineError('Source exceeds 2 MiB')
        text(data)
        if index == 1 and not data.strip():
            raise IntentlineError('Original request is empty')
        source_id = f'S{index}'
        blobs[source_id] = data
        if sum(len(b) for b in blobs.values()) > 8 * 1024 * 1024:
            raise IntentlineError('Source bundle exceeds 8 MiB')
        rows.append({'source_id': source_id, 'role': 'request' if index == 1 else 'context',
                     'relative_path': relative, 'original_location': origin, 'identity': identity,
                     'declared_authority': 'user_request' if index == 1 else 'unverified_context',
                     'sha256': sha(data), 'bytes': len(data)})
    if sum(len(b) for b in blobs.values()) > 8 * 1024 * 1024:
        raise IntentlineError('Source bundle exceeds 8 MiB')
    return {'manifest': 'intentline.sources', 'schema_version': 1, 'root': str(root), 'sources': rows}, blobs


def prepare(source, contexts, root, out, stdin=None):
    capability()
    manifest, blobs = capture(source, contexts, root, stdin)
    with Directory(out, create=True) as work, work.lock():
        try:
            existing, _ = work.read('source-manifest.json')
        except FileNotFoundError:
            existing = None
        encoded = canonical(manifest)
        if existing is not None and existing != encoded:
            raise IntentlineError('Work item already binds different inputs; use a new work directory')
        with Directory(work.path / 'source', create=True) as snapshots:
            for source_id, data in blobs.items():
                try:
                    before, _ = snapshots.read(source_id + '.txt')
                except FileNotFoundError:
                    snapshots.write(source_id + '.txt', data)
                else:
                    if before != data:
                        raise IntentlineError('Interrupted or corrupted source capture', 3)
        if existing is None:
            if freshness(manifest):
                raise IntentlineError('Source changed before capture publication')
            work.write('source-manifest.json', encoded)
    return {'summary': 'Sources captured; no semantic requirements inferred',
            'work': str(absolute(out)), 'source_bundle_sha256': sha(encoded), 'sources': manifest['sources']}


def bundle(work):
    raw, _ = work.read('source-manifest.json')
    manifest = parse(raw)
    if not isinstance(manifest, dict):
        raise IntentlineError('Invalid source manifest', 3)
    if type(manifest.get('schema_version')) is int and manifest['schema_version'] == 2:
        if canonical(manifest) != raw:
            raise IntentlineError('Noncanonical source manifest', 3)
        from .amendments import successor_bundle
        return successor_bundle(work, manifest, raw)
    fields(manifest, ['manifest', 'schema_version', 'root', 'sources'])
    if manifest['manifest'] != 'intentline.sources' or type(manifest['schema_version']) is not int or manifest['schema_version'] != 1:
        raise IntentlineError('Unsupported source manifest', 3)
    if canonical(manifest) != raw:
        raise IntentlineError('Noncanonical source manifest', 3)
    absolute(manifest['root'])
    rows = manifest['sources']
    if not isinstance(rows, list) or not 1 <= len(rows) <= 64:
        raise IntentlineError('Invalid source count', 3)
    blobs = {}
    with Directory(work.path / 'source') as snapshots:
        for i, row in enumerate(rows, 1):
            fields(row, ['source_id', 'role', 'relative_path', 'original_location', 'identity', 'declared_authority', 'sha256', 'bytes'])
            if row['source_id'] != f'S{i}' or row['role'] != ('request' if i == 1 else 'context'):
                raise IntentlineError('Invalid source ID or role', 3)
            digest(row['sha256'])
            integer(row['bytes'], 0)
            if row['original_location'] is None:
                if i != 1 or row['relative_path'] is not None or row['identity'] is not None:
                    raise IntentlineError('Invalid stdin identity', 3)
            else:
                origin = absolute(row['original_location'])
                relative = origin.relative_to(Path(manifest['root'])).as_posix()
                if row['relative_path'] != relative:
                    raise IntentlineError('Source path identity mismatch', 3)
                fields(row['identity'], ['device', 'inode'])
                integer(row['identity']['device'], 0)
                integer(row['identity']['inode'], 0)
            authority = 'user_request' if i == 1 else 'unverified_context'
            if row['declared_authority'] != authority:
                raise IntentlineError('Unsupported declared authority', 3)
            data, _ = snapshots.read(row['source_id'] + '.txt')
            if sha(data) != row['sha256'] or len(data) != row['bytes']:
                raise IntentlineError('Source snapshot hash mismatch', 3)
            text(data)
            blobs[row['source_id']] = data
    if sum(len(b) for b in blobs.values()) > 8 * 1024 * 1024 or not blobs['S1'].strip():
        raise IntentlineError('Invalid source bundle', 3)
    return manifest, blobs, sha(raw)


def freshness(manifest):
    stale = []
    for row in manifest['sources']:
        if row.get('provenance') == 'frozen_historical' or row['original_location'] is None:
            continue  # Stdin is an explicit frozen input, with no live location to recheck.
        try:
            data, identity = read_file(row['original_location'])
            if sha(data) != row['sha256'] or identity != row['identity']:
                stale.append(row['source_id'])
        except (OSError, IntentlineError):
            stale.append(row['source_id'])
    return stale
