"""Explicit ready-input export, with no consumer execution or approval."""
from pathlib import Path

from .audits import reports
from .contracts import current, inspect
from .errors import IntentlineError
from .export import check_product_sources
from .native_inspect import inspect_bundle, inspect_payload
from .paths import Directory, absolute, read_file
from .records import canonical, immutable, sha
from .schemas import ADOPTION, AUDIT
from .sources import bundle, freshness


def inspect_native(path):
    try:
        return inspect_bundle(path)
    except (ValueError, OSError, KeyError, TypeError, RecursionError) as exc:
        raise IntentlineError('Native inspection refused: ' + str(exc), 3 if 'unavailable on this host' in str(exc) else 2) from exc


def export_native(work_path, out, product_root=None):
    work_path, target = absolute(work_path), absolute(out)
    if target == work_path or work_path in target.parents or target in work_path.parents:
        raise IntentlineError('Export must be separate from the work directory')
    with Directory(work_path) as work, work.lock():
        manifest, blobs, source_digest = bundle(work)
        c, pointer, history = current(work, manifest, blobs, source_digest)
        status, checked = inspect(work_path)
        if status['exit_code'] or checked != c or c['evidence_gaps'] or any(r['plan_state'] != 'planned' for r in c['requirements']):
            raise IntentlineError('Native input requires a complete fresh undisputed plan; gaps/decisions/stale assertions are not ready')
        for source in manifest['sources']:
            if source['original_location'] and target == absolute(source['original_location']).parent:
                raise IntentlineError('Export cannot target a source directory')
        binding = {ref['source_id'] for category in ('requirements','constraints','out_of_scope') for row in c[category] for ref in row['source_refs']}
        binding_context = {s['source_id'] for s in manifest['sources'] if s['role'] == 'context'} & binding
        if binding_context and product_root is None:
            raise IntentlineError('Native binding context requires explicit --product-root')
        root = absolute(product_root) if product_root else Path(manifest['root'])
        check_product_sources(manifest, binding_context, root)
        files = {'contract.json': canonical(c), 'history.json': canonical(history), 'source-manifest.json': canonical(manifest),
                 'brief.md': b'# Native acceptance input (authorization not established)\n\n' + canonical(c),
                 'inspect_bundle.py': read_file(Path(__file__).with_name('native_inspect.py'))[0]}
        for sid, data in blobs.items(): files['source-' + sid + '.txt'] = data
        continuity_digest = None
        if manifest['schema_version'] == 2:
            from .amendments import archives
            _, archived = archives(work, manifest)
            files.update({'archive-' + name: data for name, data in archived.items()})
            files['initial-contract.json'] = canonical(history[0])
            files['continuity.json'] = work.read('continuity.json')[0]
            files['successor-complete.json'] = work.read('successor-complete.json')[0]
            continuity_digest = sha(files['continuity.json'])
        matching = lambda r: all(r[k] == pointer[k] for k in ('contract_sha256','source_bundle_sha256'))
        # Only non-sensitive provenance identities enter the portable/model-visible bundle.
        provenance = {'authentication':'unverified',
                      'audits':[{'sha256':sha(canonical(r)), 'outcome':r['outcome'],
                                 'reported_independence':r['reported_independence'],'authentication':'unverified'}
                                for r in reports(work,'audits',AUDIT) if matching(r)],
                      'adoptions':[{'sha256':sha(canonical(r)), 'approval_file_sha256':r['approval_file_sha256'],
                                    'assertion':'operator_asserted','authentication':'unverified'}
                                   for r in reports(work,'adoptions',ADOPTION) if matching(r)]}
        envelope = {'record':'intentline.native-handoff','schema_version':1,
                    'authorization':'not_established','consumer_execution':'not_observed', **pointer,
                    'source_chain_sha256':sha(canonical({'source_manifest':manifest,'ancestors':manifest.get('ancestors',[])})),
                    'continuity_sha256':continuity_digest, 'requirement_ids':[r['id'] for r in c['requirements']],
                    'provenance':provenance,'files':{name:sha(data) for name,data in sorted(files.items())}}
        if any(len(data) > 2 * 1024 * 1024 for data in files.values()):
            raise IntentlineError('Native metadata/file exceeds 2 MiB; unsupported excess is not truncated')
        inspect_payload(envelope,files,sha(canonical(envelope)))
        with Directory(target,create=True) as destination, destination.lock():
            try: prior = destination.read('native-manifest.json')[0]
            except FileNotFoundError: prior = None
            if prior is not None and prior != canonical(envelope):
                raise IntentlineError('Output already binds another native export; use a new --out')
            for name,data in files.items():
                try: existing = destination.read(name)[0]
                except FileNotFoundError: destination.write(name,data)
                else:
                    if existing != data: raise IntentlineError('Conflicting native output; existing bytes preserved',3)
            now, checked = inspect(work_path)
            if now['exit_code'] or checked != c or freshness(manifest):
                raise IntentlineError('Native source/assertion changed before completion')
            check_product_sources(manifest,binding_context,root)
            for name,data in files.items():
                if destination.read(name)[0] != data: raise IntentlineError('Native output changed before completion',3)
            immutable(destination,'native-manifest.json',envelope)
    return {**envelope,'out':str(target),'bundle_sha256':sha(canonical(envelope)),
            'summary':'Native candidate input exported; authorization not established, consumer execution not observed'}
