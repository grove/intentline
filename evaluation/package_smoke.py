"""Explicit build qualification, not imported by CLI or ordinary unit tests."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
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


def ai_receipt(python, data, root, env):
    """Operator copies public empty data; the installed evaluator only reads it."""
    source = data/'evaluation/cases/ai_06/not-run-packet'
    private = root/'ai-receipt'
    private.mkdir(mode=0o700)
    shutil.copytree(source, private, dirs_exist_ok=True)
    private.chmod(0o700)  # copytree preserves public source directory permissions.
    pin = (private/'registration.sha256').read_text().strip()
    command = [str(python), '-I', '-B', '-m', 'evaluation.ai_development_06', 'report',
               str(private/'study.json'), '--private-root', str(private), '--registration-sha256', pin]
    before = {str(p.relative_to(private)): p.read_bytes() for p in private.rglob('*') if p.is_file()}
    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
    if os.name != 'posix':
        assert result.returncode == 3 and not result.stdout, 'Windows evaluator must refuse storage'
    else:
        assert result.returncode == 0, result.stderr
        expected = json.loads((data/'evaluation/results/ai-development-06-not-run.json').read_bytes())
        assert json.loads(result.stdout) == expected, 'Installed report differs from frozen empty receipt'
        assert expected['actual_attempts'] == expected['registered_assignments'] == 0
        assert all(v is None for v in expected['all_in_usage'].values())
    assert before == {str(p.relative_to(private)): p.read_bytes() for p in private.rglob('*') if p.is_file()}, 'Read-only evaluator wrote records'


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
            for name in ('intentline-plan','intentline-audit','intentline-slice','intentline-issue'):
                skill=data/'skills'/name/'SKILL.md'
                text=skill.read_text(encoding='utf-8')
                for link in re.findall(r'\]\(([^)]+)\)',text):
                    assert (skill.parent/link).is_file(),f'Broken installed skill link: {link}'
            # The new issue skill uses reference-style links. Resolve them
            # strictly to files in the installed distribution without network.
            issue_text=(data/'skills/intentline-issue/SKILL.md').read_text(encoding='utf-8')
            refs=re.findall(r'\[[^\]\n]+\]\[([a-z0-9-]+)\]',issue_text)
            definitions=re.findall(r'^\[([a-z0-9-]+)\]:[ \t]+(\S+)[ \t]*
            assert (data/'docs/SCORECARD_0.3.md').is_file()
            assert (data/'docs/SCORECARD_0.4.md').is_file()
            assert (data/'docs/SCORECARD_0.5.md').is_file()
            assert (data/'docs/IMPLEMENTATION_0.5.md').is_file()
            for name in ('SCORECARD_0.6.md', 'IMPLEMENTATION_0.6.md'):
                assert (data/'docs'/name).is_file()
            for name in ('AI_DEVELOPMENT_06.md', 'CODEX_PREPARATION_06.md', 'AGENT_ACCESS_06.md',
                         'CODEX_JUDGING_06.md', 'JUDGE_CONTROLS_06.md', 'RUNBOOK_06.md'):
                path = data/'evaluation'/name
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    if not link.startswith('https://'):
                        assert (path.parent/link).is_file(), 'Broken installed evaluation link: '+link
            run(python, '-I', '-B', '-m', 'evaluation.ai_development_06', '--help', cwd=root, env=env)
            located = Path(run(python, '-I', '-B', '-c',
                               'import evaluation.ai_development_06 as a; print(a.__file__)', cwd=root, env=env).strip())
            assert prefix in located.parents, 'Evaluator imported from source instead of fresh install'
            ai_receipt(python, data, prefix, env)
            for operation in ('preview','record','status','render','impact','audit-record','export','inspect'):
                run(python,'-B','-m','intentline','slice',operation,'--help',cwd=root,env=env)
            for schema in ('acceptance-v1','source-bundle-v2','continuity-v1','native-handoff-v1','slicing-v1','slice-audit-v1','slice-handoff-v1'):
                assert (data/('schema/'+schema+'.schema.json')).is_file()
            for command in ('prepare','propose','check','render','status','review','approval-request','amend-source','reconcile','inspect-native','audit-record','adopt','export'):
                run(python,'-B','-m','intentline',command,'--help',cwd=root,env=env)
            executable=prefix/('Scripts/intentline.exe' if os.name == 'nt' else 'bin/intentline')
            run(executable,'--help',cwd=root,env=env)
            assert run(python,'-B','-c','import intentline; print(intentline.__version__)',cwd=root,env=env).strip() == '0.5.0rc1'
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
                assert (work/'source/S1.txt').read_bytes() == source.read_bytes(), 'Original bytes changed'
                reused=json.loads(run(python,'-B','-m','intentline','propose','--work',work,'--draft',path,'--json',cwd=root,env=env))['data']
                assert reused['contract_sha256'] == pointer['contract_sha256'] and reused['revision'] == 1
                assert len(list((work/'revisions').iterdir())) == 1, 'Unchanged rerun appended a revision'
                before={str(p.relative_to(work)):p.read_bytes() for p in work.rglob('*') if p.is_file()}
                for command in ('check','render','status','review','approval-request'):
                    run(python,'-B','-m','intentline',command,'--work',work,'--json',cwd=root,env=env)
                assert before == {str(p.relative_to(work)):p.read_bytes() for p in work.rglob('*') if p.is_file()}, 'Read-only command wrote files'
                # Authored installed-fixture controls, not human or real-agent observations.
                for scenario in ('docs','gap','decision'):
                    case=root/(kind+'-'+scenario);case.mkdir(mode=0o700)
                    original=case/'request.md';original.write_bytes(source.read_bytes())
                    context=case/'policy.md';context.write_bytes(b'Keep valid usernames unchanged\n')
                    if scenario=='decision':original.write_bytes(original.read_bytes()+b'Error text is undecided\n')
                    scenario_work=case/'work'
                    args=[python,'-B','-m','intentline','prepare','--source',original,'--root',case,'--out',scenario_work,'--json']
                    if scenario=='docs':args+=['--context',context]
                    identity=json.loads(run(*args,cwd=root,env=env))['data']
                    proposed=copy.deepcopy(draft);proposed['source_bundle_sha256']=identity['source_bundle_sha256']
                    if scenario=='docs':proposed['constraints']=[{'statement':'Keep valid usernames unchanged','basis':'project_constraint','scope':'All validation','source_refs':[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Keep valid usernames unchanged'}]}]
                    if scenario=='gap':
                        proposed['requirements'][0].update(plan_state='gap',planned_evidence='Await an available public validation observation seam')
                        proposed['evidence_gaps']=[{'requirement_ids':['R1'],'reason':'Authored missing-harness control'}]
                    if scenario=='decision':
                        line=len(original.read_text(encoding='utf-8').splitlines())
                        proposed['open_decisions']=[{'id':'D1','statement':'Which error text should be shown?','kind':'outcome','source_refs':[{'source_id':'S1','line_start':line,'line_end':line,'quote':'Error text is undecided'}]}]
                    candidate=case/'draft.json';candidate.write_text(json.dumps(proposed),encoding='utf-8')
                    run(python,'-B','-m','intentline','propose','--work',scenario_work,'--draft',candidate,'--json',cwd=root,env=env)
                    checked=subprocess.run([str(python),'-B','-m','intentline','check','--work',str(scenario_work),'--json'],cwd=root,env=env,capture_output=True,text=True)
                    assert checked.returncode == (2 if scenario=='decision' else 0),checked.stderr
                    observed=json.loads(checked.stdout)['data']
                    assert observed['status'] == ('BLOCKED' if scenario=='decision' else 'STRUCTURALLY_VALID')
                    assert observed['current_adoptions'] == observed['audit_records'] == 0
                    assert (scenario_work/'source/S1.txt').read_bytes() == original.read_bytes()
                    original.write_bytes(original.read_bytes()+b'Changed original\n')
                    stale=subprocess.run([str(python),'-B','-m','intentline','check','--work',str(scenario_work),'--json'],cwd=root,env=env,capture_output=True,text=True)
                    assert stale.returncode == 2 and json.loads(stale.stdout)['data']['stale_sources'] == ['S1']
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
                refused=subprocess.run([str(python),'-B','-m','intentline','inspect-native','--bundle',str(child),'--json'],cwd=root,env=env,capture_output=True,text=True)
                assert refused.returncode != 0, 'Advisory child entered standalone native inspection'

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
            for required in ('INTENTLINE_0.6_IMPLEMENTATION_PLAN.md','INTENTLINE_0.5_IMPLEMENTATION_PLAN.md','evaluation/intake_05.py','evaluation/INTAKE_05.md','evaluation/USABILITY_05.md','evaluation/SLICING_05.md','evaluation/baseline_05/identity.json','evaluation/results/planning-05-not-run.json','evaluation/results/slicing-05-not-run.json', 'evaluation/ai_development_06.py', 'evaluation/AI_DEVELOPMENT_06.md', 'evaluation/JUDGE_CONTROLS_06.md', 'evaluation/cases/ai_06/authored-controls.json', 'evaluation/baseline_06/identity.json', 'evaluation/results/ai-development-06-not-run.json'):
                assert any(n.endswith('/'+required) for n in names),required
            for name in names:
                path=PurePosixPath(name)
                assert not path.is_absolute() and '..' not in path.parts
                assert not any(part in ('private-studies','restricted','restricted-gold','restricted-reviews','restricted-outcomes','.intentline') for part in path.parts), 'Private materials in sdist'
        with zipfile.ZipFile(wheels[0]) as wheel:
            for name in wheel.namelist():
                assert not any(part in ('private-studies','restricted','.intentline','original-05','historical') for part in PurePosixPath(name).parts), 'Private materials in wheel'
            assert 'evaluation/ai_development_06.py' in wheel.namelist()
    return 0


if __name__ == '__main__':
    sys.exit(main())
,issue_text,re.M)
            assert refs and len(definitions)==len(set(k for k,_ in definitions))
            assert set(refs)==set(k for k,_ in definitions), 'Broken issue-skill references'
            prefix_url='https://github.com/grove/intentline/blob/main/'
            for _,url in definitions:
                assert url.startswith(prefix_url), 'Untrusted issue-skill URL: '+url
                parts=PurePosixPath(url[len(prefix_url):]).parts
                assert len(parts)==2 and parts[0] in ('docs','schema')
                assert all(re.fullmatch(r'[A-Za-z0-9_.-]+', part) for part in parts)
                assert (data.joinpath(*parts)).is_file(), 'Missing installed issue-skill reference: '+url
            assert (data/'docs/SCORECARD_0.2.md').is_file()
            assert (data/'docs/SCORECARD_0.3.md').is_file()
            assert (data/'docs/SCORECARD_0.4.md').is_file()
            assert (data/'docs/SCORECARD_0.5.md').is_file()
            assert (data/'docs/IMPLEMENTATION_0.5.md').is_file()
            for name in ('SCORECARD_0.6.md', 'IMPLEMENTATION_0.6.md'):
                assert (data/'docs'/name).is_file()
            for name in ('AI_DEVELOPMENT_06.md', 'CODEX_PREPARATION_06.md', 'AGENT_ACCESS_06.md',
                         'CODEX_JUDGING_06.md', 'JUDGE_CONTROLS_06.md', 'RUNBOOK_06.md'):
                path = data/'evaluation'/name
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    if not link.startswith('https://'):
                        assert (path.parent/link).is_file(), 'Broken installed evaluation link: '+link
            run(python, '-I', '-B', '-m', 'evaluation.ai_development_06', '--help', cwd=root, env=env)
            located = Path(run(python, '-I', '-B', '-c',
                               'import evaluation.ai_development_06 as a; print(a.__file__)', cwd=root, env=env).strip())
            assert prefix in located.parents, 'Evaluator imported from source instead of fresh install'
            ai_receipt(python, data, prefix, env)
            for operation in ('preview','record','status','render','impact','audit-record','export','inspect'):
                run(python,'-B','-m','intentline','slice',operation,'--help',cwd=root,env=env)
            for schema in ('acceptance-v1','source-bundle-v2','continuity-v1','native-handoff-v1','slicing-v1','slice-audit-v1','slice-handoff-v1'):
                assert (data/('schema/'+schema+'.schema.json')).is_file()
            for command in ('prepare','propose','check','render','status','review','approval-request','amend-source','reconcile','inspect-native','audit-record','adopt','export'):
                run(python,'-B','-m','intentline',command,'--help',cwd=root,env=env)
            executable=prefix/('Scripts/intentline.exe' if os.name == 'nt' else 'bin/intentline')
            run(executable,'--help',cwd=root,env=env)
            assert run(python,'-B','-c','import intentline; print(intentline.__version__)',cwd=root,env=env).strip() == '0.5.0rc1'
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
                assert (work/'source/S1.txt').read_bytes() == source.read_bytes(), 'Original bytes changed'
                reused=json.loads(run(python,'-B','-m','intentline','propose','--work',work,'--draft',path,'--json',cwd=root,env=env))['data']
                assert reused['contract_sha256'] == pointer['contract_sha256'] and reused['revision'] == 1
                assert len(list((work/'revisions').iterdir())) == 1, 'Unchanged rerun appended a revision'
                before={str(p.relative_to(work)):p.read_bytes() for p in work.rglob('*') if p.is_file()}
                for command in ('check','render','status','review','approval-request'):
                    run(python,'-B','-m','intentline',command,'--work',work,'--json',cwd=root,env=env)
                assert before == {str(p.relative_to(work)):p.read_bytes() for p in work.rglob('*') if p.is_file()}, 'Read-only command wrote files'
                # Authored installed-fixture controls, not human or real-agent observations.
                for scenario in ('docs','gap','decision'):
                    case=root/(kind+'-'+scenario);case.mkdir(mode=0o700)
                    original=case/'request.md';original.write_bytes(source.read_bytes())
                    context=case/'policy.md';context.write_bytes(b'Keep valid usernames unchanged\n')
                    if scenario=='decision':original.write_bytes(original.read_bytes()+b'Error text is undecided\n')
                    scenario_work=case/'work'
                    args=[python,'-B','-m','intentline','prepare','--source',original,'--root',case,'--out',scenario_work,'--json']
                    if scenario=='docs':args+=['--context',context]
                    identity=json.loads(run(*args,cwd=root,env=env))['data']
                    proposed=copy.deepcopy(draft);proposed['source_bundle_sha256']=identity['source_bundle_sha256']
                    if scenario=='docs':proposed['constraints']=[{'statement':'Keep valid usernames unchanged','basis':'project_constraint','scope':'All validation','source_refs':[{'source_id':'S2','line_start':1,'line_end':1,'quote':'Keep valid usernames unchanged'}]}]
                    if scenario=='gap':
                        proposed['requirements'][0].update(plan_state='gap',planned_evidence='Await an available public validation observation seam')
                        proposed['evidence_gaps']=[{'requirement_ids':['R1'],'reason':'Authored missing-harness control'}]
                    if scenario=='decision':
                        line=len(original.read_text(encoding='utf-8').splitlines())
                        proposed['open_decisions']=[{'id':'D1','statement':'Which error text should be shown?','kind':'outcome','source_refs':[{'source_id':'S1','line_start':line,'line_end':line,'quote':'Error text is undecided'}]}]
                    candidate=case/'draft.json';candidate.write_text(json.dumps(proposed),encoding='utf-8')
                    run(python,'-B','-m','intentline','propose','--work',scenario_work,'--draft',candidate,'--json',cwd=root,env=env)
                    checked=subprocess.run([str(python),'-B','-m','intentline','check','--work',str(scenario_work),'--json'],cwd=root,env=env,capture_output=True,text=True)
                    assert checked.returncode == (2 if scenario=='decision' else 0),checked.stderr
                    observed=json.loads(checked.stdout)['data']
                    assert observed['status'] == ('BLOCKED' if scenario=='decision' else 'STRUCTURALLY_VALID')
                    assert observed['current_adoptions'] == observed['audit_records'] == 0
                    assert (scenario_work/'source/S1.txt').read_bytes() == original.read_bytes()
                    original.write_bytes(original.read_bytes()+b'Changed original\n')
                    stale=subprocess.run([str(python),'-B','-m','intentline','check','--work',str(scenario_work),'--json'],cwd=root,env=env,capture_output=True,text=True)
                    assert stale.returncode == 2 and json.loads(stale.stdout)['data']['stale_sources'] == ['S1']
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
                refused=subprocess.run([str(python),'-B','-m','intentline','inspect-native','--bundle',str(child),'--json'],cwd=root,env=env,capture_output=True,text=True)
                assert refused.returncode != 0, 'Advisory child entered standalone native inspection'

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
            for required in ('INTENTLINE_0.6_IMPLEMENTATION_PLAN.md','INTENTLINE_0.5_IMPLEMENTATION_PLAN.md','evaluation/intake_05.py','evaluation/INTAKE_05.md','evaluation/USABILITY_05.md','evaluation/SLICING_05.md','evaluation/baseline_05/identity.json','evaluation/results/planning-05-not-run.json','evaluation/results/slicing-05-not-run.json', 'evaluation/ai_development_06.py', 'evaluation/AI_DEVELOPMENT_06.md', 'evaluation/JUDGE_CONTROLS_06.md', 'evaluation/cases/ai_06/authored-controls.json', 'evaluation/baseline_06/identity.json', 'evaluation/results/ai-development-06-not-run.json'):
                assert any(n.endswith('/'+required) for n in names),required
            for name in names:
                path=PurePosixPath(name)
                assert not path.is_absolute() and '..' not in path.parts
                assert not any(part in ('private-studies','restricted','restricted-gold','restricted-reviews','restricted-outcomes','.intentline') for part in path.parts), 'Private materials in sdist'
        with zipfile.ZipFile(wheels[0]) as wheel:
            for name in wheel.namelist():
                assert not any(part in ('private-studies','restricted','.intentline','original-05','historical') for part in PurePosixPath(name).parts), 'Private materials in wheel'
            assert 'evaluation/ai_development_06.py' in wheel.namelist()
    return 0


if __name__ == '__main__':
    sys.exit(main())
