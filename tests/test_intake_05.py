import copy
import json
import os
from unittest.mock import patch

from evaluation.intake_05 import inspect, main
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical, sha
from tests.support import WorkCase


class Intake05(WorkCase):
    def fixture(self):
        def ref(name, text):
            raw = text.encode()
            (self.root / name).write_bytes(raw)
            return {'path': name, 'sha256': sha(raw)}
        task = {'id': 'authored-candidate', 'status': 'candidate_unreviewed', 'repository': 'example/project',
                'commit': 'a' * 40, 'license': 'MIT', 'license_capture': ref('license.txt', 'Authored license fixture'),
                'request': ref('request.txt', 'Authored request'), 'context': [], 'provenance': ref('provenance.txt', 'Authored provenance'),
                'scope': 'Authored test only', 'author': None, 'checker': None, 'reviews': [], 'reference': None,
                'slicing_parent': None, 'blockers': ['Authored incomplete packet']}
        return {'record': 'intentline.task-intake', 'schema_version': 1, 'captured_at': '2026-10-12T00:00:00Z',
                'tasks': [task], 'registered_assignments': 0, 'executed': 0,
                'model_authorization': None, 'host_isolation': None, 'blinding_ready': None, 'cost_permission': None}

    def test_read_only_partial_packet_and_sanitized_report(self):
        if os.name != 'posix':
            self.setup_work()
            return
        intake = self.fixture()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        with patch.object(Directory, 'write', side_effect=AssertionError('write')), patch('subprocess.Popen', side_effect=AssertionError('dispatch')), patch('socket.socket', side_effect=AssertionError('network')):
            result = inspect(intake, self.root)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})
        self.assertEqual(result['candidate_count'], 1)
        self.assertEqual(result['eligible_count'], 0)
        self.assertEqual(result['missing_authors'], 1)
        self.assertEqual(result['missing_independent_reviews'], 1)
        self.assertEqual(result['cost_permission'], 'missing')
        self.assertNotIn('authored-candidate', json.dumps(result))
        self.assertNotIn('request.txt', json.dumps(result))

    def test_invalid_pins_captures_grants_and_fake_eligibility(self):
        if os.name != 'posix':
            self.setup_work()
            return
        original = self.fixture()
        mutations = [lambda s: s['tasks'][0].update(commit='abc'),
                     lambda s: s['tasks'][0].update(repository='../escape'),
                     lambda s: s['tasks'][0].update(license=''),
                     lambda s: s['tasks'][0]['license_capture'].update(sha256='0' * 64),
                     lambda s: s['tasks'][0]['provenance'].update(path='../escape'),
                     lambda s: s['tasks'][0].update(status='eligible'),
                     lambda s: s.update(executed=1),
                     lambda s: s.update(registered_assignments=True),
                     lambda s: s.update(host_isolation='authenticated'),
                     lambda s: s['tasks'].append(copy.deepcopy(s['tasks'][0]))]
        for index, mutate in enumerate(mutations):
            intake = copy.deepcopy(original)
            mutate(intake)
            with self.subTest(index=index), self.assertRaises(IntentlineError):
                inspect(intake, self.root)

    def test_private_role_aliases_and_owner_boundary(self):
        if os.name != 'posix':
            self.setup_work()
            return
        intake = self.fixture()
        task = intake['tasks'][0]
        private = {'path': 'private.txt', 'sha256': task['request']['sha256']}
        (self.root / private['path']).write_bytes((self.root / task['request']['path']).read_bytes())
        task['author'] = private
        with self.assertRaisesRegex(IntentlineError, 'Private'):
            inspect(intake, self.root)
        task['author'] = None
        self.root.chmod(0o755)
        try:
            with self.assertRaisesRegex(IntentlineError, 'owner-only'):
                inspect(intake, self.root)
        finally:
            self.root.chmod(0o700)

    def test_cli_refuses_unsafe_without_exposing_input(self):
        import contextlib
        import io
        path = self.root / 'intake.json'
        path.write_bytes(canonical({'private-person': 'Sensitive authored text'}))
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(main([str(path), '--private-root', str(self.root)]), 3)
        self.assertEqual(out.getvalue(), '')
        self.assertNotIn('Sensitive', err.getvalue())

    def test_cross_candidate_private_parent_content_alias(self):
        if os.name != 'posix':
            self.setup_work()
            return
        from intentline.contracts import propose
        from intentline.export import export
        from intentline.records import parse
        # Real native payload validation remains active; only private-role provenance is authored.
        self.assertTrue(self.setup_work())
        propose(self.work, self.draft_path)
        native = self.root / 'native'
        export(self.work, 'proofline-native', native)
        envelope = parse((native / 'native-manifest.json').read_bytes())
        payload = {'envelope': envelope, 'files_utf8': {name: (native / name).read_bytes().decode() for name in envelope['files']}}
        raw = canonical(payload)
        path = self.root / 'parent.json'
        path.write_bytes(raw)
        intake = self.fixture()
        task = intake['tasks'][0]
        (self.root / task['request']['path']).write_bytes(self.source.read_bytes())
        task['request']['sha256'] = sha(self.source.read_bytes())
        task['slicing_parent'] = {'path': path.name, 'sha256': sha(raw)}
        # The other candidate's private reference duplicates a complete parent file, not a visible ref.
        other = copy.deepcopy(task)
        other.update(id='other', slicing_parent=None)
        secret = self.root / 'renamed-gold.txt'
        secret.write_bytes((native / 'contract.json').read_bytes())
        other['reference'] = {'path': secret.name, 'sha256': sha(secret.read_bytes())}
        intake['tasks'].append(other)
        with self.assertRaisesRegex(IntentlineError, 'parent payload'):
            inspect(intake, self.root)
