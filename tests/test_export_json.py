"""Existing JSON producer shape for optional Proofline mapping; no peer runtime."""
import contextlib
import io
import json
from unittest.mock import patch

from intentline.adoption import adopt
from intentline.cli import main
from intentline.contracts import inspect, propose
from intentline.export import export
from intentline.paths import Directory
from intentline.records import canonical, sha
from tests.support import WorkCase
from tests.test_adoption import approval


class AdvisoryJSONExports(WorkCase):
    def test_single_original_json_cli_preserves_advisory_producer_contract(self):
        self.source.write_bytes('Reject empty and whitespace-only usernames\r\nKeep valid usernames unchanged\nDo not add authentication for ø users\r\n'.encode())
        if not self.setup_work():
            return
        self.draft['requirements'][0]['plan_state'] = 'gap'
        self.draft['evidence_gaps'] = [{'requirement_ids': ['R1'], 'reason': 'Executable harness not yet selected'}]
        self.draft['constraints'] = [{'statement': 'Keep valid usernames unchanged', 'basis': 'request',
                                     'scope': 'Valid usernames', 'source_refs': [{'source_id': 'S1', 'line_start': 2,
                                     'line_end': 2, 'quote': 'Keep valid usernames unchanged'}]}]
        self.draft['out_of_scope'] = [{'statement': 'Do not add authentication for ø users',
                                     'source_refs': [{'source_id': 'S1', 'line_start': 3, 'line_end': 3,
                                                      'quote': 'Do not add authentication for ø users'}]}]
        pointer = propose(self.work, self.write_draft(self.draft))
        out = self.root / 'json-advisory'
        stdout = io.StringIO()
        original_import = __import__

        def without_peer(name, *args, **kwargs):
            if name.split('.')[0] in ('proofline', 'checks'):
                raise AssertionError('No Proofline imports')
            return original_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=without_peer), \
                patch('subprocess.Popen', side_effect=AssertionError('No external commands')), \
                patch('socket.socket', side_effect=AssertionError('No egress')), contextlib.redirect_stdout(stdout):
            self.assertEqual(main(['export', '--work', str(self.work), '--format', 'json', '--out', str(out), '--json']), 0)
        marker_raw = (out / 'export-manifest.json').read_bytes()
        marker = json.loads(marker_raw)
        self.assertEqual(json.loads(stdout.getvalue())['data']['authority'], 'unapproved')
        self.assertEqual(marker_raw, canonical(marker))
        identity = {key: pointer[key] for key in ('contract_id', 'revision', 'contract_sha256', 'source_bundle_sha256')}
        self.assertEqual(marker, {'record': 'intentline.export', 'schema_version': 1, 'format': 'json',
                                 **identity, 'advisory': True, 'authority': 'unapproved', 'files': marker['files']})
        self.assertEqual(set(marker['files']), {'contract.json', 'source-manifest.json', 'source-S1.txt'})
        self.assertEqual({p.name for p in out.iterdir()}, {'export-manifest.json', *marker['files']})
        for name, digest in marker['files'].items():
            self.assertEqual(sha((out / name).read_bytes()), digest)
            self.assertEqual((out / name).stat().st_mode & 0o777, 0o600)
        self.assertEqual(out.stat().st_mode & 0o777, 0o700)
        self.assertEqual((out / 'source-S1.txt').read_bytes(), self.source.read_bytes())
        source_raw = (out / 'source-manifest.json').read_bytes()
        self.assertEqual(source_raw, (self.work / 'source-manifest.json').read_bytes())
        self.assertEqual(sha(source_raw), marker['source_bundle_sha256'])
        source = json.loads(source_raw)['sources'][0]
        self.assertEqual(source['source_id'], 'S1')
        self.assertEqual(source['sha256'], sha(self.source.read_bytes()))
        self.assertEqual(source['bytes'], len(self.source.read_bytes()))
        contract_raw = (out / 'contract.json').read_bytes()
        self.assertEqual(contract_raw, canonical(self.draft))
        self.assertEqual(sha(contract_raw), marker['contract_sha256'])
        contract = json.loads(contract_raw)
        self.assertEqual([r['id'] for r in contract['requirements']], ['R1'])
        for category in ('requirements', 'constraints', 'out_of_scope'):
            for row in contract[category]:
                for ref in row['source_refs']:
                    lines = self.source.read_bytes().decode().splitlines(keepends=True)
                    exact = ''.join(lines[ref['line_start'] - 1:ref['line_end']])
                    self.assertEqual(ref['quote'], exact.removesuffix('\n').removesuffix('\r'))
        self.assertEqual(contract['evidence_gaps'], self.draft['evidence_gaps'])

        assertion = self.root / 'approval.json'
        assertion.write_bytes(canonical(approval(pointer)))
        adopt(self.work, pointer['contract_sha256'], assertion)
        adopted = export(self.work, 'json', self.root / 'asserted-json')
        self.assertEqual(adopted['authority'], 'operator_asserted_unverified')
        self.assertEqual(adopted['files'], marker['files'])
        self.assertEqual(inspect(self.work)[0]['authentication'], 'unverified')

    def test_json_completion_marker_is_last_and_interruption_is_recoverable(self):
        if not self.setup_work():
            return
        propose(self.work, self.draft_path)
        out = self.root / 'interrupted-json'
        original_write = Directory.write

        def interrupt(directory, name, data, replace=False):
            if name == 'export-manifest.json':
                self.assertEqual({p.name for p in out.iterdir()} - {'.writer.lock'},
                                 {'contract.json', 'source-manifest.json', 'source-S1.txt'})
                raise OSError('Interrupted before completion')
            return original_write(directory, name, data, replace)

        with patch.object(Directory, 'write', interrupt):
            with self.assertRaisesRegex(OSError, 'Interrupted'):
                export(self.work, 'json', out)
        self.assertFalse((out / 'export-manifest.json').exists())
        partial = {p.name: p.read_bytes() for p in out.iterdir()}
        complete = export(self.work, 'json', out)
        self.assertEqual(complete, export(self.work, 'json', out))
        for name, data in partial.items():
            self.assertEqual((out / name).read_bytes(), data)

