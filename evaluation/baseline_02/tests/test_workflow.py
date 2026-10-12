import contextlib
import io
import json
import os
from pathlib import Path
import random

from intentline.cli import main
from intentline.records import canonical, parse
from tests.support import WorkCase
from tests.test_adoption import approval
from tests.test_audits import report


class Workflow(WorkCase):
    def cli(self, *args, expected=0):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            code = main([*map(str,args),'--json'])
        self.assertEqual(code, expected, stdout.getvalue())
        result = json.loads(stdout.getvalue())
        self.assertEqual(result['schema_version'], 1)
        return result

    def test_full_manual_flow_and_invalid_exit(self):
        if not self.setup_work():
            return
        prepared = self.cli('prepare','--source',self.source,'--root',self.root,'--out',self.work)
        proposal = self.cli('propose','--work',self.work,'--draft',self.draft_path)['data']
        for command in ('check','render','status'):
            self.assertTrue(self.cli(command,'--work',self.work)['ok'])
        audit_path = self.root / 'audit.json'
        audit_path.write_bytes(canonical(report(proposal)))
        self.cli('audit-record','--work',self.work,'--report',audit_path)
        path = self.root / 'approval.json'
        path.write_bytes(canonical(approval(proposal)))
        self.cli('adopt','--work',self.work,'--expected-contract-sha256',proposal['contract_sha256'],'--approval-file',path)
        status = self.cli('status','--work',self.work)['data']
        self.assertEqual(status['status'], 'ADOPTED_ASSERTED')
        self.cli('export','--work',self.work,'--format','proofline-direct','--out',self.root/'handoff')
        self.source.write_text('changed')
        result = self.cli('check','--work',self.work,expected=2)
        self.assertFalse(result['ok'])
        self.cli('export','--work',self.work,'--format','json','--out',self.root/'stale',expected=2)

    def test_seeded_canonical_roundtrips_and_key_order(self):
        rng = random.Random(20261012)
        for i in range(100):
            items = [(f'k{n}', {'text':'ø | ** <tag>\n'+str(rng.randrange(100000)), 'rows':[True,None,n]}) for n in range(5)]
            rng.shuffle(items)
            value = dict(items)
            self.assertEqual(parse(canonical(value)), value)
            self.assertEqual(canonical(value), canonical(dict(reversed(items))))
