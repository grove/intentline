import copy
import json
from unittest.mock import patch

from intentline.adoption import adopt
from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.export import export
from intentline.records import canonical, sha
from intentline.sources import prepare
from tests.compatibility.proofline_direct_parser import criterion_ids, InputGap
from tests.support import WorkCase
from tests.test_adoption import approval


class Exports(WorkCase):
    def test_direct_exact_bytes_ids_advisory_and_no_external_commands(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        out = self.root / 'handoff'
        with patch('subprocess.Popen', side_effect=AssertionError('No external commands')), patch('socket.socket', side_effect=AssertionError('No egress')):
            first = export(self.work, 'proofline-direct', out)
            self.assertEqual(first, export(self.work, 'proofline-direct', out))
        self.assertEqual((out / 'source.md').read_bytes(), self.source.read_bytes())
        brief = (out / 'brief.md').read_text()
        self.assertEqual(criterion_ids(brief), ['R1'])
        self.assertIn('Preview', brief)
        self.assertEqual(first['authority'], 'unapproved')
        self.assertTrue(first['advisory'])
        self.assertEqual(json.loads((out / 'contract.json').read_text()), self.draft)
        manifest = json.loads((out / 'export-manifest.json').read_text())
        for name, digest in manifest['files'].items():
            self.assertEqual(sha((out / name).read_bytes()), digest)
        for bad in ('No criteria', '| R1 | A |\n| R1 | B |'):
            with self.assertRaises(InputGap):
                criterion_ids(bad)

    def test_markdown_json_and_changed_export_rejection(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        for format_name in ('markdown','json'):
            result = export(self.work, format_name, self.root / format_name)
            self.assertEqual(result['format'], format_name)
        new = self.revision(self.draft)
        new['advisory_notes'] = ['Changed proposal']
        propose(self.work, self.write_draft(new))
        with self.assertRaises(IntentlineError):
            export(self.work, 'json', self.root / 'json')
        with self.assertRaises(IntentlineError):
            export(self.work, 'json', self.work / 'nested')

    def test_material_decisions_stale_source_and_approval_block(self):
        if not self.setup_work():
            return
        self.draft['open_decisions'] = [{'id':'D1','statement':'Choose expected error', 'kind':'outcome',
                                        'source_refs':self.draft['requirements'][0]['source_refs']}]
        propose(self.work, self.write_draft(self.draft))
        with self.assertRaisesRegex(IntentlineError, 'BLOCKED'):
            export(self.work, 'proofline-direct', self.root / 'blocked')
        new = self.revision(self.draft)
        new['open_decisions'] = []
        pointer = propose(self.work, self.write_draft(new))
        path = self.root / 'approval.json'
        path.write_bytes(canonical(approval(pointer)))
        adopt(self.work, pointer['contract_sha256'], path)
        path.unlink()
        with self.assertRaisesRegex(IntentlineError, 'STALE'):
            export(self.work, 'proofline-direct', self.root / 'stale-approval')
        self.source.unlink()
        with self.assertRaisesRegex(IntentlineError, 'STALE'):
            export(self.work, 'proofline-direct', self.root / 'stale-source')

    def test_binding_project_reference_gate(self):
        if not self.setup_work():
            return
        policy = self.root / 'policy.md'
        policy.write_text('Keep valid usernames unchanged\n')
        work = self.root / 'with-context'
        capture = prepare(str(self.source), [str(policy)], str(self.root), str(work))
        self.draft['source_bundle_sha256'] = capture['source_bundle_sha256']
        self.draft['constraints'] = [{'statement':'Keep valid usernames unchanged', 'basis':'project_constraint',
                                      'scope':'Valid usernames', 'source_refs':[{'source_id':'S2','line_start':1,'line_end':1,
                                                                              'quote':'Keep valid usernames unchanged'}]}]
        propose(work, self.write_draft(self.draft))
        with self.assertRaisesRegex(IntentlineError, 'explicit --product-root'):
            export(work, 'proofline-direct', self.root / 'missing-root')
        export(work, 'proofline-direct', self.root / 'with-root', self.root)
        downstream = self.root / 'downstream'
        downstream.mkdir()
        with self.assertRaisesRegex(IntentlineError, 'unavailable'):
            export(work, 'proofline-direct', self.root / 'unavailable', downstream)
        (downstream / 'policy.md').write_bytes(policy.read_bytes())
        export(work, 'proofline-direct', self.root / 'matching', downstream)
