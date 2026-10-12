import json
from pathlib import Path
import unittest

from intentline.records import sha


class Baseline04(unittest.TestCase):
    def test_frozen_03_files_and_tests(self):
        root=Path(__file__).resolve().parents[1]
        frozen=root/'evaluation/baseline_04'
        identity=json.loads((frozen/'identity.json').read_bytes())
        self.assertEqual(identity['commit'],'0ff076576317745aad66dab60a4f1bb9eb2db4b3')
        for name,digest in identity['files'].items():
            path=root/name if name.startswith('tests/') else frozen/name
            self.assertEqual(sha(path.read_bytes()),digest,name)
        self.assertEqual((root/'schema/acceptance-v1.schema.json').read_bytes(),(frozen/'schema/acceptance-v1.schema.json').read_bytes())
