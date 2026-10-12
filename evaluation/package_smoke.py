"""Explicit build qualification, not imported by CLI or ordinary unit tests."""
import argparse
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
            for name in ('intentline-plan','intentline-audit'):
                skill=data/'skills'/name/'SKILL.md'
                text=skill.read_text(encoding='utf-8')
                for link in re.findall(r'\]\(([^)]+)\)',text):
                    assert (skill.parent/link).is_file(),f'Broken installed skill link: {link}'
            assert (data/'docs/SCORECARD_0.2.md').is_file()
            for command in ('prepare','propose','check','render','status','audit-record','adopt','export'):
                run(python,'-B','-m','intentline',command,'--help',cwd=root,env=env)
            executable=prefix/('Scripts/intentline.exe' if os.name == 'nt' else 'bin/intentline')
            run(executable,'--help',cwd=root,env=env)
            assert run(python,'-B','-c','import intentline; print(intentline.__version__)',cwd=root,env=env).strip() == '0.2.0'
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
                for command in ('check','render','status'):
                    run(python,'-B','-m','intentline',command,'--work',work,'--json',cwd=root,env=env)
            print(kind+': installed CLI, skill links, version, dependency and workflow controls pass')
        with tarfile.open(archives[0]) as archive:
            names=archive.getnames()
            assert any(n.endswith('/evaluation/planning_02.py') for n in names)
            assert any(n.endswith('/evaluation/baseline/identity.json') for n in names)
            assert any(n.endswith('/INTENTLINE_0.2_IMPLEMENTATION_PLAN.md') for n in names)
            for name in names:
                path=PurePosixPath(name)
                assert not path.is_absolute() and '..' not in path.parts
    return 0


if __name__ == '__main__':
    sys.exit(main())
