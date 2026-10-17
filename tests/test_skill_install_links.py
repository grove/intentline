"""Verify standalone agent entries without changing frozen historical tests."""
from pathlib import Path, PurePosixPath
import re
import unittest


class StandaloneSkillInstall(unittest.TestCase):
    def test_portable_entries_match_frozen_skill_metadata_and_link_to_support_files(self):
        root = Path(__file__).resolve().parents[1]
        prefix = 'https://github.com/grove/intentline/blob/main/'
        for name in ('intentline-plan', 'intentline-audit', 'intentline-slice', 'intentline-issue'):
            with self.subTest(skill=name):
                original = (root / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
                portable = (root / name / 'SKILL.md').read_text(encoding='utf-8')
                self.assertEqual(original.split('---', 2)[1], portable.split('---', 2)[1])
                if name == 'intentline-issue':
                    self.assertEqual(original, portable, 'The portable and packaged new skill must match')
                self.assertIn('npx skills@latest add grove/intentline', portable)
                self.assertEqual(re.findall(r'\]\(([^)]+)\)', portable), [])
                definitions = re.findall(r'^\[([a-z0-9-]+)\]:[ \t]+(\S+)[ \t]*$', portable, re.M)
                refs = re.findall(r'\[[^\]\n]+\]\[([a-z0-9-]+)\]', portable)
                self.assertTrue(refs)
                self.assertEqual(set(refs), {key for key, _ in definitions})
                self.assertEqual(len(definitions), len({key for key, _ in definitions}))
                for _, url in definitions:
                    self.assertTrue(url.startswith(prefix), url)
                    parts = PurePosixPath(url[len(prefix):]).parts
                    self.assertEqual(len(parts), 2, url)
                    self.assertIn(parts[0], ('docs', 'schema'), url)
                    self.assertTrue(all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) for p in parts), url)
                    self.assertTrue(root.joinpath(*parts).is_file(), url)

    def test_portable_plan_test_design_handoff_is_optional_and_source_bound(self):
        """Guard the instruction change, not the quality of a future model response."""
        root = Path(__file__).resolve().parents[1]
        portable = (root / 'intentline-plan/SKILL.md').read_text(encoding='utf-8')
        historical = (root / 'skills/intentline-plan/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Optional test-design handoff, same planning pass', portable)
        self.assertNotIn('Optional test-design handoff, same planning pass', historical)
        for phrase in (
            'source_refs', 'boundaries', 'seam', 'oracle', 'planned_evidence',
            'exact captured source', 'plausible incorrect behavior',
            'independent expected result', 'UNKNOWN', 'open_decisions',
            'evidence_gaps', 'skip extra scenarios', 'NOT RUN',
            'No test quota', 'no new model', 'test execution',
            'not assertions that a test exists or passed',
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), portable.casefold())
        # Authored positive/negative/unknown example; not a model-quality test.
        for phrase in ('four', 'five', '> 5', 'subsequent login after lock: UNKNOWN'):
            with self.subTest(example=phrase):
                self.assertIn(phrase.casefold(), portable.casefold())

    def test_issue_skill_modes_and_write_boundaries_are_documented(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / 'intentline-issue/SKILL.md').read_text(encoding='utf-8').lower()
        for phrase in ('review', 'create', 'update', 'authorization',
                       'relevant comments', 'evidence gap', 'untrusted',
                       'immediately', 'not an atomic', 'unchanged',
                       'not published', 'one request, one useful issue'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_material_boundaries_have_feasible_planned_observations(self):
        """Instruction regression only; this cannot assess agent behavior."""
        root = Path(__file__).resolve().parents[1]
        for name in ('intentline-plan/SKILL.md', 'intentline-issue/SKILL.md',
                     'skills/intentline-issue/SKILL.md'):
            text = ' '.join((root / name).read_text(encoding='utf-8').split()).casefold()
            for phrase in (
                'risk-relevant boundary', 'feasible', 'observation',
                'existing covering scenario', 'equivalent', 'stable r id',
                'fixture constraints', 'transaction/session ordering', 'execution path',
                'pending', 'protected consumer', 'independently expected',
                'unknown', 'gap',
                'routine low-risk work', 'PROPOSED — NOT RUN',
                'intentline-docs-planned-check-examples',
            ):
                with self.subTest(skill=name, phrase=phrase):
                    self.assertIn(phrase.casefold(), text)

    def test_issue_review_is_read_only_including_local_records(self):
        root = Path(__file__).resolve().parents[1]
        portable = (root / 'intentline-issue/SKILL.md').read_text(encoding='utf-8').casefold()
        packaged = (root / 'skills/intentline-issue/SKILL.md').read_text(encoding='utf-8').casefold()
        guide = (root / 'docs/ISSUE_WORKFLOW.md').read_text(encoding='utf-8').casefold()
        self.assertEqual(portable, packaged)
        for phrase in ('including local storage', 'write local files',
                       'separately requests', 'alone does not authorize'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, portable)
        self.assertIn('review never runs record-producing commands', guide)

    def test_issue_skill_is_tracker_agnostic_and_preserves_native_fields(self):
        """Provider choices stay host-driven; no exclusive GitHub dependency."""
        root = Path(__file__).resolve().parents[1]
        skill = (root / 'intentline-issue/SKILL.md').read_text(encoding='utf-8')
        guide = (root / 'docs/ISSUE_WORKFLOW.md').read_text(encoding='utf-8')
        frontmatter = skill.split('---', 2)[1].casefold()
        self.assertIn('host-accessible issue tracker', frontmatter)
        self.assertNotIn('github', frontmatter)
        for phrase in (
            "host agent's existing issue-tracker",
            'tracker\'s native representation',
            'rich text',
            'custom fields',
            'project/workspace',
            'version/etag/compare-and-swap',
            'not an atomic',
            'without the cli',
            'read-only',
            'not published',
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.replace('\\', '').casefold(), skill.casefold())
        for name in ('GitHub', 'Jira', 'Linear'):
            with self.subTest(tracker=name):
                self.assertIn(name, guide)
        self.assertIn('illustrative requests, not verified jira/linear integrations',
                      guide.casefold())
        self.assertIn('not automatically', guide.casefold())
