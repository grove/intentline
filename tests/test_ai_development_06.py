"""Authored mechanics only; no real model output or human review."""
import copy
import contextlib
import io
import json
import os
from pathlib import Path
from unittest.mock import patch

from evaluation import ai_development_06 as ai
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical, parse, sha
from tests.support import WorkCase


class AIDevelopment(WorkCase):
    def ref(self, name, value, kind):
        raw = value.encode() if isinstance(value, str) else canonical(value)
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return {'path': name, 'sha256': sha(raw), 'size': len(raw), 'kind': kind}

    def register(self, study):
        study['registration'] = self.ref('receipts/registration.json', ai.sealed(study), 'registration')
        return study['registration']['sha256']

    def fixture(self, empty=False):
        arms = {arm: {'model_id': None, 'version': None, 'reasoning': None, 'seconds': None,
                      'tools': [], 'differences': [],
                      'instructions': self.ref('instructions/'+arm+'.txt', 'Authored '+arm+' fixture', 'instructions')}
                for arm in ai.ARMS}
        task = {'id': 'private-task', 'kind': 'authored_control', 'repository': 'example/control',
                'commit': 'a'*40, 'license': self.ref('sources/license.txt', 'Authored license fixture', 'license'),
                'provenance': self.ref('sources/provenance.txt', 'Authored provenance', 'provenance'),
                'request': self.ref('visible/request.txt', 'Keep retries unchanged\n', 'source'),
                'context': [], 'reference': None, 'critique': None, 'agents': [],
                'source_decision': 'unreviewed', 'contamination': ['Authored unit-test case']}
        population = [{'task': task['id'], 'arm': arm, 'blind_id': '%032x' % i} for i, arm in enumerate(ai.ARMS)]
        runs = [{**entry, 'state': 'not_run', 'inputs': [task['request']],
                 **dict.fromkeys(('output', 'neutral', 'mapping', 'prompt', 'transcript', 'execution')),
                 'scores': [], 'metrics': dict.fromkeys(ai.USAGE)} for entry in population]
        study = {'record': 'intentline.ai-development-study', 'schema_version': 1, 'mode': 'ai_only_development',
                 'phase': 'development', 'registered_at': '2026-10-12T18:00:00Z', 'registration': None, 'authorization': None,
                 'arms': arms, 'tasks': [] if empty else [task], 'population': [] if empty else population,
                 'assignments': [] if empty else runs,
                 'judge_calibration': {'status': 'not_run', 'protocol': None, 'judges': [], 'receipts': [],
                                       'metrics': dict.fromkeys(ai.USAGE), 'judging_metrics': dict.fromkeys(ai.USAGE)},
                 'isolation': {'mode': 'shared', 'receipts': []}, 'preparation': dict.fromkeys(ai.USAGE),
                 'blockers': ['budget', 'host', 'isolation', 'sources', 'calibration'],
                 'decision': 'insufficient_or_unqualified_evidence'}
        self.register(study)
        return study

    def check(self, study):
        return ai.assess(study, self.root, study['registration']['sha256'])

    def test_frozen_05_bytes_and_public_source_identity_controls(self):
        root = Path(__file__).resolve().parents[1]
        baseline = root / 'evaluation/baseline_06'
        identity = parse((baseline/'identity.json').read_bytes())
        self.assertEqual(identity['commit'], '8c17d093ae77e2b1588f9671fc586aa733a0a801')
        for name, expected in identity['files'].items():
            self.assertEqual(sha((baseline/name).read_bytes()), expected, name)
        for name, expected in identity['preserved'].items():
            self.assertEqual(sha((root/name).read_bytes()), expected, name)
        from intentline.contracts import contract_check
        contract = parse((baseline/'captures/contract.json').read_bytes())
        manifest = parse((baseline/'captures/source-manifest.json').read_bytes())
        source = (baseline/'captures/source.txt').read_bytes()
        contract_check(contract, manifest, {'S1': source}, contract['source_bundle_sha256'])
        with self.assertRaises(IntentlineError):
            contract_check({**contract, 'source_bundle_sha256': '0'*64}, manifest, {'S1': source}, contract['source_bundle_sha256'])

    def test_read_only_and_sanitized_all_commands(self):
        if os.name != 'posix':
            self.setup_work(); return
        study = self.fixture()
        path = self.root/'study.json'; path.write_bytes(canonical(study))
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(Directory, 'write', side_effect=AssertionError('write')), patch('subprocess.Popen', side_effect=AssertionError('dispatch')), patch('socket.socket', side_effect=AssertionError('network')):
            for operation in ('validate', 'assess', 'report'):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    self.assertEqual(ai.main([operation, str(path), '--private-root', str(self.root),
                                              '--registration-sha256', study['registration']['sha256']]), 0)
                for forbidden in ('private-task', 'example/control', 'request.txt', str(self.root), 'Keep retries'):
                    self.assertNotIn(forbidden, out.getvalue())
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        result = self.check(study)
        self.assertEqual(result['status'], 'offline_prepared')
        self.assertEqual(result['registered_assignments'], 3)
        self.assertEqual(result['actual_attempts'], result['formal_eligible_tasks'], 0)
        self.assertIsNone(result['all_in_usage']['cost'])

    def test_registration_denominator_identity_and_usage_refusals(self):
        if os.name != 'posix':
            self.setup_work(); return
        original = self.fixture()
        mutations = [lambda s: s.update(mode='human_independent'), lambda s: s.update(eligible=True),
                     lambda s: s['tasks'][0].update(author='fictional-human'),
                     lambda s: s['assignments'].pop(),
                     lambda s: s['assignments'][0].update(blind_id=s['assignments'][1]['blind_id']),
                     lambda s: s['assignments'][0]['metrics'].pop('tokens'),
                     lambda s: s['assignments'][0]['metrics'].update(cost=0),
                     lambda s: s['assignments'][0].update(state='completed'),
                     lambda s: s['tasks'][0]['request'].update(path='/etc/passwd'),
                     lambda s: s['tasks'][0]['request'].update(path='visible/../escape'),
                     lambda s: s['arms']['ordinary'].update(tools=['extra'])]
        for i, mutate in enumerate(mutations):
            study = copy.deepcopy(original); mutate(study)
            with self.subTest(i=i), self.assertRaises(IntentlineError):
                self.check(study)
        study = copy.deepcopy(original); pin = study['registration']['sha256']
        study['tasks'][0]['commit'] = 'b'*40
        self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'External registration'):
            ai.assess(study, self.root, pin)

    def test_whole_corpus_gold_alias_swapped_reference_and_quote_checks(self):
        if os.name != 'posix':
            self.setup_work(); return
        study = self.fixture(); task = study['tasks'][0]
        source = task['request']
        value = {'record': 'intentline.ai-obligation-ledger', 'schema_version': 1, 'task': task['id'],
                 'input_sha256s': [source['sha256']], 'obligations': [{'id': 'O1',
                 'source': {'sha256': source['sha256'], 'line_start': 1, 'line_end': 1, 'quote': 'Keep retries unchanged'},
                 'scope': 'Retry policy', 'severity': 'critical', 'observable': 'Existing retry count retained',
                 'counterexample': 'Deletes retry', 'uncertainty': 'resolved', 'binding': True}]}
        task['reference'] = self.ref('restricted/gold/ledger.json', value, 'reference')
        self.register(study); self.check(study)
        pin = study['registration']['sha256']
        value['task'] = 'different'
        task['reference'] = self.ref('restricted/gold/ledger.json', value, 'reference')
        with self.assertRaises(IntentlineError): ai.assess(study, self.root, pin)
        self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'Reference subject'): self.check(study)
        value['task'] = task['id']; value['obligations'][0]['source']['quote'] = 'Wrong citation'
        task['reference'] = self.ref('restricted/gold/ledger.json', value, 'reference'); self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'Citation quote'): self.check(study)
        value['obligations'][0]['source']['quote'] = 'Keep retries unchanged'
        task['reference'] = self.ref('restricted/gold/ledger.json', value, 'reference')
        study['arms']['ordinary']['instructions'] = self.ref('instructions/renamed.json', value, 'instructions')
        self.register(study)
        with self.assertRaisesRegex(IntentlineError, 'Private reference'): self.check(study)

    def test_hostile_files_and_errors_never_disclose_private_text(self):
        if os.name != 'posix':
            self.setup_work(); return
        study = self.fixture(); path = self.root/'study.json'
        for raw in (b'{"Secret Person":1,"Secret Person":2}', b'{"x":NaN}', b'{}', b'{}\n '):
            path.write_bytes(raw); err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(ai.main(['report', str(path), '--private-root', str(self.root),
                                          '--registration-sha256', study['registration']['sha256']]), 3)
            self.assertNotIn('Secret', err.getvalue()); self.assertNotIn(str(self.root), err.getvalue())
        source = self.root/study['tasks'][0]['request']['path']; saved = source.read_bytes()
        for kind in ('symlink', 'hardlink', 'fifo'):
            source.unlink(); other = self.root/'other.txt'; other.write_bytes(saved)
            if kind == 'symlink': source.symlink_to(other)
            elif kind == 'hardlink': os.link(other, source)
            else: os.mkfifo(source)
            with self.subTest(kind=kind), self.assertRaises(IntentlineError): self.check(study)
            source.unlink(); source.write_bytes(saved)

    def test_empty_not_run_requires_precise_blocker(self):
        if os.name != 'posix':
            self.setup_work(); return
        study = self.fixture(empty=True)
        result = self.check(study)
        self.assertEqual(result['status'], 'not_run')
        self.assertEqual(result['registered_assignments'], 0)
        study['blockers'] = []
        with self.assertRaises(IntentlineError): self.check(study)
