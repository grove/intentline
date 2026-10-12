"""Read-only lineage comparison; allocation/adoption never transfers."""
from .errors import IntentlineError
from .paths import Directory
from .records import canonical, parse, sha
from .review import difference
from .slice_records import saved, subject, unchanged


def impact(work_path, successor_path):
    with Directory(work_path) as work:
        manifest,blobs,current,pointer,history,parent=subject(work)
        plan,plans=saved(work,manifest,blobs,history)
        if not plan:raise IntentlineError('BLOCKED: no recorded slicing recommendation')
        old=history[plan['parent']['revision']-1]
        before_digest=sha(canonical(old))
        with Directory(successor_path) as successor:
            new_manifest,new_blobs,new,new_pointer,new_history,new_parent=subject(successor)
            chain=[]
            if new_manifest['schema_version']==2:
                from .amendments import archives
                _,files=archives(successor,new_manifest)
                chain=[parse(files[d+'.json']) for d in reversed(new_manifest['ancestors'])]
            chain.append({'manifest':new_manifest,'history':new_history,
                          'continuity':parse(successor.read('continuity.json')[0]) if new_manifest['schema_version']==2 else None})
            position=next(((i,j) for i,snapshot in enumerate(chain) for j,c in enumerate(snapshot['history'])
                           if sha(canonical(c))==before_digest and c['source_bundle_sha256']==plan['parent']['source_bundle_sha256']),None)
            if position is None:raise IntentlineError('BLOCKED: missing/unrelated continuity; cannot guess allocation transfer')
            mappings=[]
            start,revision=position
            for index,snapshot in enumerate(chain[start:],start):
                if index>start:mappings.append({'kind':'source_successor','record':snapshot['continuity']})
                for c in snapshot['history'][(revision+1 if index==start else 1):]:
                    mappings.append({'kind':'same_source_revision','record':c['change_notes'][-1]})
            diff=difference(old,new)
            changed={r['id'] for r in diff['removed']} | {r['after']['id'] for r in diff['changed']}
            identity_changed=plan['parent']!=new_parent
            affected=[c['id'] for c in plan['children'] if identity_changed or any(changed & set(r['parent_requirement_ids']) for r in c['requirements'])]
            unchanged(successor,new_pointer,new_manifest)
            if work.read('current.json')[0]!=canonical(pointer) or saved(work,manifest,blobs,history)[0]!=plan:
                raise IntentlineError('Prior parent/plan changed during impact',3)
            return {'status':'IMPACT_REVIEW_REQUIRED' if identity_changed else 'UNCHANGED_INPUTS',
                    'kind':'mechanical','semantic_equivalence':'not_established','authorization':'not_transferred',
                    'prior_parent':plan['parent'],'successor_parent':new_parent,'plan_sha256':sha(canonical(plan)),
                    'diff':diff,'lineage_mappings':mappings,'potentially_affected_children':affected,
                    'potentially_affected_prerequisites':plan['prerequisites'] if affected else [],
                    'potentially_affected_parent_checks':plan['parent_final_checks'] if identity_changed else [],
                    'unchanged_candidate_ids':diff['unchanged_ids'],
                    'summary':'Mechanical impact only; review a fresh bound allocation before recording or exporting'}
