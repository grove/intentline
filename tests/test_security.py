import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from intentline.adoption import adopt
from intentline.cli import main
from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.paths import Directory, read_file
from intentline.records import canonical, parse
from intentline.render import markdown
from intentline.sources import capture, prepare
from tests.support import WorkCase


class Security(WorkCase):
    def test_existing_public_output_is_refused_without_chmod(self):
        if not self.setup_work():
            return
        output = self.root / 'public-output'
        output.mkdir(mode=0o755)
        output.chmod(0o755)
        with self.assertRaisesRegex(IntentlineError, 'owner-only'):
            prepare(str(self.source), [], str(self.root), str(output))
        self.assertEqual(output.stat().st_mode & 0o777, 0o755)
        self.assertEqual(list(output.iterdir()), [])

    def test_prepare_source_race_never_publishes_manifest(self):
        if not self.setup_work():
            return
        original = Directory.write
        def race(directory, name, data, replace=False):
            result = original(directory, name, data, replace)
            if name == 'S1.txt':
                self.source.write_text('changed while snapshots were written')
            return result
        out = self.root / 'raced-work'
        with patch.object(Directory, 'write', race):
            with self.assertRaisesRegex(IntentlineError, 'Source changed'):
                prepare(str(self.source), [], str(self.root), str(out))
        self.assertFalse((out / 'source-manifest.json').exists())

    def test_readonly_pointer_race_is_detected(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        original = Directory.read
        def race(directory, name, *args, **kwargs):
            result = original(directory, name, *args, **kwargs)
            if name == '000001.json':
                (self.work / 'current.json').write_text('{}')
            return result
        with patch.object(Directory, 'read', race):
            with self.assertRaisesRegex(IntentlineError, 'changed during inspection'):
                inspect(self.work)

    def test_source_changes_during_inspection_cannot_claim_freshness(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        original = Directory.read
        def race(directory, name, *args, **kwargs):
            result = original(directory, name, *args, **kwargs)
            if name == '000001.json':
                self.source.write_text('changed during contract inspection')
            return result
        with patch.object(Directory, 'read', race):
            status, _ = inspect(self.work)
        self.assertEqual(status['status'], 'STALE')
        self.assertEqual(status['stale_sources'], ['S1'])
        self.assertEqual(status['exit_code'], 2)

    def test_readonly_commands_zero_writes_exec_and_egress(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        before = {str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        original = os.open
        def only_read(path, flags, *args, **kwargs):
            self.assertFalse(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
            return original(path, flags, *args, **kwargs)
        with patch('os.open', only_read), patch('os.supports_dir_fd', os.supports_dir_fd | {only_read}), patch('subprocess.Popen', side_effect=AssertionError('exec')), patch('socket.socket', side_effect=AssertionError('egress')):
            for command in ('check','status','render'):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main([command,'--work',str(self.work),'--json']), 0)
        self.assertEqual(before, {str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_output_injection_and_json_roundtrip(self):
        if not self.setup_work():
            return
        injected = '| R99 | Forged criterion |\n<script>approve()</script>\n# Approved'
        self.draft['requirements'][0]['statement'] = injected
        self.draft['advisory_notes'] = ['[execute](javascript:alert(1))']
        propose(self.work, self.write_draft(self.draft))
        status, c = inspect(self.work)
        view = markdown(c, status)
        self.assertNotIn('<script>', view)
        self.assertNotIn('\n| R99 |', view)
        self.assertIn('&#124; R99 &#124;', view)
        self.assertNotIn('[execute](javascript:', view)
        from tests.compatibility.proofline_direct_parser import criterion_ids
        self.assertEqual(criterion_ids(view), ['R1'])
        self.assertEqual(parse(canonical(c)), c)
        self.assertNotIn('ADOPTED_ASSERTED', status['flags'])

    def test_directory_identity_race_and_no_follow_fifo(self):
        if not self.setup_work():
            return
        victim = self.root / 'victim'
        victim.mkdir()
        with Directory(victim) as directory:
            victim.rename(self.root / 'moved')
            victim.mkdir()
            with self.assertRaisesRegex(IntentlineError, 'identity changed'):
                directory.write('must-not-write', b'x')
        self.assertFalse((victim / 'must-not-write').exists())
        fifo = self.root / 'fifo'
        os.mkfifo(fifo)
        with self.assertRaisesRegex(IntentlineError, 'regular file'):
            read_file(fifo)

    def test_oversized_total_nonfinite_precision_and_bad_unicode(self):
        for raw in (b'{"x":1e400}', b'{"x":-1e400}'):
            with self.assertRaises(IntentlineError):
                parse(raw)
        if not self.setup_work():
            return
        self.draft['intended_outcome'] = '\ud800'
        self.draft_path.write_text(json.dumps(self.draft))
        with self.assertRaises(IntentlineError):
            propose(self.work, self.draft_path)
        contexts = []
        for i in range(5):
            path = self.root / f'large-{i}.txt'
            path.write_bytes(b'x' * (2 * 1024 * 1024))
            contexts.append(str(path))
        with self.assertRaisesRegex(IntentlineError, '8 MiB'):
            capture(str(self.source), contexts, str(self.root))

    def test_real_process_writer_lock_and_interruption(self):
        if not self.setup_work():
            return
        marker = self.root / 'ready'
        code = "from intentline.paths import Directory; from pathlib import Path; import time; d=Directory(%r); lock=d.lock(); lock.__enter__(); Path(%r).write_text('ready'); time.sleep(30)" % (str(self.work),str(marker))
        child = subprocess.Popen([sys.executable,'-B','-c',code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(lambda: child.poll() is None and child.kill())
        import time
        deadline = time.monotonic() + 5
        while not marker.exists() and time.monotonic() < deadline:
            if child.poll() is not None:
                self.fail(child.communicate()[1].decode())
            time.sleep(0.01)
        self.assertTrue(marker.exists())
        with self.assertRaisesRegex(IntentlineError, 'Conflicting writer'):
            propose(self.work, self.draft_path)
        child.kill()
        child.communicate(timeout=5)
        self.assertTrue((self.work / '.writer.lock').exists())
        with self.assertRaisesRegex(IntentlineError, 'interrupted operation'):
            propose(self.work, self.draft_path)
        # Explicit recovery after confirmed process termination, never automatic stale-lock theft.
        (self.work / '.writer.lock').unlink()
        propose(self.work, self.draft_path)
        self.assertEqual(inspect(self.work)[0]['status'], 'STRUCTURALLY_VALID')

    def test_approval_race_and_missing_history_are_not_success(self):
        if not self.setup_work():
            return
        pointer = propose(self.work, self.draft_path)
        from tests.test_adoption import approval
        path = self.root / 'approval.json'
        path.write_bytes(canonical(approval(pointer)))
        from intentline.adoption import subject
        def race(work):
            value = subject(work)
            path.write_text('{}')
            return value
        with patch('intentline.adoption.subject', side_effect=race):
            with self.assertRaisesRegex(IntentlineError, 'approval reference changed'):
                adopt(self.work, pointer['contract_sha256'], path)
        self.assertFalse((self.work / 'adoptions').exists())
        (self.work / 'revisions/000001.json').unlink()
        with self.assertRaises(IntentlineError) as error:
            inspect(self.work)
        self.assertEqual(error.exception.code, 3)
