"""Inspect advisory child data without importing peers or executing bundle code."""
import json
import sys

from . import native_inspect as native
from . import slicing


def child_view(plan, contract, child_id):
    child=next((c for c in plan['children'] if c['id']==child_id),None)
    native.require(child is not None, 'Unknown child ID')
    return {'record':'intentline.slice-contribution','schema_version':1,
            'parent':plan['parent'],'plan_sha256':native.sha(native.canonical(plan)),
            'child_acceptance':'not_established','child':child,
            'qualified_criterion_ids':[child_id+':'+r['id'] for r in child['requirements']],
            'constraints':contract['constraints'],'out_of_scope':contract['out_of_scope'],
            'parent_final_checks':plan['parent_final_checks'],'prerequisites':plan['prerequisites']}


def inspect_slice_payload(envelope, files, bundle_digest):
    native.fields(envelope,['record','schema_version','parent','plan_sha256','child_id','authorization',
                            'consumer_execution','child_acceptance','validation','semantics','files'])
    slicing.validate(envelope['parent'],slicing.PARENT)
    slicing.validate(envelope['child_id'],slicing.SID)
    slicing.validate(envelope['plan_sha256'],slicing.DIGEST)
    native.require(envelope['record']=='intentline.slice-handoff' and type(envelope['schema_version']) is int and envelope['schema_version']==1
                   and envelope['authorization']=='not_established' and envelope['consumer_execution']=='not_observed'
                   and envelope['child_acceptance']=='not_established' and envelope['validation']=='structurally_validated'
                   and envelope['semantics']=='unverified','Unsupported child envelope/false authority')
    native.require(set(files)==set(envelope['files']) and all(native.sha(data)==envelope['files'][name] for name,data in files.items()),'Child inventory hash mismatch')
    native.require({'contract.json','history.json','source-manifest.json','plan.json','child.json','inspect_child.py'} <= files.keys(),'Missing child context')
    contract=native.parse(files['contract.json']);manifest=native.parse(files['source-manifest.json'])
    parent=slicing.parent_identity(contract,manifest,native.sha(files['continuity.json']) if manifest['schema_version']==2 else None)
    native.require(parent==envelope['parent'],'Child parent identity mismatch')
    plan=native.parse(files['plan.json'])
    native.require(native.sha(files['plan.json'])==envelope['plan_sha256'] and plan['decision']=='split','Child plan identity/decision mismatch')
    blobs=native.sources(manifest,files)
    slicing.check(plan,contract,manifest,blobs,parent)
    # Reuse full standalone source/history/ancestor validation without native readiness claims.
    parent_files={k:v for k,v in files.items() if k not in ('plan.json','child.json','inspect_child.py')}
    parent_files.update({'brief.md':b'# Native acceptance input (authorization not established)\n\n'+native.canonical(contract),
                         'inspect_bundle.py':b'Advisory parent validation only; no consumer dispatch\n'})
    native_envelope={'record':'intentline.native-handoff','schema_version':1, 'authorization':'not_established',
                     'consumer_execution':'not_observed', **{k:parent[k] for k in ('contract_id','revision','contract_sha256','source_bundle_sha256','source_chain_sha256','continuity_sha256')},
                     'requirement_ids':[r['id'] for r in contract['requirements']],
                     'provenance':{'authentication':'unverified','audits':[],'adoptions':[]},
                     'files':{k:native.sha(v) for k,v in parent_files.items()}}
    native.inspect_payload(native_envelope,parent_files,native.sha(native.canonical(native_envelope)),advisory=True)
    expected=child_view(plan,contract,envelope['child_id'])
    native.require(files['child.json']==native.canonical(expected),'Child contribution/constraints/exclusions changed')
    return {'record':'intentline.slice-inspection','schema_version':1,'bundle_sha256':bundle_digest,
            'parent':parent,'plan_sha256':envelope['plan_sha256'],'child_id':envelope['child_id'],
            'authorization':'not_established','child_acceptance':'not_established','consumer_execution':'not_observed',
            'validation':'structurally_validated','semantics':'unverified','child_view':expected,'files':envelope['files']}


def inspect_slice(path):
    return inspect_slice_payload(*native.read_files(path,'slice-manifest.json'))


def main():
    try:
        native.require(len(sys.argv)==2,'Usage: python -I -B inspect_child.py BUNDLE')
        print(json.dumps(inspect_slice(sys.argv[1]),ensure_ascii=True,sort_keys=True))
    except (ValueError,OSError,KeyError,TypeError,RecursionError) as exc:
        print(str(exc),file=sys.stderr);return 2
    return 0


if __name__=='__main__':sys.exit(main())
