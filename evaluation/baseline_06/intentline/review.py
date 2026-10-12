"""Read-only display and mechanical comparison; viewing never adopts."""
from .audits import reports
from .contracts import current, inspect
from .errors import IntentlineError
from .paths import Directory, text
from .records import canonical, sha
from .render import markdown, safe
from .schemas import AUDIT
from .sources import bundle


def difference(old, new):
    before = {r['id']: r for r in old['requirements']} if old else {}
    after = {r['id']: r for r in new['requirements']}
    return {
        'kind': 'mechanical', 'semantic_equivalence': 'not_established',
        'added': [after[i] for i in after if i not in before],
        'removed': [before[i] for i in before if i not in after],
        'changed': [{'before': before[i], 'after': after[i]} for i in after
                    if i in before and before[i] != after[i]],
        'unchanged_ids': [i for i in after if i in before and before[i] == after[i]],
        'other_changes': {k: {'before': old[k], 'after': new[k]} for k in
                          ('intended_outcome', 'constraints', 'out_of_scope', 'open_decisions', 'evidence_gaps')
                          if old and old[k] != new[k]}}


def review(work_path, against_revision=None):
    with Directory(work_path) as work:
        manifest, blobs, digest = bundle(work)
        c, pointer, history = current(work, manifest, blobs, digest)
        predecessor_evidence = None
        continuity = None
        if manifest['schema_version'] == 2:
            from .amendments import archives
            predecessor_evidence, archived_files = archives(work, manifest)
            from .records import parse
            continuity = parse(work.read('continuity.json')[0])
        if against_revision is not None:
            if type(against_revision) is not int or not 1 <= against_revision <= len(history):
                raise IntentlineError('Comparison revision is unavailable')
            old = history[against_revision - 1]
        else:
            old = history[-2] if len(history) > 1 else (predecessor_evidence['history'][-1] if predecessor_evidence else None)
        audits = reports(work, 'audits', AUDIT)
        status, checked = inspect(work_path)
        if checked != c:
            raise IntentlineError('Current revision changed during review', 3)
        active_audits = [a for a in audits if all(a[k] == pointer[k] for k in ('contract_sha256', 'source_bundle_sha256'))]
        disputes = [a for a in active_audits if a['outcome'] != 'READY_FOR_ADOPTION']
        source_states = [{'source_id': s['source_id'], 'role': s['role'],
                          'provenance': s.get('provenance', 'explicit_frozen_stdin' if s['original_location'] is None else 'current'),
                          'support': 'stale' if s['source_id'] in status['stale_sources'] else 'frozen_historical' if s.get('provenance') == 'frozen_historical' else 'captured_current_or_explicit_stdin'}
                         for s in manifest['sources']]
        diff = difference(old, c)
        old_identity = None if old is None else {
            'contract_id': old['contract_id'], 'revision': old['revision'],
            'contract_sha256': sha(canonical(old)), 'source_bundle_sha256': old['source_bundle_sha256']}
        summary = ['# Agreement review', '', 'Viewing does not adopt, authenticate or prove this agreement.', '',
                   'Comparison: ' + ('no predecessor' if old is None else f"revision {old['revision']}"), '',
                   'Added: ' + ', '.join(safe(r['id']) for r in diff['added']),
                   'Removed: ' + ', '.join(safe(r['id']) for r in diff['removed']),
                   'Changed: ' + ', '.join(safe(r['after']['id']) for r in diff['changed']),
                   'Mechanically unchanged: ' + ', '.join(safe(i) for i in diff['unchanged_ids']), '',
                   'Semantic equivalence requires audit; matching IDs are insufficient.', '',
                   f"Current audits: {status['current_audits']}; recorded assertions are unverified.", '']
        if old_identity:
            summary.extend(['Previous contract: ' + safe(old_identity['contract_id']) + '; SHA-256 `' + old_identity['contract_sha256'] + '`',
                            'Previous source bundle SHA-256: `' + old_identity['source_bundle_sha256'] + '`', ''])
        for kind in ('added', 'removed'):
            for row in diff[kind]:
                summary.append(kind.capitalize() + ': ' + safe(row['id'] + ' — ' + row['statement']))
        for change in diff['changed']:
            for field, value in change['after'].items():
                if value != change['before'].get(field):
                    summary.append('Changed ' + safe(change['after']['id'] + ' ' + field) + ': ' + safe(canonical(change['before'].get(field)).decode().strip()) + ' → ' + safe(canonical(value).decode().strip()))
        for field, change in diff['other_changes'].items():
            summary.append('Changed ' + safe(field) + ': ' + safe(canonical(change['before']).decode().strip()) + ' → ' + safe(canonical(change['after']).decode().strip()))
        for state in source_states:
            summary.append('Source: ' + safe(state['source_id'] + ' ' + state['role'] + '; ' + state['support']))
        for report in active_audits:
            summary.append('Audit: ' + safe(report['outcome']) + '; reported independence ' + safe(report['reported_independence']) + '; authentication unverified')
            for finding in report['findings']:
                summary.append('- ' + safe(finding['id'] + ': ' + finding['consequence'] + '; evidence: ' + finding['evidence'] + '; correction: ' + finding['correction']))
        return {**status, 'contract': c, 'source_manifest': manifest,
                'sources': {sid: text(data) for sid, data in blobs.items()}, 'source_states': source_states,
                'predecessor': old_identity, 'diff': diff,
                'continuity': continuity, 'predecessor_evidence': predecessor_evidence,
                'archived_evidence': {name: text(data) for name, data in archived_files.items()} if predecessor_evidence else {},
                'advisory_mappings': c['change_notes'][-1].get('mappings', []),
                'audits': audits, 'audit_disputes': disputes, 'adoption_boundary': 'operator_asserted; authentication unverified',
                'markdown': '\n'.join(summary) + '\n\n' + markdown(c, status, manifest)}


def approval_request(work_path):
    display = review(work_path)
    return {**display, 'request': 'intentline.approval-request', 'schema_version': 1,
            'authorization': 'not_established', 'external_decision': None,
            'approval_template': {'record': 'intentline.approval', 'schema_version': 1,
                                  'contract_sha256': display['contract_sha256'],
                                  'source_bundle_sha256': display['source_bundle_sha256'],
                                  'actor': None, 'timestamp': None, 'reference': None},
            'warning': 'An external authorized actor must supply actual adoption bytes. This template is not approval.'}
