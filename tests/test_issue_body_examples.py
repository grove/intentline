"""Offline authored examples and instruction delivery, not agent/provider tests."""
import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IssueBodyExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = json.loads((ROOT / 'tests/fixtures/issue_body_examples.json').read_bytes())

    def test_shorter_audit_preserves_findings_and_shared_limits_once(self):
        before, after = (self.examples['audit'][key] for key in ('before', 'after'))
        self.assertLess(len(after), len(before))
        # Only the repeated shared paragraph is removed, not substantive evidence.
        self.assertEqual(set(before.split('\n\n')), set(after.split('\n\n')))
        for phrase in (
            'S1:1', 'S2:10', 'R1 (proposed)', 'require [1,2]', 'caller may already sort',
            'S1:2', 'S2:20', 'R2 (proposed)', '"a,b"', 'no runnable download harness',
            'header naming is UNKNOWN', 'source inspection only', 'fixture-v1',
            'working-tree identity unknown', 'bounded export-path sample',
            'Tests/builds executed: NONE', 'runtime effects unconfirmed',
            'non-verbatim and incomplete', 'private captures are not attached',
            'not establish semantic approval or runtime proof',
        ):
            with self.subTest(phrase=phrase):
                self.assertEqual(after.count(phrase), 1)
        self.assertEqual(after.count('PROPOSED — NOT RUN'), 2)

    def test_refinement_preserves_other_fields_promises_and_historical_bytes(self):
        case = self.examples['refinement']
        before, after = case['before'], case['after']
        self.assertNotEqual(before['body'], after['body'])
        self.assertEqual({k: v for k, v in before.items() if k != 'body'},
                         {k: v for k, v in after.items() if k != 'body'})
        self.assertEqual(case['saved_before'], case['saved_after'])
        for phrase in (
            'R1 (proposed): Downloaded rows retain visible order; hidden rows are excluded.',
            'Rollout note: coordinate the existing documentation translation; no release-date change.',
            'PROPOSED — NOT RUN', 'saved request capture is non-verbatim and incomplete',
            'No runtime tests ran.',
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, before['body'])
                self.assertIn(phrase, after['body'])
        self.assertIn('exactly [1,2], excluding row 3', after['body'])
        for key, label in (('draft', 'Contract'), ('source_capture', 'Source bundle')):
            digest = hashlib.sha256(case['saved_before'][key].encode()).hexdigest()
            for body in (before['body'], after['body']):
                self.assertEqual(body.count(f'{label} SHA-256: {digest}'), 1)
        for phrase in ('Historical draft identity', 'not the revised issue text',
                       'did not create or validate a new saved revision'):
            self.assertIn(phrase, after['body'])

    def test_concise_issue_stays_byte_identical(self):
        case = self.examples['concise']
        self.assertEqual(case['result'], 'UNCHANGED')
        self.assertEqual(case['before'].encode(), case['after'].encode())
        self.assertIn(case['after'], (ROOT / 'docs/ISSUE_BODY_EXAMPLES.md').read_text(encoding='utf-8'))

    def test_guidance_preserves_evidence_identity_and_existing_update_safeguards(self):
        for name in ('intentline-issue/SKILL.md', 'skills/intentline-issue/SKILL.md',
                     'docs/ISSUE_WORKFLOW.md'):
            text = ' '.join((ROOT / name).read_text(encoding='utf-8').split()).casefold()
            for phrase in ('condense repeated', 'once when useful', 'evidence level',
                           'snapshot limits', 'execution status', 'uncertainty',
                           'non-verbatim/incomplete-source', 'PROPOSED — NOT RUN',
                           'historical', 'not the revised issue text',
                           'create or validate a new saved revision',
                           'do not fabricate a revision, validation, hash, or source capture',
                           'word count', 'ISSUE_BODY_EXAMPLES.md'):
                with self.subTest(file=name, phrase=phrase):
                    self.assertIn(phrase.casefold(), text)
        skill = ' '.join((ROOT / 'intentline-issue/SKILL.md').read_text(encoding='utf-8').split())
        for phrase in ('Immediately before writing', 're-read', 'relevant decisions',
                       'not an atomic', 'Skip byte-equivalent or semantically identical',
                       'verify the exact tracker', 'result after the host write'):
            self.assertIn(phrase, skill)
