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

    def test_frozen_original_contract_sources_result_and_native_bundle(self):
        import io
        import os
        from unittest.mock import patch
        from intentline.cli import main
        from intentline.contracts import inspect
        from intentline.native_handoff import inspect_native
        from intentline.records import parse,canonical
        root=Path(__file__).resolve().parents[1]/'evaluation/baseline_04/captures'
        identity=parse((root/'capture-identity.json').read_bytes())
        for name,digest in identity['files'].items():self.assertEqual(sha((root/name).read_bytes()),digest)
        if os.name!='posix':return  # The blanket Windows refusal has separate no-I/O assertions.
        self.assertEqual(inspect(root/'work')[0],parse((root/'status.json').read_bytes()))
        with patch('sys.stdout',new_callable=io.StringIO) as wire:
            self.assertEqual(main(['--json','status','--work',str(root/'work')]),0)
        self.assertEqual(wire.getvalue().encode(),(root/'result.json').read_bytes())
        self.assertEqual(inspect_native(root/'native')['contract_sha256'],parse((root/'work/current.json').read_bytes())['contract_sha256'])
