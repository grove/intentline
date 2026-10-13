import os

from intentline.records import sha
from intentline.sources import prepare
from tests.support import WorkCase


class SearchTraversal(WorkCase):
    def test_prepare_through_search_only_ancestor(self):
        if not hasattr(os, 'O_SEARCH') or os.geteuid() == 0:
            self.skipTest('Requires O_SEARCH and a user subject to directory permissions')
        parent = self.root / 'search-only'
        parent.mkdir(mode=0o700)
        inputs = parent / 'input'
        inputs.mkdir(mode=0o700)
        source = inputs / 'request.md'
        source.write_bytes(b'Original source through a search-only ancestor\n')
        parent.chmod(0o311)
        try:
            with self.assertRaises(PermissionError):
                list(parent.iterdir())
            out = parent / 'work'
            result = prepare(str(source), [], str(inputs), str(out))
            self.assertEqual(result['sources'][0]['sha256'],
                             sha(source.read_bytes()))
            self.assertEqual((out / 'source' / 'S1.txt').read_bytes(), source.read_bytes())
        finally:
            parent.chmod(0o700)
