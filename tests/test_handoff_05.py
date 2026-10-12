import copy

from evaluation.handoff_02 import record_evidence
from intentline.errors import IntentlineError
from intentline.export import export as native_export
from intentline.records import canonical, parse, sha
from tests.test_slicing_coverage import CoverageCase


class Handoff05(CoverageCase):
    def test_trust_stop_and_unattempted_coverage_refusal(self):
        if not self.setup_work():
            return
        evidence = {'record': 'intentline.handoff-evidence', 'schema_version': 1, 'state': 'blocked_trust_gate',
                    'blockers': ['Authored trust-stop control'], 'inspection': None, 'external_records': [],
                    'candidate_commit': None, 'coverage': [], 'usage': {'cost': None, 'tokens': None, 'elapsed_seconds': None}}
        out = self.root / 'retained'
        result = record_evidence(evidence, self.root, out)
        self.assertEqual(result['state'], 'blocked_trust_gate')
        self.assertEqual(result['authentication'], 'unverified')
        for key, value in (('coverage', ['Fake PASS']), ('candidate_commit', 'a' * 40), ('usage', {'cost': 0, 'tokens': None, 'elapsed_seconds': None})):
            bad = copy.deepcopy(evidence)
            bad[key] = value
            with self.subTest(key=key), self.assertRaises(IntentlineError):
                record_evidence(bad, self.root, out)

    def test_opaque_fake_pass_never_authenticates_proof(self):
        if not self.setup_work():
            return
        raw = b'Authored fake proof role: PASS; this is not a native runtime receipt\n'
        path = self.root / 'fake-pass.txt'
        path.write_bytes(raw)
        ref = {'path': path.name, 'sha256': sha(raw)}
        evidence = {'record': 'intentline.handoff-evidence', 'schema_version': 1, 'state': 'completed',
                    'blockers': [], 'inspection': ref, 'external_records': [ref], 'candidate_commit': 'a' * 40,
                    'coverage': ['Authored declared coverage'], 'usage': {'cost': None, 'tokens': None, 'elapsed_seconds': None}}
        out = self.root / 'asserted-only'
        result = record_evidence(evidence, self.root, out)
        retained = parse((out / (result['evidence_sha256'] + '.json')).read_bytes())
        self.assertEqual(retained['authentication'], 'unverified')
        self.assertIn('does not authenticate proof or approval', retained['qualification'])

    def test_rehashed_missing_exclusion_cannot_inherit_exact_adoption(self):
        if not self.setup_split():
            return
        from tests.compatibility.proofline_native_input import adopted_intentline, inspect_bundle
        out = self.root / 'native'
        native_export(self.work, 'proofline-native', out)
        metadata = inspect_bundle(out)
        request = {'path': out, 'contract_sha256': metadata['contract_sha256'],
                   'source_chain_sha256': metadata['source_chain_sha256'], 'bundle_sha256': metadata['bundle_sha256'],
                   'approval_reference': 'Authored trusted-caller control; no real adoption'}
        adopted_intentline(**request)
        marker = parse((out / 'native-manifest.json').read_bytes())
        # A new self-consistent proposal is data; the old exact caller adoption must still refuse it.
        for filename in ('contract.json', 'history.json'):
            value = parse((out / filename).read_bytes())
            contract = value if filename == 'contract.json' else value[-1]
            contract['out_of_scope'] = []
            raw = canonical(value)
            (out / filename).write_bytes(raw)
            marker['files'][filename] = sha(raw)
        marker['contract_sha256'] = marker['files']['contract.json']
        (out / 'native-manifest.json').write_bytes(canonical(marker))
        with self.assertRaises((ValueError, OSError)):
            adopted_intentline(**request)
