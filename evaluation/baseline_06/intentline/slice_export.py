"""Explicit data-only child publication; no authority or consumer execution."""
import os
from pathlib import Path

from .errors import IntentlineError
from .paths import Directory, absolute, read_file
from .records import canonical, immutable, sha
from .slice_records import saved, status, subject, unchanged
from .slice_inspect import child_view, inspect_slice, inspect_slice_payload


def inspect(path):
    try:return inspect_slice(path)
    except (ValueError,OSError,KeyError,TypeError,RecursionError) as exc:
        raise IntentlineError('Child inspection refused: '+str(exc),3 if 'unavailable on this host' in str(exc) else 2) from exc


def inspector_bytes():
    # Package one stdlib file so isolated Python needs neither Intentline nor sibling imports.
    root=Path(__file__).parent
    native=read_file(root/'native_inspect.py')[0].decode().split("if __name__ == '__main__':")[0]
    slicing=read_file(root/'slicing.py')[0].decode()
    start=slicing.index('if __package__:');end=slicing.index('\n\ndef obj',start)
    slicing=slicing[:start]+slicing[end:]
    inspector=read_file(root/'slice_inspect.py')[0].decode()
    inspector=inspector.replace('from . import native_inspect as native\n','').replace('from . import slicing\n','')
    inspector=inspector.replace('native.','').replace('slicing.','')
    return (native+'\n'+slicing+'\n'+inspector).encode()


def export(work_path, child_id, out):
    target=absolute(out);work_path=absolute(work_path)
    if target==work_path or work_path in target.parents or target in work_path.parents:
        raise IntentlineError('Child export must be separate from parent work')
    with Directory(work_path) as work,work.lock():
        manifest,blobs,contract,pointer,history,parent=subject(work)
        plan,plans=saved(work,manifest,blobs,history)
        if not plan or plan['parent']!=parent or plan['decision']!='split':raise IntentlineError('No current SPLIT plan for child export')
        if status(work_path)['exit_code']:raise IntentlineError('Blocked/stale child export')
        try:view=child_view(plan,contract,child_id)
        except ValueError as exc:raise IntentlineError(str(exc)) from exc
        files={'contract.json':canonical(contract),'history.json':canonical(history),'source-manifest.json':canonical(manifest),
               'plan.json':canonical(plan),'child.json':canonical(view),'inspect_child.py':inspector_bytes()}
        files.update({'source-'+sid+'.txt':data for sid,data in blobs.items()})
        if manifest['schema_version']==2:
            from .amendments import archives
            _,archive=archives(work,manifest);files.update({'archive-'+name:data for name,data in archive.items()})
            files.update({'initial-contract.json':canonical(history[0]),'continuity.json':work.read('continuity.json')[0],
                          'successor-complete.json':work.read('successor-complete.json')[0]})
        if any(len(data)>2*1024*1024 for data in files.values()) or sum(map(len,files.values()))>48*1024*1024:
            raise IntentlineError('Child bundle exceeds file/total bounds; no truncation')
        envelope={'record':'intentline.slice-handoff','schema_version':1,'parent':parent,'plan_sha256':sha(canonical(plan)),
                  'child_id':child_id,'authorization':'not_established','consumer_execution':'not_observed',
                  'child_acceptance':'not_established','validation':'structurally_validated','semantics':'unverified',
                  'files':{name:sha(data) for name,data in sorted(files.items())}}
        inspect_slice_payload(envelope,files,sha(canonical(envelope)))
        unchanged(work,pointer,manifest)
        with Directory(target,create=True) as destination,destination.lock():
            if set(os.listdir(destination.fd)) - set(files) - {'slice-manifest.json','.writer.lock'}:
                raise IntentlineError('Child output contains unrelated files; choose a new private output')
            for name,data in files.items():
                try:prior=destination.read(name)[0]
                except FileNotFoundError:destination.write(name,data)
                else:
                    if prior!=data:raise IntentlineError('Conflicting immutable child output',3)
            unchanged(work,pointer,manifest)
            if status(work_path)['exit_code'] or saved(work,manifest,blobs,history)[0]!=plan:
                raise IntentlineError('Child parent/plan/audit changed before publication')
            for name,data in files.items():
                if destination.read(name)[0]!=data:raise IntentlineError('Child output changed before marker',3)
            try: destination.read('slice-manifest.json')
            except FileNotFoundError: new_marker=True
            else: new_marker=False
            try:
                immutable(destination,'slice-manifest.json',envelope)
                unchanged(work,pointer,manifest)
                if saved(work,manifest,blobs,history)[0]!=plan or status(work_path)['exit_code']:
                    raise IntentlineError('Child inputs changed during marker publication')
            except BaseException:
                if new_marker:
                    try: os.unlink('slice-manifest.json',dir_fd=destination.fd)
                    except FileNotFoundError: pass
                    os.fsync(destination.fd)
                raise
    receipt=inspect(target)
    return {**receipt,'out':str(target),'summary':'Advisory child data exported; no standalone acceptance, authority or dispatch'}
