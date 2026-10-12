"""Inspect an advisory bundle or preserve externally supplied handoff evidence."""
import argparse
import json
import sys

from intentline.contracts import inspect
from intentline.errors import IntentlineError
from intentline.paths import Directory, absolute, read_file
from intentline.records import canonical, fields, immutable, load, parse, sha
from intentline.render import markdown, safe
from intentline.sources import bundle
from evaluation.planning_02 import number, require, snapshot


def inspect_handoff(out, work_path, product_root, shape='standalone'):
    require(shape == 'standalone', 'Unsupported parent/prerequisite handoff shape')
    root = absolute(product_root)
    status, contract = inspect(work_path)
    require(status['exit_code'] == 0, 'Stale or blocked acceptance cannot be handed off')
    with Directory(work_path) as work:
        manifest, blobs, source_digest = bundle(work)
    pointer = {k: status[k] for k in ('contract_id', 'revision', 'contract_sha256', 'source_bundle_sha256')}
    view = markdown(contract, status, manifest)
    view += '\n## Direct handoff boundary\n\nPreview / advisory direct brief; never approved-contract authority.\n'
    view += '\nDownstream product root: ' + safe(str(root)) + '\n'
    view += '\nAdditional binding references must be regular tracked files in the clean downstream checkout; Proofline independently checks checkout readiness.\n'
    files = {'contract.json': canonical(contract), 'source-manifest.json': canonical(manifest),
             'source.md': blobs['S1'], 'brief.md': view.encode()}
    files.update({'source-'+sid+'.txt': data for sid, data in blobs.items()})
    expected = {'record': 'intentline.export', 'schema_version': 1, 'format': 'proofline-direct',
                **pointer, 'advisory': True,
                'authority': 'operator_asserted_unverified' if status['status'] == 'ADOPTED_ASSERTED' else 'unapproved',
                'files': {name: sha(data) for name, data in sorted(files.items())}}
    with Directory(out) as exported:
        raw, _ = exported.read('export-manifest.json')
        require(raw == canonical(expected), 'Export completion identity/authority mismatch')
        for name, data in files.items():
            require(exported.read(name)[0] == data, 'Handoff file identity mismatch')
        require(exported.read('export-manifest.json')[0] == raw, 'Completion marker changed during inspection')
    binding = {ref['source_id'] for category in ('requirements', 'constraints', 'out_of_scope')
               for row in contract[category] for ref in row['source_refs']} - {'S1'}
    for source in manifest['sources'][1:]:
        if source['source_id'] in binding:
            require(sha(read_file(root / source['relative_path'])[0]) == source['sha256'],
                    'Binding context missing or changed in downstream checkout')
    now, _ = inspect(work_path)
    require(now['exit_code'] == 0 and all(now[k] == pointer[k] for k in pointer), 'Acceptance changed during handoff inspection')
    return {'record': 'intentline.handoff-inspection', 'schema_version': 1, **pointer,
            'export_manifest_sha256': sha(canonical(expected)),
            'source_sha256': sha(blobs['S1']), 'brief_sha256': sha(files['brief.md']),
            'criterion_ids': [r['id'] for r in contract['requirements']],
            'authority': 'advisory_direct_only', 'live_delivery': 'not_observed',
            'checkout_qualification': 'consumer must independently check clean tracked Git and host boundary'}


def record_evidence(evidence, private_root, out):
    fields(evidence, ['record', 'schema_version', 'state', 'blockers', 'inspection', 'external_records',
                      'candidate_commit', 'coverage', 'usage'])
    require(evidence['record'] == 'intentline.handoff-evidence' and type(evidence['schema_version']) is int and evidence['schema_version'] == 1,
            'Unsupported evidence record')
    require(evidence['state'] in ('not_run', 'blocked_external', 'blocked_trust_gate', 'completed', 'failed', 'interrupted'), 'Unknown outcome')
    root = absolute(private_root)
    require(isinstance(evidence['blockers'], list) and isinstance(evidence['external_records'], list)
            and isinstance(evidence['coverage'], list), 'Evidence disclosures required')
    if evidence['inspection'] is not None:
        snapshot(root, evidence['inspection'])
    for ref in evidence['external_records']:
        snapshot(root, ref)
    if evidence['state'] == 'completed':
        require(evidence['inspection'] is not None and evidence['external_records'] and evidence['candidate_commit'] and evidence['coverage'],
                'Completed execution requires bound actual native/status records and candidate')
    if evidence['state'] in ('not_run', 'blocked_external', 'blocked_trust_gate'):
        require(evidence['blockers'] and not evidence['external_records'] and not evidence['coverage'] and evidence['candidate_commit'] is None,
                'Unattempted run cannot claim native delivery evidence')
    if evidence['candidate_commit'] is not None:
        require(isinstance(evidence['candidate_commit'], str) and len(evidence['candidate_commit']) == 40
                and all(c in '0123456789abcdef' for c in evidence['candidate_commit']), 'Invalid candidate commit')
    fields(evidence['usage'], ['cost', 'tokens', 'elapsed_seconds'])
    for value in evidence['usage'].values():
        number(value, nullable=True)
    if evidence['state'] in ('not_run', 'blocked_external', 'blocked_trust_gate'):
        require(all(v is None for v in evidence['usage'].values()), 'Unattempted usage must be null')
    retained = {**evidence, 'authentication': 'unverified',
                'qualification': 'externally supplied evidence; Intentline does not authenticate proof or approval'}
    with Directory(out, create=True) as records, records.lock():
        digest = immutable(records, sha(canonical(retained))+'.json', retained)
    return {'evidence_sha256': digest, 'state': evidence['state'], 'authentication': 'unverified'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True)
    check = sub.add_parser('inspect')
    for option in ('out', 'work', 'product-root'):
        check.add_argument('--'+option, required=True)
    record = sub.add_parser('record')
    for option in ('evidence', 'private-root', 'out'):
        record.add_argument('--'+option, required=True)
    args = parser.parse_args(argv)
    try:
        result = (inspect_handoff(args.out, args.work, args.product_root) if args.operation == 'inspect'
                  else record_evidence(load(args.evidence), args.private_root, args.out))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (IntentlineError, OSError, ValueError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return exc.code if isinstance(exc, IntentlineError) else 3


if __name__ == '__main__':
    sys.exit(main())
