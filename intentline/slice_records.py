"""Advisory recommendations, immutable bytes and pointer-last publication."""
import html
import os

from .contracts import current
from .errors import IntentlineError
from .paths import Directory, read_file
from .records import canonical, fields, immutable, parse, sha
from .sources import bundle, freshness
from . import slicing


def checked(plan, contract, manifest, blobs, parent):
    try:
        return slicing.check(plan, contract, manifest, blobs, parent)
    except (ValueError, KeyError, TypeError, RecursionError) as exc:
        raise IntentlineError('Slicing refused: ' + str(exc)) from exc


def subject(work):
    manifest, blobs, digest = bundle(work)
    contract, pointer, history = current(work, manifest, blobs, digest)
    continuity = sha(work.read('continuity.json')[0]) if manifest['schema_version'] == 2 else None
    return manifest, blobs, contract, pointer, history, slicing.parent_identity(contract, manifest, continuity)


def proposal(path):
    raw = read_file(path)[0]
    plan = parse(raw)
    if canonical(plan) != raw:
        raise IntentlineError('Slicing proposal must be canonical JSON')
    return plan


def saved(work, manifest, blobs, history):
    try:
        os.stat('slicing', dir_fd=work.fd, follow_symlinks=False)
    except FileNotFoundError:
        return None, []
    with Directory(work.path / 'slicing') as directory:
        try: raw = directory.read('current.json')[0]
        except FileNotFoundError: return None, []  # Orphans do not become published records.
        pointer = parse(raw)
        fields(pointer, ['record','schema_version','plan_sha256','history'])
        if pointer['record'] != 'intentline.slice-pointer' or type(pointer['schema_version']) is not int or pointer['schema_version'] != 1 or canonical(pointer) != raw:
            raise IntentlineError('Corrupt slicing pointer',3)
        digests = pointer['history']
        if not isinstance(digests,list) or not 1 <= len(digests) <= 256 or not all(isinstance(d,str) for d in digests) or len(set(digests)) != len(digests) or digests[-1] != pointer['plan_sha256']:
            raise IntentlineError('Corrupt slicing history',3)
        plans = []
        for digest in digests:
            from .records import digest as validate_digest
            validate_digest(digest)
            data = directory.read(digest + '.json')[0]
            plan = parse(data)
            if canonical(plan) != data or sha(data) != digest:
                raise IntentlineError('Corrupt immutable slicing record',3)
            try:
                slicing.validate(plan, slicing.SLICING)
                revision = plan['parent']['revision']
                if not 1 <= revision <= len(history): raise ValueError('Missing parent revision')
                contract = history[revision-1]
                continuity = sha(work.read('continuity.json')[0]) if manifest['schema_version'] == 2 else None
                checked(plan, contract, manifest, blobs, slicing.parent_identity(contract,manifest,continuity))
                prior = next((p for p in reversed(plans) if p['parent'] == plan['parent']), None)
                expected = sha(canonical(prior)) if prior else None
                if plan['supersedes_sha256'] != expected: raise ValueError('Invalid explicit supersession')
                if prior and plan['rationale'] == prior['rationale']: raise ValueError('Changed recommendation requires a new rationale/evidence')
            except (ValueError, KeyError, TypeError, IntentlineError) as exc:
                raise IntentlineError('Corrupt slicing history: '+str(exc),3) from exc
            plans.append(plan)
        if directory.read('current.json')[0] != raw:
            raise IntentlineError('Slicing pointer changed during inspection',3)
        return plans[-1], plans


def result(plan, count, stale=(), blocked=False):
    state = 'STALE_PARENT' if stale else 'BLOCKED' if blocked else 'NO_PLAN' if plan is None else 'NO_SPLIT' if plan['decision'] == 'no_split' else 'SPLIT_PROPOSED'
    return {'status':state, 'history_count':count, 'plan_sha256':sha(canonical(plan)) if plan else None,
            'parent':plan['parent'] if plan else None, 'stale_sources':list(stale),
            'validation':'structurally_validated', 'semantics':'unverified',
            'authorization':'not_established', 'exit_code':2 if state in ('STALE_PARENT','BLOCKED') else 0,
            'summary':state + ': advisory recommendation; semantics unverified'}


def preview(work_path, proposal_path):
    plan = proposal(proposal_path)
    with Directory(work_path) as work:
        manifest, blobs, contract, pointer, history, parent = subject(work)
        checked(plan,contract,manifest,blobs,parent)
        old, plans = saved(work,manifest,blobs,history)
        replacement(plan,old,plans)
        unchanged(work,pointer,manifest)
        return {**result(plan,len(plans),blocked=bool(contract['open_decisions'])), 'plan':plan, 'recorded':False}


def replacement(plan, old, plans):
    if old == plan: return
    prior = next((p for p in reversed(plans) if p['parent'] == plan['parent']), None)
    if plan['supersedes_sha256'] != (sha(canonical(prior)) if prior else None):
        raise IntentlineError('Replacement requires explicit exact same-parent supersedes_sha256')
    if prior and plan['rationale'] == prior['rationale']:
        raise IntentlineError('Changed recommendation requires new rationale/evidence')
    if len(plans) >= 256: raise IntentlineError('Slicing history limit; no truncation')


def unchanged(work, pointer, manifest):
    if freshness(manifest): raise IntentlineError('STALE_PARENT: source changed')
    if work.read('current.json')[0] != canonical(pointer):
        raise IntentlineError('Parent pointer changed during slicing',3)
    _, _, _, now, _, _ = subject(work)
    if now != pointer or freshness(manifest):
        raise IntentlineError('Parent/source changed during slicing',3)


def record(work_path, proposal_path, expected):
    from .records import digest
    digest(expected)
    plan = proposal(proposal_path)
    with Directory(work_path) as work, work.lock():
        manifest, blobs, contract, pointer, history, parent = subject(work)
        if expected != pointer['contract_sha256']: raise IntentlineError('Expected parent digest mismatch')
        checked(plan,contract,manifest,blobs,parent)
        if contract['open_decisions']: raise IntentlineError('BLOCKED: unresolved parent decisions')
        unchanged(work,pointer,manifest)
        old, plans = saved(work,manifest,blobs,history)
        replacement(plan,old,plans)
        if old == plan: return result(plan,len(plans))
        with Directory(work.path / 'slicing',create=True) as directory:
            digest = immutable(directory,sha(canonical(plan))+'.json',plan)
            unchanged(work,pointer,manifest)
            if saved(work,manifest,blobs,history)[0] != old:
                raise IntentlineError('Concurrent slicing pointer change',3)
            if directory.read(digest+'.json')[0] != canonical(plan):
                raise IntentlineError('Slicing bytes changed before publication',3)
            pointer = {'record':'intentline.slice-pointer','schema_version':1,'plan_sha256':digest,
                       'history':[sha(canonical(p)) for p in plans]+[digest]}
            directory.write('current.json',canonical(pointer),replace=True)
        return result(plan,len(plans)+1)


def status(work_path, render=False):
    with Directory(work_path) as work:
        manifest, blobs, contract, pointer, history, parent = subject(work)
        plan, plans = saved(work,manifest,blobs,history)
        stale = freshness(manifest)
        if plan and plan['parent'] != parent: stale = list(stale)+['parent_identity']
        if work.read('current.json')[0] != canonical(pointer): raise IntentlineError('Parent changed during status',3)
        data = result(plan,len(plans),stale,bool(contract['open_decisions']))
        data['current_parent'] = parent
        from .slice_audits import reports
        audits = reports(work,plans,history,manifest,blobs)
        active = [r for r in audits if r['plan_sha256'] == data['plan_sha256']]
        disputes = [r for r in active if r['outcome'] != 'NO_MATERIAL_FINDINGS']
        data.update(audit_records=len(audits), current_audits=len(active),
                    audit_disputes=disputes, historical_disputes=[r for r in audits if r not in active and r['outcome'] != 'NO_MATERIAL_FINDINGS'])
        if disputes and data['status'] not in ('STALE_PARENT','BLOCKED'):
            data.update(status='BLOCKED',exit_code=2,summary='BLOCKED: retained adverse slicing findings; no approval')
        if freshness(manifest):
            data.update(status='STALE_PARENT',stale_sources=freshness(manifest),exit_code=2,summary='STALE_PARENT: source changed during inspection')
        if work.read('current.json')[0] != canonical(pointer) or saved(work,manifest,blobs,history)[0] != plan:
            raise IntentlineError('Parent/plan changed during status',3)
        if render:
            data['markdown'] = '# '+data['status']+'\n\nAdvisory allocation; semantics and authorization unverified.\n\n'
            if plan:
                # Indented escaped data cannot create active Markdown/HTML instructions or links.
                data['markdown'] += '    '+html.escape(canonical(plan).decode().strip())+'\n'
        return data
