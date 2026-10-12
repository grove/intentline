"""Explicit build qualification, not imported by CLI or ordinary unit tests."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile


def run(*args, cwd, env):
    result = subprocess.run(list(map(str,args)),cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.returncode:
        raise RuntimeError(result.stdout+'\n'+result.stderr)
    return result.stdout


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dist')
    args=parser.parse_args(argv)
    dist=Path(args.dist).resolve()
    wheels=list(dist.glob('intentline-*.whl'));archives=list(dist.glob('intentline-*.tar.gz'))
    assert len(wheels) == len(archives) == 1, 'Use a fresh distribution directory'
    with zipfile.ZipFile(wheels[0]) as wheel:
        metadata=wheel.read(next(n for n in wheel.namelist() if n.endswith('.dist-info/METADATA'))).decode()
        assert 'Requires-Dist:' not in metadata, 'Runtime dependencies were introduced'
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory).resolve(); env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PIP_DISABLE_PIP_VERSION_CHECK':'1'}
        # Installation is explicit dev tooling; no model calls, prompts, credentials or inference.
        for kind,artifact in (('wheel',wheels[0]),('sdist',archives[0])):
            prefix=root/kind;venv.create(prefix,with_pip=True)
            python=prefix/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
            run(python,'-m','pip','install','--no-deps',artifact,cwd=root,env=env)
            data=Path(run(python,'-B','-c','import sysconfig; print(sysconfig.get_path("data"))',cwd=root,env=env).strip())/'share/intentline'
            for name in ('intentline-plan','intentline-audit','intentline-slice'):
                skill=data/'skills'/name/'SKILL.md'
                text=skill.read_text(encoding='utf-8')
                for link in re.findall(r'\]\(([^)]+)\)',text):
                    assert (skill.parent/link).is_file(),f'Broken installed skill link: {link}'
            assert (data/'docs/SCORECARD_0.2.md').is_file()
            assert (data/'docs/SCORECARD_0.3.md').is_file()
            assert (data/'docs/SCORECARD_0.4.md').is_file()
            for operation in ('preview','record','status','render','impact','audit-record','export','inspect'):
                run(python,'-B','-m','intentline','slice',operation,'--help',cwd=root,env=env)
            for schema in ('acceptance-v1','source-bundle-v2','continuity-v1','native-handoff-v1','slicing-v1','slice-audit-v1','slice-handoff-v1'):
                assert (data/('schema/'+schema+'.schema.json')).is_file()
            for command in ('prepare','propose','check','render','status','review','approval-request','amend-source','reconcile','inspect-native','audit-record','adopt','export'):
                run(python,'-B','-m','intentline',command,'--help',cwd=root,env=env)
            executable=prefix/('Scripts/intentline.exe' if os.name == 'nt' else 'bin/intentline')
            run(executable,'--help',cwd=root,env=env)
            assert run(python,'-B','-c','import intentline; print(intentline.__version__)',cwd=root,env=env).strip() == '0.4.0'
            # Installed manual workflow uses the shipped public example, not a live agent.
            source=data/'examples/username-validation/request.md';work=root/(kind+'-work')
            command=[str(python),'-B','-m','intentline','prepare','--source',str(source),'--root',str(data),'--out',str(work),'--json']
            result=subprocess.run(command,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            if os.name != 'posix':
                assert result.returncode == 3 and not work.exists(), 'Windows must fail closed'
            else:
                assert result.returncode == 0,result.stderr
                captured=json.loads(result.stdout)
                draft=json.loads((data/'examples/username-validation/good.template.json').read_text())
                draft['source_bundle_sha256']=captured['data']['source_bundle_sha256']
                path=root/(kind+'-draft.json');path.write_text(json.dumps(draft),encoding='utf-8')
                run(python,'-B','-m','intentline','propose','--work',work,'--draft',path,'--json',cwd=root,env=env)
                for command in ('check','render','status','review','approval-request'):
                    run(python,'-B','-m','intentline',command,'--work',work,'--json',cwd=root,env=env)
                pointer=json.loads(run(python,'-B','-m','intentline','status','--work',work,'--json',cwd=root,env=env))['data']
                amendment=root/(kind+'-amendment.md');amendment.write_text('Reject usernames longer than 32 characters\n',encoding='utf-8')
                successor=root/(kind+'-successor')
                captured=json.loads(run(python,'-B','-m','intentline','amend-source','--work',work,'--amendment',amendment,'--root',root,'--out',successor,'--expected-contract-sha256',pointer['contract_sha256'],'--json',cwd=root,env=env))['data']
                draft['contract_id']+='-successor';draft['source_bundle_sha256']=captured['source_bundle_sha256']
                row=copy.deepcopy(draft['requirements'][0]);row.update(id='R2',statement='Reject usernames longer than 32 characters',boundaries=['33 characters'],oracle='Validation error for 33-character username',planned_evidence='Call public validation interface with 33 characters',source_refs=[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Reject usernames longer than 32 characters'}]);draft['requirements'].append(row)
                def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode('utf-8')
                mapping={'record':'intentline.continuity','schema_version':1,'predecessor_contract_sha256':pointer['contract_sha256'],'predecessor_source_bundle_sha256':pointer['source_bundle_sha256'],'contract_sha256':hashlib.sha256(canonical(draft)).hexdigest(),'source_bundle_sha256':draft['source_bundle_sha256'],'mappings':[{'from':['R1'],'to':['R1'],'disposition':'preserved','reason':'Unchanged obligation; semantic audit remains external','source_refs':draft['requirements'][0]['source_refs']}],'added_requirement_ids':['R2'],'other_changes':[]}
                path.write_bytes(canonical(draft));mapping_path=root/(kind+'-continuity.json');mapping_path.write_bytes(canonical(mapping))
                run(python,'-B','-m','intentline','reconcile','--work',successor,'--draft',path,'--continuity',mapping_path,'--json',cwd=root,env=env)
                for command in ('review','approval-request'):
                    run(python,'-B','-m','intentline',command,'--work',successor,'--json',cwd=root,env=env)
                native=root/(kind+'-native');run(python,'-B','-m','intentline','export','--work',successor,'--format','proofline-native','--out',native,'--json',cwd=root,env=env)
                inspection=json.loads(run(python,'-B','-m','intentline','inspect-native','--bundle',native,'--json',cwd=root,env=env))['data']
                assert inspection['authorization']=='not_established'
                run(python,'-I','-B',native/'inspect_bundle.py',native,cwd=root,env=env)
                # Both installed slicing routes use only public authored sources.
                example=data/'examples/slicing';slice_work=root/(kind+'-slicing')
                captured=json.loads(run(python,'-B','-m','intentline','prepare','--source',example/'request.md','--root',data,'--out',slice_work,'--json',cwd=root,env=env))['data']
                contract=json.loads((example/'good.template.json').read_bytes());contract['source_bundle_sha256']=captured['source_bundle_sha256']
                contract_path=root/(kind+'-slice-parent.json');contract_path.write_bytes(canonical(contract))
                run(python,'-B','-m','intentline','propose','--work',slice_work,'--draft',contract_path,'--json',cwd=root,env=env)
                for route in ('no-split','split'):
                    plan=json.loads((example/(route+'.template.json')).read_bytes())
                    state=json.loads(run(python,'-B','-m','intentline','slice','status','--work',slice_work,'--json',cwd=root,env=env))['data']
                    plan['parent']=state['current_parent']
                    plan['supersedes_sha256']=state['plan_sha256']
                    candidate=root/(kind+'-'+route+'.json');candidate.write_bytes(canonical(plan))
                    run(python,'-B','-m','intentline','slice','preview','--work',slice_work,'--proposal',candidate,'--json',cwd=root,env=env)
                    run(python,'-B','-m','intentline','slice','record','--work',slice_work,'--proposal',candidate,'--expected-parent-sha256',plan['parent']['contract_sha256'],'--json',cwd=root,env=env)
                    run(python,'-B','-m','intentline','slice','render','--work',slice_work,'--json',cwd=root,env=env)
                child=root/(kind+'-child');run(python,'-B','-m','intentline','slice','export','--work',slice_work,'--child','S1','--out',child,'--json',cwd=root,env=env)
                receipt=json.loads(run(python,'-B','-m','intentline','slice','inspect','--bundle',child,'--json',cwd=root,env=env))['data']
                assert receipt['child_acceptance']=='not_established'
                run(python,'-I','-B',child/'inspect_child.py',child,cwd=root,env=env)

            print(kind+': installed CLI, skill links, version, dependency and workflow controls pass')
        with tarfile.open(archives[0]) as archive:
            names=archive.getnames()
            assert any(n.endswith('/evaluation/planning_02.py') for n in names)
            assert any(n.endswith('/evaluation/baseline/identity.json') for n in names)
            assert any(n.endswith('/INTENTLINE_0.2_IMPLEMENTATION_PLAN.md') for n in names)
            assert any(n.endswith('/INTENTLINE_0.3_IMPLEMENTATION_PLAN.md') for n in names)
            assert any(n.endswith('/evaluation/baseline_02/pyproject.toml') for n in names)
            assert any(n.endswith('/tests/compatibility/proofline_native_input.py') for n in names)
            assert any(n.endswith('/evaluation/baseline_04/identity.json') for n in names)
            assert any(n.endswith('/evaluation/baseline_04/.github/workflows/ci.yml') for n in names)
            assert any(n.endswith('/evaluation/slicing_04.py') for n in names)
            assert any(n.endswith('/INTENTLINE_0.4_IMPLEMENTATION_PLAN.md') for n in names)
            for name in names:
                path=PurePosixPath(name)
                assert not path.is_absolute() and '..' not in path.parts
    return 0


if __name__ == '__main__':
    sys.exit(main())
