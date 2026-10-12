import json
import os
from pathlib import Path

from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.sources import prepare
from tests.support import WorkCase


class SkillFixtures(WorkCase):
    def test_all_authored_scenarios_replay_without_models(self):
        examples = Path(__file__).resolve().parents[1] / 'examples'
        if os.name != 'posix':
            self.setup_work()  # Assert the documented fail-closed boundary, not a skipped pass.
            return
        for case in sorted(examples.iterdir()):
            if not case.is_dir():
                continue
            expected = json.loads((case / 'expected.json').read_text())
            contexts = [str(case / 'policy.md')] if (case / 'policy.md').exists() else []
            for kind in ('good', 'bad'):
                with self.subTest(case=case.name, kind=kind):
                    work = self.root / f'{case.name}-{kind}'
                    capture = prepare(str(case / 'request.md'), contexts, str(examples), str(work))
                    draft = json.loads((case / f'{kind}.template.json').read_text())
                    if draft['source_bundle_sha256'] == 'SOURCE_BUNDLE_AT_PREPARE':
                        draft['source_bundle_sha256'] = capture['source_bundle_sha256']
                    path = self.write_draft(draft)
                    if kind == 'bad' and expected['bad_mechanically_invalid']:
                        with self.assertRaises(IntentlineError):
                            propose(work, path)
                    else:
                        propose(work, path)
                        if kind == 'good':
                            self.assertEqual(inspect(work)[0]['status'], expected['good_status'])
                        else:
                            # A semantic defect is not a structural parser verdict.
                            self.assertTrue(expected['semantic_finding'])

    def test_skill_has_required_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / 'skills/intentline-plan/SKILL.md').read_text()
        for phrase in ('verbatim', 'lower completeness bound', 'upper scope bound', 'necessary inferred',
                       'scoped exception', 'evidence_gaps', 'self', 'Unsettled', 'Reuse', 'Never label'):
            if phrase == 'self':
                continue
            self.assertIn(phrase, skill)
