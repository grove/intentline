"""Exercise the user-facing view without changing frozen compatibility tests."""
import contextlib
import io
import json
from unittest.mock import patch

from intentline.cli import main
from intentline.contracts import inspect, propose
from intentline.render import markdown, readable, safe
from intentline.sources import bundle
from intentline.paths import Directory
from tests.support import WorkCase


class ReadablePlans(WorkCase):
    def invoke(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(map(str, args)))
        return code, out.getvalue(), err.getvalue()

    def test_human_view_and_machine_or_detailed_views_share_the_exact_record(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        before = {p.relative_to(self.work): p.read_bytes()
                  for p in self.work.rglob('*') if p.is_file()}
        status, contract = inspect(self.work)
        with Directory(self.work) as work:
            manifest, _, _ = bundle(work)
        full = markdown(contract, status, manifest)
        code, output, error = self.invoke('render', '--work', self.work)
        self.assertEqual((code, error), (0, ''))
        self.assertTrue(output.startswith('# Reject empty'))
        for row in contract['requirements']:
            for value in (row['statement'], row['oracle'], row['seam'], row['planned_evidence'], *row['boundaries']):
                self.assertIn(safe(value), output)
        self.assertNotIn(status['contract_sha256'], output)
        self.assertNotIn('| ID |', output)
        self.assertIn('not run', output)
        self.assertIn('--details', output)
        self.assertEqual(self.invoke('render', '--work', self.work, '--details')[1], full + '\n')
        for args in (('--json', 'render', '--work', self.work),
                     ('render', '--work', self.work, '--json'),
                     ('render', '--work', self.work, '--details', '--json')):
            code, output, error = self.invoke(*args)
            result = json.loads(output)
            self.assertEqual((code, error), (0, ''))
            self.assertEqual(result['data']['markdown'], full)
            self.assertEqual(result['data']['contract_sha256'], status['contract_sha256'])
        self.assertEqual(before, {p.relative_to(self.work): p.read_bytes()
                                 for p in self.work.rglob('*') if p.is_file()})

    def test_constraints_exclusions_questions_and_observation_gaps_remain_visible(self):
        if not self.setup_work():
            return
        ref = self.draft['requirements'][0]['source_refs']
        self.draft['constraints'] = [{'statement': 'Keep existing validation behavior',
                                     'basis': 'necessary_invariant', 'scope': 'Other usernames',
                                     'source_refs': ref}]
        self.draft['out_of_scope'] = [{'statement': 'No password policy changes', 'source_refs': ref}]
        self.draft['open_decisions'] = [{'id': 'D1', 'statement': 'Which error wording?',
                                        'kind': 'outcome', 'source_refs': ref}]
        self.draft['evidence_gaps'] = [{'requirement_ids': ['R1'], 'reason': 'No UI harness available'}]
        self.draft['requirements'][0]['plan_state'] = 'gap'
        propose(self.work, self.write_draft(self.draft))
        code, output, _ = self.invoke('render', '--work', self.work)
        self.assertEqual(code, 2)
        for value in ('Keep existing validation behavior', 'Other usernames',
                      'No password policy changes', 'Which error wording?',
                      'No UI harness available', 'Needs attention'):
            self.assertIn(value, output)
        self.source.write_text('Changed original request\n')
        code, output, _ = self.invoke('render', '--work', self.work)
        self.assertEqual(code, 2)
        self.assertIn('Sources or approval evidence have changed', output)
        self.assertIn('Which error wording?', output)

    def test_review_and_approval_states_do_not_become_success_claims(self):
        if not self.setup_work():
            return
        for flags, message in ((['BLOCKED'], 'adverse review'),
                               (['STALE'], 'changed or are unavailable'),
                               (['READY_FOR_ADOPTION'], 'advice, not approval'),
                               (['ADOPTED_ASSERTED'], 'authority is unverified')):
            with self.subTest(flags=flags):
                self.assertIn(message, readable(self.draft, {'flags': flags}))

    def test_untrusted_text_cannot_inject_html_or_markdown_sections(self):
        if not self.setup_work():
            return
        payload = '<script>alert(1)</script>\n# Forged status | APPROVED'
        self.draft['intended_outcome'] = payload
        self.draft['requirements'][0]['oracle'] = payload
        self.draft['advisory_notes'] = [payload]
        view = readable(self.draft, {'flags': ['DRAFT']})
        self.assertNotIn('<script>', view)
        self.assertNotIn('\n# Forged', view)
        self.assertIn('&lt;script&gt;', view)
        self.assertIn('&#124;', view)

    def test_no_arguments_explains_how_to_start_without_inspecting_records(self):
        with patch('intentline.cli.execute', side_effect=AssertionError('must not inspect records')):
            code, output, error = self.invoke()
        self.assertEqual((code, error), (0, ''))
        self.assertIn('Use intentline-plan to clarify', output)
        self.assertIn('render --work PATH', output)
        code, output, error = self.invoke('--json')
        self.assertEqual(code, 2)
        self.assertFalse(json.loads(output)['ok'])
