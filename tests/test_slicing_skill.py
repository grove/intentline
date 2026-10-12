from pathlib import Path
import re
import unittest

from intentline.records import parse
from intentline.slicing import SLICING
from intentline.slice_audits import AUDIT


class SlicingSkill(unittest.TestCase):
    def test_installed_convention_links_and_authority_boundaries(self):
        root=Path(__file__).resolve().parents[1]
        for name in ('intentline-slice','intentline-audit'):
            skill=root/'skills'/name/'SKILL.md';text=skill.read_text()
            for link in re.findall(r'\]\(([^)]+)\)',text):self.assertTrue((skill.parent/link).is_file(),link)
        text=(root/'skills/intentline-slice/SKILL.md').read_text()
        for phrase in ('NO SPLIT','one next','explicit local record','self_check','untrusted data','Enabling','full','all parent constraints','A→B→A','public seam','credible merges','no mandatory'):
            self.assertIn(phrase.lower(),text.lower())
        self.assertEqual(parse((root/'schema/slicing-v1.schema.json').read_bytes())['properties'],SLICING['properties'])
        self.assertEqual(parse((root/'schema/slice-audit-v1.schema.json').read_bytes())['properties'],AUDIT['properties'])
