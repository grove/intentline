import io
import os
from pathlib import Path
import tempfile
import unittest

from intentline.errors import IntentlineError
from intentline.paths import Directory, MAX_FILE, absolute, capability
from intentline.sources import bundle, capture, freshness, prepare


class Sources(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'request.md'
        self.source.write_bytes(b'Exact request\r\nWith unicode: \xc3\xb8\n')
        self.work = self.root / 'work'

    def test_capability_fails_closed(self):
        if os.name == 'posix':
            capability()
        else:
            with self.assertRaisesRegex(IntentlineError, 'capability unavailable'):
                capability()

    def supported(self):
        if os.name == 'posix':
            return True
        with self.assertRaises(IntentlineError) as error:
            prepare(str(self.source), [], str(self.root), str(self.work))
        self.assertEqual(error.exception.code, 3)
        return False

    def test_exact_round_trip_idempotence_and_private(self):
        if not self.supported():
            return
        first = prepare(str(self.source), [], str(self.root), str(self.work))
        before = {p.name: p.read_bytes() for p in self.work.rglob('*') if p.is_file()}
        self.assertEqual(first, prepare(str(self.source), [], str(self.root), str(self.work)))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.work.rglob('*') if p.is_file()})
        with Directory(self.work) as directory:
            manifest, blobs, digest = bundle(directory)
        self.assertEqual(blobs['S1'], self.source.read_bytes())
        self.assertEqual(digest, first['source_bundle_sha256'])
        self.assertEqual(freshness(manifest), [])
        self.assertEqual(self.work.stat().st_mode & 0o777, 0o700)
        self.assertEqual((self.work / 'source-manifest.json').stat().st_mode & 0o777, 0o600)
        self.source.write_text('changed')
        self.assertEqual(freshness(manifest), ['S1'])
        self.source.unlink()
        self.assertEqual(freshness(manifest), ['S1'])

    def test_stdin_is_explicit_frozen_source(self):
        if not self.supported():
            return
        prepare('-', [], str(self.root), str(self.work), io.BytesIO(b'stdin\r\n'))
        with Directory(self.work) as directory:
            manifest, blobs, _ = bundle(directory)
        self.assertEqual(blobs['S1'], b'stdin\r\n')
        self.assertEqual(freshness(manifest), [])

    def test_invalid_sources_and_duplicate_identity(self):
        if not self.supported():
            return
        for data in (b'x\0y', b'\xff', b'x' * (MAX_FILE + 1)):
            self.source.write_bytes(data)
            with self.assertRaises(IntentlineError):
                capture(str(self.source), [], str(self.root))
        self.source.write_text('request')
        with self.assertRaises(IntentlineError):
            capture(str(self.source), [str(self.source)], str(self.root))
        with self.assertRaises(IntentlineError):
            capture(str(self.source), [str(self.source)] * 64, str(self.root))

    def test_symlink_parent_traversal_and_windows_paths(self):
        for path in ('a/../b', './a', r'C:\work\request.md', 'a\0b'):
            with self.assertRaises(IntentlineError):
                absolute(path)
        if not self.supported():
            return
        alias = self.root / 'alias.md'
        alias.symlink_to(self.source)
        with self.assertRaises(IntentlineError):
            capture(str(alias), [], str(self.root))
        parent_alias = self.root / 'alias-dir'
        parent_alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(IntentlineError):
            capture(str(parent_alias / 'request.md'), [], str(self.root))
        with self.assertRaises(IntentlineError):
            capture(str(self.root), [], str(self.root))

    def test_lock_interruption_and_snapshot_tamper(self):
        if not self.supported():
            return
        prepare(str(self.source), [], str(self.root), str(self.work))
        with Directory(self.work) as directory, directory.lock():
            with self.assertRaisesRegex(IntentlineError, 'Conflicting writer'):
                prepare(str(self.source), [], str(self.root), str(self.work))
        (self.work / 'source' / 'S1.txt').write_text('tamper')
        with Directory(self.work) as directory:
            with self.assertRaisesRegex(IntentlineError, 'hash mismatch'):
                bundle(directory)

    def test_recovery_before_manifest_publication(self):
        if not self.supported():
            return
        self.work.mkdir(mode=0o700)
        (self.work / 'source').mkdir(mode=0o700)
        (self.work / 'source' / 'S1.txt').write_bytes(self.source.read_bytes())
        prepare(str(self.source), [], str(self.root), str(self.work))
        self.assertTrue((self.work / 'source-manifest.json').exists())
