import contextlib
import io
import json
from pathlib import Path

from intentline.cli import main
from intentline.records import sha
from tests.support import WorkCase


class OneRequest(WorkCase):
    def command(self, *args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(io.StringIO()):
            code=main([*map(str,args),'--json'])
        return code,json.loads(out.getvalue())

    def test_internal_fixture_authoring_validation_repair_and_reuse(self):
        if not self.setup_work():
            return
        # The host authors JSON; this fixture exercises mechanics, not real model quality.
        self.draft['requirements'][0]['source_refs'][0]['quote']='Paraphrased incorrectly'
        self.write_draft(self.draft)
        code,_=self.command('propose','--work',self.work,'--draft',self.draft_path)
        self.assertEqual(code,2)
        self.draft['requirements'][0]['source_refs'][0]['quote']='Reject empty and whitespace-only usernames'
        self.write_draft(self.draft)
        code,first=self.command('propose','--work',self.work,'--draft',self.draft_path)
        self.assertEqual(code,0)
        code,again=self.command('propose','--work',self.work,'--draft',self.draft_path)
        self.assertEqual(code,0)
        self.assertEqual(first['data']['contract_sha256'],again['data']['contract_sha256'])
        self.assertEqual(again['data']['revision'],1)
        for operation in ('check','status','render'):
            code,result=self.command(operation,'--work',self.work)
            self.assertEqual(code,0)
            self.assertIn('DRAFT',result['data']['flags'])
            self.assertEqual(result['data']['audit_records'],0)
            self.assertEqual(result['data']['adoption_records'],0)
        self.assertEqual((self.work/'source/S1.txt').read_bytes(),self.source.read_bytes())

    def test_entry_and_source_fidelity_instructions(self):
        root=Path(__file__).resolve().parents[1]
        skill=(root/'skills/intentline-plan/SKILL.md').read_text()
        for phrase in ('one semantic planning pass','zero mandatory separate audits','non-verbatim capture',
                       'persistence incomplete','Do not change .gitignore','No extra approval step',
                       'No automatic adopt','independently expected oracle'):
            self.assertIn(phrase," ".join(skill.split()))
        import re
        for target in re.findall(r'\]\(([^)]+)\)',skill):
            self.assertTrue((root/'skills/intentline-plan'/target).is_file(),target)
