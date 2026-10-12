"""Mechanical continuity accounting; semantic equivalence is never inferred."""
from .errors import IntentlineError
from .paths import Directory
from .records import canonical, immutable, load, parse, sha
from .schemas import CONTINUITY, validate
from .sources import bundle, freshness


def remapped(row, manifest, old_manifest):
    import copy
    result = copy.deepcopy(row)
    sid_map = {s['predecessor_source_id']: s['source_id'] for s in manifest['sources'] if s['provenance'] == 'frozen_historical'}
    for old_source in old_manifest['sources']:
        if old_source['role'] != 'context': continue
        match = next((s for s in manifest['sources'] if s['role'] == 'context' and s['sha256'] == old_source['sha256'] and s['relative_path'] == old_source['relative_path']), None)
        sid_map[old_source['source_id']] = match['source_id'] if match else 'unavailable_historical_context'
    for ref in result['source_refs']:
        ref['source_id'] = sid_map.get(ref['source_id'], ref['source_id'])
    return result


def support(mapping, old_rows, manifest, blobs):
    from .contracts import references
    references(mapping, blobs, manifest)
    if mapping['disposition'] == 'preserved': return
    selected = {ref['source_id'] for ref in mapping['source_refs']}
    required_role = 'amendment' if any(r.get('basis', 'request') != 'project_constraint' for r in old_rows) else 'context'
    if not any(s['source_id'] in selected and s['role'] == required_role and s['provenance'] == 'current' for s in manifest['sources']):
        raise IntentlineError('Changed/retired obligations require new explicit amendment support or current documentary context')


def continuity_check(record, old, new, manifest, blobs, old_manifest):
    validate(record, CONTINUITY)
    expected = {'predecessor_contract_sha256': sha(canonical(old)),
                'predecessor_source_bundle_sha256': old['source_bundle_sha256'],
                'contract_sha256': sha(canonical(new)), 'source_bundle_sha256': new['source_bundle_sha256']}
    if any(record[k] != value for k, value in expected.items()): raise IntentlineError('Continuity subject identity mismatch')
    if new['contract_id'] == old['contract_id'] or new['revision'] != 1:
        raise IntentlineError('Successor requires a distinct contract ID and initial revision 1')
    before = {r['id']: r for r in old['requirements']}
    after = {r['id']: r for r in new['requirements']}
    origins, targets = set(), set()
    for mapping in record['mappings']:
        source, target = set(mapping['from']), set(mapping['to'])
        if len(source) != len(mapping['from']) or len(target) != len(mapping['to']) or not source <= before.keys() or not target <= after.keys() or origins & source or targets & target:
            raise IntentlineError('Missing/unrelated/duplicate continuity mapping IDs')
        kind = mapping['disposition']
        shape = {'preserved': len(source) == len(target) == 1, 'changed': len(source) == len(target) == 1,
                 'retired': not target, 'split': len(source) == 1 and len(target) > 1,
                 'merged': len(source) > 1 and len(target) == 1}
        if not shape[kind]: raise IntentlineError('Continuity disposition/mapping shape mismatch')
        support(mapping, [before[i] for i in source], manifest, blobs)
        if kind == 'preserved':
            origin, destination = mapping['from'][0], mapping['to'][0]
            if origin != destination or remapped(before[origin], manifest, old_manifest) != after[destination]:
                raise IntentlineError('Preserved mapping requires unchanged mechanical row and stable ID; semantic audit still required')
        elif any(i in before and i not in source for i in target):
            raise IntentlineError('Requirement ID aliases an unrelated historical obligation')
        origins.update(source); targets.update(target)
    added = record['added_requirement_ids']
    if origins != before.keys() or len(added) != len(set(added)) or set(added) != after.keys() - targets or set(added) & before.keys():
        raise IntentlineError('Every old obligation and every added requirement needs exact continuity accounting')
    # Constraints and exclusions are material too. Unchanged context references may move IDs.
    accounted = set()
    for mapping in record['other_changes']:
        category, index = mapping['category'], mapping['from_index']
        if index > len(old[category]) or (category, index) in accounted or any(i > len(new[category]) for i in mapping['to_indices']) or len(set(mapping['to_indices'])) != len(mapping['to_indices']):
            raise IntentlineError('Invalid ancillary continuity accounting')
        support({**mapping, 'disposition': 'changed'}, [old[category][index - 1]], manifest, blobs)
        accounted.add((category, index))
    for category in ('constraints', 'out_of_scope'):
        for index, row in enumerate(old[category], 1):
            if (category, index) not in accounted:
                expected_row = remapped(row, manifest, old_manifest)
                if expected_row not in new[category]:
                    raise IntentlineError('Inherited constraint/exclusion omitted or changed without supported continuity')
    return record


def validate_new_identity(draft, old, histories):
    if any(c['contract_id'] == draft['contract_id'] for history in histories for c in history):
        raise IntentlineError('Successor contract ID aliases an ancestor')
    historic_ids = {r['id'] for history in histories for c in history for r in c['requirements']}
    old_ids = {r['id'] for r in old['requirements']}
    if ({r['id'] for r in draft['requirements']} - old_ids) & historic_ids:
        raise IntentlineError('Retired ancestor requirement ID cannot be reused')


def completed(work, manifest, blobs, initial):
    from .amendments import archives
    marker_raw = work.read('successor-complete.json')[0]
    continuity_raw = work.read('continuity.json')[0]
    record = parse(continuity_raw)
    if canonical(record) != continuity_raw or marker_raw != canonical({
            'record': 'intentline.successor-complete', 'schema_version': 1,
            'contract_sha256': sha(canonical(initial)), 'source_bundle_sha256': initial['source_bundle_sha256'],
            'continuity_sha256': sha(continuity_raw)}):
        raise IntentlineError('Incomplete or tampered successor publication', 3)
    predecessor, archived = archives(work, manifest)
    validate_new_identity(initial, predecessor['history'][-1], [parse(data)['history'] for name, data in archived.items() if name.endswith('.json')])
    continuity_check(record, predecessor['history'][-1], initial, manifest, blobs, predecessor['manifest'])
    return record


def reconcile(work_path, draft_path, continuity_path):
    from .amendments import archives
    from .contracts import contract_check, current
    draft, record = load(draft_path), load(continuity_path)
    with Directory(work_path) as work, work.lock():
        manifest, blobs, source_digest = bundle(work)
        if manifest['schema_version'] != 2: raise IntentlineError('Reconcile requires a successor source generation')
        contract_check(draft, manifest, blobs, source_digest)
        predecessor, _ = archives(work, manifest)
        continuity_check(record, predecessor['history'][-1], draft, manifest, blobs, predecessor['manifest'])
        _, archived = archives(work, manifest)
        validate_new_identity(draft, predecessor['history'][-1], [parse(data)['history'] for name, data in archived.items() if name.endswith('.json')])
        try: prior = work.read('current.json')[0]
        except FileNotFoundError: prior = None
        if prior is not None:
            now, pointer, _ = current(work, manifest, blobs, source_digest)
            if now != draft or parse(work.read('continuity.json')[0]) != record:
                raise IntentlineError('Successor already reconciled; use propose for same-source revisions')
            return {**pointer, 'summary': 'Identical complete successor reused'}
        if freshness(manifest): raise IntentlineError('STALE: current successor inputs changed')
        with Directory(work.path / 'revisions', create=True) as revisions:
            contract_digest = immutable(revisions, '000001.json', draft)
        continuity_digest = immutable(work, 'continuity.json', record)
        if freshness(manifest): raise IntentlineError('STALE: source changed before complete reconciliation')
        marker = {'record': 'intentline.successor-complete', 'schema_version': 1,
                  'contract_sha256': contract_digest, 'source_bundle_sha256': source_digest,
                  'continuity_sha256': continuity_digest}
        immutable(work, 'successor-complete.json', marker)
        pointer = {'contract_id': draft['contract_id'], 'revision': 1,
                   'contract_sha256': contract_digest, 'source_bundle_sha256': source_digest}
        work.write('current.json', canonical(pointer), replace=True)
    return {**pointer, 'continuity_sha256': continuity_digest,
            'summary': 'Complete successor DRAFT reconciled; previous adoption remains historical'}
