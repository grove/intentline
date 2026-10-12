"""Optional actor-unverified slicing reports; favorable reports erase nothing."""
import os

from .audits import timestamp
from .contracts import references
from .errors import IntentlineError
from .paths import Directory
from .records import canonical, fields, immutable, parse, sha, digest
from .slice_records import proposal, saved, subject, unchanged
from .slicing import DIGEST, TEXT, REFS, RID, arr, obj, validate

FINDING = obj({'id':{'type':'string','pattern':'^A[1-9][0-9]{0,5}$'},
               'requirement_ids':arr(RID), 'source_refs':REFS,
               'evidence':TEXT,'consequence':TEXT,'correction':TEXT})
AUDIT = obj({'record':{'const':'intentline.slice-audit'},'schema_version':{'const':1},
             'contract_sha256':DIGEST,'source_bundle_sha256':DIGEST,'plan_sha256':DIGEST,
             'actor':TEXT,'timestamp':TEXT,
             'reported_independence':{'enum':['self_check','unverified_independence','independent']},
             'authentication':{'const':'unverified'},
             'outcome':{'enum':['NO_MATERIAL_FINDINGS','CHANGES_NEEDED','BLOCKED']},
             'coverage':TEXT,'findings':arr(FINDING)})


def check(report, plan, contract, manifest, blobs):
    try: validate(report,AUDIT)
    except ValueError as exc: raise IntentlineError('Invalid slice audit: '+str(exc)) from exc
    timestamp(report['timestamp'])
    expected={'plan_sha256':sha(canonical(plan)), **{k:plan['parent'][k] for k in ('contract_sha256','source_bundle_sha256')}}
    if any(report[k] != v for k,v in expected.items()):raise IntentlineError('Slice audit subject mismatch')
    ids={r['id'] for r in contract['requirements']};seen=set()
    for finding in report['findings']:
        if finding['id'] in seen or not set(finding['requirement_ids']) <= ids or len(set(finding['requirement_ids'])) != len(finding['requirement_ids']):
            raise IntentlineError('Invalid/duplicate slice finding identity')
        seen.add(finding['id']);references(finding,blobs,manifest)
    if (report['outcome']=='NO_MATERIAL_FINDINGS') != (not report['findings']):
        raise IntentlineError('Adverse audit needs findings; favorable audit cannot retain material findings')


def reports(work, plans, history, manifest, blobs):
    try:os.stat('slicing',dir_fd=work.fd,follow_symlinks=False)
    except FileNotFoundError:return []
    with Directory(work.path/'slicing') as slices:
        try:os.stat('audits',dir_fd=slices.fd,follow_symlinks=False)
        except FileNotFoundError:return []
    with Directory(work.path/'slicing'/'audits') as directory:
        try:raw=directory.read('index.json')[0]
        except FileNotFoundError:return []
        index=parse(raw);fields(index,['record','schema_version','reports'])
        digests=index['reports']
        if index['record']!='intentline.slice-audit-index' or type(index['schema_version']) is not int or index['schema_version']!=1 or canonical(index)!=raw or not isinstance(digests,list) or len(digests)>256 or not all(isinstance(d,str) for d in digests) or len(set(digests))!=len(digests):
            raise IntentlineError('Corrupt slice audit index',3)
        by_digest={sha(canonical(p)):p for p in plans};result=[]
        for value in digests:
            digest(value);data=directory.read(value+'.json')[0];report=parse(data)
            if sha(data)!=value or canonical(report)!=data:raise IntentlineError('Corrupt slice audit bytes',3)
            try:
                validate(report,AUDIT)
                plan=by_digest[report['plan_sha256']]
                check(report,plan,history[plan['parent']['revision']-1],manifest,blobs)
            except (ValueError,KeyError,TypeError,IntentlineError) as exc:raise IntentlineError('Corrupt slice audit: '+str(exc),3) from exc
            result.append(report)
        if directory.read('index.json')[0]!=raw:raise IntentlineError('Slice audit index changed',3)
        return result


def audit_record(work_path, report_path):
    report=proposal(report_path)
    with Directory(work_path) as work,work.lock():
        manifest,blobs,contract,pointer,history,parent=subject(work)
        plan,plans=saved(work,manifest,blobs,history)
        if not plan or plan['parent']!=parent:raise IntentlineError('No current slice plan for audit')
        check(report,plan,contract,manifest,blobs)
        prior=reports(work,plans,history,manifest,blobs)
        unchanged(work,pointer,manifest)
        if report not in prior:
            if len(prior)>=256:raise IntentlineError('Slice audit history limit')
            with Directory(work.path/'slicing'/'audits',create=True) as directory:
                value=immutable(directory,sha(canonical(report))+'.json',report)
                unchanged(work,pointer,manifest)
                if saved(work,manifest,blobs,history)[0]!=plan or reports(work,plans,history,manifest,blobs)!=prior:
                    raise IntentlineError('Slice/audit changed before publication',3)
                if directory.read(value+'.json')[0]!=canonical(report):raise IntentlineError('Audit bytes changed',3)
                directory.write('index.json',canonical({'record':'intentline.slice-audit-index','schema_version':1,
                                                       'reports':[sha(canonical(r)) for r in prior]+[value]}),replace=True)
    return {'audit_sha256':sha(canonical(report)),'authentication':'unverified',
            'reported_independence':report['reported_independence'], 'summary':'Optional slice audit retained; no approval or authenticated independence'}
