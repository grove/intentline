"""Portable advisory outputs; no execution, network, or downstream approval."""
from pathlib import Path

from .contracts import current, inspect
from .errors import IntentlineError
from .paths import Directory, absolute, read_file
from .records import canonical, immutable, sha
from .render import markdown, safe
from .sources import bundle, freshness


def check_product_sources(manifest, binding_ids, root):
    for source in manifest['sources'][1:]:
        if source['source_id'] not in binding_ids:
            continue
        try:
            data, _ = read_file(root / source['relative_path'])
            if sha(data) != source['sha256']:
                raise IntentlineError('hash mismatch')
        except (OSError, IntentlineError) as exc:
            raise IntentlineError('Unsupported handoff shape: binding project reference unavailable in exact product checkout') from exc


def export(work_path, format_name, out, product_root=None):
    if format_name not in ('proofline-direct','markdown','json'):
        raise IntentlineError('Unsupported export format')
    target = absolute(out)
    work_path = absolute(work_path)
    if target == work_path or work_path in target.parents or target in work_path.parents:
        raise IntentlineError('Export must be separate from the work directory')
    with Directory(work_path) as work, work.lock():
        manifest, blobs, source_digest = bundle(work)
        c, pointer, _ = current(work, manifest, blobs, source_digest)
        status, _ = inspect(work_path)
        if status['exit_code']:
            raise IntentlineError(f"{status['status']}: export requires fresh sources, assertions and settled decisions")
        for row in manifest['sources']:
            if row['original_location'] and target == absolute(row['original_location']).parent:
                raise IntentlineError('Export cannot target a source directory')
        if format_name == 'proofline-direct':
            root = absolute(product_root) if product_root else Path(manifest['root'])
            binding_ids = {ref['source_id'] for category in ('requirements','constraints','out_of_scope')
                           for row in c[category] for ref in row['source_refs']} - {'S1'}
            if binding_ids and product_root is None:
                raise IntentlineError('Unsupported handoff shape: binding context needs explicit --product-root for the downstream checkout')
            check_product_sources(manifest, binding_ids, root)
        view = markdown(c, status, manifest)
        files = {'contract.json':canonical(c), 'source-manifest.json':canonical(manifest)}
        for sid, data in blobs.items():
            files['source-' + sid + '.txt'] = data
        if format_name == 'proofline-direct':
            files['source.md'] = blobs['S1']
            view += '\n## Direct handoff boundary\n\nPreview / advisory direct brief; never approved-contract authority.\n'
            view += '\nDownstream product root: ' + safe(str(root)) + '\n'
            view += '\nAdditional binding references must be regular tracked files in the clean downstream checkout; Proofline independently checks checkout readiness.\n'
            files['brief.md'] = view.encode('utf-8')
        elif format_name == 'markdown':
            files['brief.md'] = view.encode('utf-8')
        export_manifest = {'record':'intentline.export','schema_version':1, 'format':format_name,
                           **pointer, 'advisory':True, 'authority':'unapproved' if status['status'] != 'ADOPTED_ASSERTED' else 'operator_asserted_unverified',
                           'files':{name:sha(data) for name, data in sorted(files.items())}}
        with Directory(target, create=True) as destination, destination.lock():
            # Completion marker is last. Interrupted copies are recoverable only with identical inputs.
            try:
                prior, _ = destination.read('export-manifest.json')
            except FileNotFoundError:
                prior = None
            if prior is not None and prior != canonical(export_manifest):
                raise IntentlineError('Output already binds another export; use a new --out')
            for name, data in files.items():
                try:
                    existing, _ = destination.read(name)
                except FileNotFoundError:
                    destination.write(name, data)
                else:
                    if existing != data:
                        raise IntentlineError('Conflicting export file; existing output is preserved', 3)
            now, _ = inspect(work_path)
            if now['exit_code'] or now['contract_sha256'] != pointer['contract_sha256'] or freshness(manifest):
                raise IntentlineError('Export identity changed before completion; no new completion marker written')
            if format_name == 'proofline-direct':
                check_product_sources(manifest, binding_ids, root)
            immutable(destination, 'export-manifest.json', export_manifest)
    return {'summary':'Advisory preview exported; no downstream execution or approval granted',
            'out':str(target), **export_manifest}
