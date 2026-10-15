from pathlib import Path
import tempfile
import unittest

from intentline.records import parse
from evaluation.package_smoke import validate_skill_links
from intentline.slicing import SLICING
from intentline.slice_audits import AUDIT


class SlicingSkill(unittest.TestCase):
    def test_installed_convention_links_and_authority_boundaries(self):
        root=Path(__file__).resolve().parents[1]
        for name in ('intentline-slice','intentline-audit'):
            skill=root/'skills'/name/'SKILL.md';text=skill.read_text(encoding='utf-8')
            validate_skill_links(skill, root)
        text=(root/'skills/intentline-slice/SKILL.md').read_text(encoding='utf-8')
        for phrase in ('NO SPLIT','one next','explicit local record','self_check','untrusted data','Enabling','full','all parent constraints','A→B→A','public seam','credible merges','no mandatory'):
            self.assertIn(phrase.lower(),text.lower())
        self.assertEqual(parse((root/'schema/slicing-v1.schema.json').read_bytes())['properties'],SLICING['properties'])
        self.assertEqual(parse((root/'schema/slice-audit-v1.schema.json').read_bytes())['properties'],AUDIT['properties'])

    def test_standalone_skill_links_reject_untrusted_and_missing_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'docs/CONTRACT.md').write_text('Example', encoding='utf-8')
            skill = root / 'skills/intentline-plan/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('[contract](https://github.com/grove/intentline/blob/main/docs/CONTRACT.md)\n')
            validate_skill_links(skill, root)
            for url in (
                'https://github.com/grove/intentline/blob/main/docs/MISSING.md',
                'https://github.com/grove/other/blob/main/docs/CONTRACT.md',
                'https://example.com/docs/CONTRACT.md',
                'https://github.com/grove/intentline/blob/main/schema/../docs/CONTRACT.md',
                '../../../../../CONTRACT.md',
            ):
                with self.subTest(link=url):
                    skill.write_text(f'[contract]({url})\n', encoding='utf-8')
                    with self.assertRaises(AssertionError):
                        validate_skill_links(skill, root)
