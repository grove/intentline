import copy
import os
from unittest.mock import patch

from intentline.amendments import amend_source
from intentline.continuity import reconcile
from intentline.contracts import inspect, propose
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical, sha
from intentline.review import review
from tests.support import WorkCase


class SuccessorCase(WorkCase):
    def successor(self, work=None, contract=None, refresh=False, contexts=None):
        work, contract = work or self.work, contract or self.draft
        amendment = self.root / ('amend-' + contract['contract_id'] + '.md')
        amendment.write_bytes(b'Disable retries by default\r\n')
        out = self.root / (contract['contract_id'] + '-next')
        result = amend_source(work, None if refresh else str(amendment), contexts or [], self.root, out, sha(canonical(contract)), refresh)
        draft = copy.deepcopy(contract)
        draft.update(contract_id=contract['contract_id'] + '-next', revision=1,
                     source_bundle_sha256=result['source_bundle_sha256'], change_notes=[{'revision': 1, 'kind': 'initial'}])
        mapping = {'record': 'intentline.continuity', 'schema_version': 1,
                   'predecessor_contract_sha256': sha(canonical(contract)),
                   'predecessor_source_bundle_sha256': contract['source_bundle_sha256'],
                   'contract_sha256': sha(canonical(draft)), 'source_bundle_sha256': draft['source_bundle_sha256'],
                   'mappings': [{'from': [r['id']], 'to': [r['id']], 'disposition': 'preserved',
                                 'reason': 'Mechanically unchanged, semantic audit required', 'source_refs': r['source_refs']} for r in contract['requirements']],
                   'added_requirement_ids': [], 'other_changes': []}
        draft_path = self.root / 'successor-draft.json'; draft_path.write_bytes(canonical(draft))
        mapping_path = self.root / 'continuity.json'; mapping_path.write_bytes(canonical(mapping))
        return out, draft, mapping, draft_path, mapping_path


class Amendments(SuccessorCase):
    def test_repeated_exact_amendments_and_historical_staleness(self):
        if not self.setup_work(): return
        propose(self.work, self.draft_path)
        original = (self.work / 'source-manifest.json').read_bytes()
        self.source.write_text('Old origin changed')
        out, draft, mapping, dp, mp = self.successor()
        self.assertEqual(inspect(out)[0]['status'], 'BLOCKED')
        with self.assertRaisesRegex(IntentlineError, 'reconcile'): propose(out, dp)
        reconcile(out, dp, mp)
        self.assertNotIn('ADOPTED_ASSERTED', inspect(out)[0]['flags'])
        self.assertEqual(review(out)['sources']['S1'].encode(), (self.work / 'source/S1.txt').read_bytes())
        second, d2, m2, d2p, m2p = self.successor(out, draft)
        reconcile(second, d2p, m2p)
        self.assertEqual(list(review(second)['sources']), ['S1', 'S2', 'S3'])
        self.assertEqual((self.work / 'source-manifest.json').read_bytes(), original)
        self.source.write_bytes((self.work / 'source/S1.txt').read_bytes())
        self.assertNotIn('ADOPTED_ASSERTED', inspect(second)[0]['flags'])

    def test_continuity_refuses_missing_alias_and_false_preserved(self):
        if not self.setup_work(): return
        propose(self.work, self.draft_path)
        out, draft, mapping, dp, mp = self.successor()
        for mutate in ('missing', 'duplicate', 'false_preserved', 'subject'):
            bad, changed = copy.deepcopy(mapping), copy.deepcopy(draft)
            if mutate == 'missing': bad['mappings'] = []
            if mutate == 'duplicate': bad['mappings'] *= 2
            if mutate == 'false_preserved': changed['requirements'][0]['statement'] = 'Invented meaning'; bad['contract_sha256'] = sha(canonical(changed))
            if mutate == 'subject': bad['predecessor_contract_sha256'] = '0' * 64
            dp.write_bytes(canonical(changed)); mp.write_bytes(canonical(bad))
            with self.assertRaises(IntentlineError): reconcile(out, dp, mp)
            self.assertFalse((out / 'current.json').exists())
        dp.write_bytes(canonical(draft)); mp.write_bytes(canonical(mapping)); reconcile(out, dp, mp)

    def test_changed_request_requires_new_amendment_and_initial_atomicity(self):
        if not self.setup_work(): return
        propose(self.work, self.draft_path)
        out, draft, mapping, dp, mp = self.successor()
        draft['requirements'][0]['statement'] = 'Disable retries by default'
        mapping['mappings'][0]['disposition'] = 'changed'
        mapping['contract_sha256'] = sha(canonical(draft))
        dp.write_bytes(canonical(draft)); mp.write_bytes(canonical(mapping))
        with self.assertRaisesRegex(IntentlineError, 'explicit amendment'): reconcile(out, dp, mp)
        ref = {'source_id': 'S2', 'line_start': 1, 'line_end': 1, 'quote': 'Disable retries by default'}
        draft['requirements'][0]['source_refs'] = [ref]
        mapping['mappings'][0]['source_refs'] = [ref]
        mapping['contract_sha256'] = sha(canonical(draft))
        dp.write_bytes(canonical(draft)); mp.write_bytes(canonical(mapping))
        original = Directory.write
        def interrupt(directory, name, data, replace=False):
            if name == 'current.json': raise OSError('interrupted pointer publication')
            return original(directory, name, data, replace)
        with patch.object(Directory, 'write', interrupt):
            with self.assertRaises(OSError): reconcile(out, dp, mp)
        self.assertEqual(inspect(out)[0]['status'], 'BLOCKED')
        reconcile(out, dp, mp)
        self.assertEqual(inspect(out)[1], draft)
        self.assertEqual(reconcile(out, dp, mp)['revision'], 1)
        (out / 'successor-complete.json').unlink()
        with self.assertRaises((IntentlineError, FileNotFoundError)): inspect(out)

    def test_context_only_refresh_and_unsafe_inputs(self):
        if not self.setup_work(): return
        policy = self.root / 'policy.md'; policy.write_text('Accepted policy\n')
        work = self.root / 'context-work'
        from intentline.sources import prepare
        captured = prepare(self.source, [str(policy)], self.root, work)
        self.draft['source_bundle_sha256'] = captured['source_bundle_sha256']
        propose(work, self.write_draft(self.draft))
        with self.assertRaisesRegex(IntentlineError, 'changed sources'): self.successor(work, self.draft, True, [str(policy)])
        policy.write_text('Revised policy\n')
        out, draft, mapping, dp, mp = self.successor(work, self.draft, True, [str(policy)])
        reconcile(out, dp, mp)
        self.assertEqual([s['role'] for s in review(out)['source_manifest']['sources']], ['request', 'context'])
        policy.unlink()
        self.assertEqual(inspect(out)[0]['stale_sources'], ['S2'])
        link = self.root / 'link.md'; link.symlink_to(self.source)
        with self.assertRaises(IntentlineError): amend_source(work, str(link), [], self.root, self.root / 'unsafe', sha(canonical(self.draft)))
        self.assertFalse((self.root / 'unsafe').exists())

    def test_tampered_predecessor_capture_and_chain_limit(self):
        if not self.setup_work(): return
        propose(self.work, self.draft_path)
        out, draft, mapping, dp, mp = self.successor()
        with patch('intentline.amendments.MAX_DEPTH', 0):
            with self.assertRaisesRegex(IntentlineError, 'eight'): self.successor()
        with patch('intentline.amendments.MAX_ARCHIVE', 1):
            with self.assertRaisesRegex(IntentlineError, '32 MiB'): self.successor()
        capture = next((out / 'archive').glob('*.txt')); capture.write_text('tampered')
        with self.assertRaisesRegex(IntentlineError, 'Tampered'): reconcile(out, dp, mp)

    def test_capture_and_reconciliation_races_and_writer_lock(self):
        if not self.setup_work(): return
        propose(self.work, self.draft_path)
        out, draft, mapping, dp, mp = self.successor()
        with Directory(out) as work, work.lock():
            with self.assertRaisesRegex(IntentlineError, 'Conflicting'): reconcile(out, dp, mp)
        original = Directory.write
        def race(directory, name, data, replace=False):
            result = original(directory, name, data, replace)
            if name == 'continuity.json': (self.root / 'amend-username-validation.md').write_text('changed during reconciliation')
            return result
        with patch.object(Directory, 'write', race):
            with self.assertRaisesRegex(IntentlineError, 'STALE'): reconcile(out, dp, mp)
        self.assertFalse((out / 'current.json').exists())
        self.assertFalse((out / 'successor-complete.json').exists())
