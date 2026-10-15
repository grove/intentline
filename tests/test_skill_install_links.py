"""New packaging-link coverage; historical frozen skill tests remain untouched."""
from pathlib import Path
import tempfile
import unittest

from evaluation.package_smoke import validate_skill_links


class SkillInstallLinks(unittest.TestCase):
    def test_all_skills_have_local_counterparts_for_remote_documentation(self):
        root = Path(__file__).resolve().parents[1]
        for name in ('intentline-plan', 'intentline-audit', 'intentline-slice'):
            with self.subTest(skill=name):
                validate_skill_links(root / 'skills' / name / 'SKILL.md', root)

    def test_missing_untrusted_or_escaping_references_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / 'docs'
            docs.mkdir()
            (docs / 'CONTRACT.md').write_text('Test fixture\n', encoding='utf-8')
            skill = root / 'skills/intentline-plan/SKILL.md'
            skill.parent.mkdir(parents=True)

            good = 'https://github.com/grove/intentline/blob/main/docs/CONTRACT.md'
            skill.write_text(f'[contract][contract]\n\n[contract]: {good}\n', encoding='utf-8')
            validate_skill_links(skill, root)

            bad_links = (
                'https://github.com/grove/intentline/blob/main/docs/MISSING.md',
                'https://github.com/another/intentline/blob/main/docs/CONTRACT.md',
                'https://example.com/docs/CONTRACT.md',
                'https://github.com/grove/intentline/blob/main/schema/../docs/CONTRACT.md',
                '../../../outside.md',
            )
            for url in bad_links:
                with self.subTest(url=url):
                    skill.write_text(f'[contract][contract]\n\n[contract]: {url}\n', encoding='utf-8')
                    with self.assertRaises(AssertionError):
                        validate_skill_links(skill, root)

            skill.write_text('[contract][undefined]\n', encoding='utf-8')
            with self.assertRaises(AssertionError):
                validate_skill_links(skill, root)

            skill.write_text(f'[contract][contract]\n\n[contract]: {good}\n[contract]: {good}\n', encoding='utf-8')
            with self.assertRaises(AssertionError):
                validate_skill_links(skill, root)
