"""Deterministic Markdown; source text cannot inject tables or raw HTML."""
import html
import re


def safe(value):
    escaped = html.escape(str(value), quote=True)
    escaped = re.sub(r'([\\`*_{}\[\]()#+.!>~-])', r'\\\1', escaped)
    return escaped.replace('|', '&#124;').replace('\r\n', '<br>').replace('\r', '<br>').replace('\n', '<br>').replace('\t', '    ')


def refs(row):
    return '; '.join(f"{r['source_id']}:{r['line_start']}-{r['line_end']} — {r['quote']}" for r in row['source_refs'])


def readable(contract, status, manifest=None):
    """Task-first view; the full identity-bearing Markdown remains available."""
    out = [f"# {safe(contract['intended_outcome'])}", '',
           'Draft plan. Suggested checks have not been run by Intentline.', '']
    flags = status['flags']
    if 'STALE' in flags:
        out.extend(['**Needs attention:** Sources or approval evidence have changed or are unavailable. '
                    'Review and refresh this plan before relying on it.', ''])
    if 'BLOCKED' in flags:
        out.extend(['**Needs attention:** An unresolved decision or adverse review blocks adoption '
                    'and handoff. Settled requirements are still shown below.', ''])
    if 'ADOPTED_ASSERTED' in flags:
        out.extend(['An external approval assertion is recorded; its authority is unverified.', ''])
    elif 'READY_FOR_ADOPTION' in flags:
        out.extend(['A review report recommends adoption; this is advice, not approval.', ''])
    out.extend(['## What should work', ''])
    for row in contract['requirements']:
        out.append(f"- **{safe(row['id'])}:** {safe(row['statement'])}")
        if row['boundaries']:
            out.append('  - Include these cases: ' + safe('; '.join(row['boundaries'])))
    for title, key in [('Constraints to keep', 'constraints'),
                       ('Outside this task', 'out_of_scope'),
                       ('Questions to settle', 'open_decisions')]:
        if contract[key]:
            out.extend(['', '## ' + title, ''])
            for row in contract[key]:
                scope = ' Scope: ' + row['scope'] if 'scope' in row else ''
                out.append('- ' + safe(row['statement'] + scope))
    out.extend(['', '## Suggested checks — not run', ''])
    for row in contract['requirements']:
        out.append(f"- **{safe(row['id'])}:** {safe(row['planned_evidence'])}")
        out.append('  - Expected: ' + safe(row['oracle']))
        out.append('  - Observe through: ' + safe(row['seam']))
    if contract['evidence_gaps']:
        out.extend(['', '## What is needed to check this', ''])
        for gap in contract['evidence_gaps']:
            out.append('- ' + safe(', '.join(gap['requirement_ids']) + ': ' + gap['reason']))
    if contract.get('advisory_notes'):
        out.extend(['', '## Suggestions and context', ''])
        out.extend('- ' + safe(note) for note in contract['advisory_notes'])
    out.extend(['', f"Saved plan: {safe(contract['contract_id'])}, revision {contract['revision']}.", '',
                'For source references, history, technical status, and hashes, '
                'rerun `render` with `--details`.'])
    return '\n'.join(out) + '\n'


def markdown(contract, status, manifest=None):
    out = [f"# Intentline: {safe(contract['contract_id'])}", '',
           f"Status: **{safe(status['status'])}**. Preview / advisory; not authenticated approval or proof.", '',
           f"Contract SHA-256: `{status['contract_sha256']}`", '',
           f"Source bundle SHA-256: `{contract['source_bundle_sha256']}`", '',
           f"Revision: {contract['revision']}", '', safe(contract['intended_outcome']), '',
           '| ID | Required outcome | Basis / source | Boundaries | Seam | Oracle | Planned evidence | Plan state |',
           '|---|---|---|---|---|---|---|---|']
    for r in contract['requirements']:
        cells = [r['id'], r['statement'], r['basis'] + ': ' + refs(r), '; '.join(r['boundaries']) or 'None',
                 r['seam'], r['oracle'], r['planned_evidence'], r['plan_state']]
        out.append('| ' + ' | '.join(safe(v) for v in cells) + ' |')
    for title, key in [('Constraints', 'constraints'), ('Out of scope', 'out_of_scope'), ('Open decisions', 'open_decisions')]:
        out.extend(['', '## ' + title, ''])
        for row in contract[key]:
            extra = ' Scope: ' + row['scope'] if 'scope' in row else ''
            out.append('- ' + safe(row['statement'] + extra + ' Source: ' + refs(row)))
        if not contract[key]:
            out.append('None.')
    out.extend(['', '## Evidence gaps', ''])
    out.extend('- ' + safe(', '.join(g['requirement_ids']) + ': ' + g['reason']) for g in contract['evidence_gaps'])
    if not contract['evidence_gaps']:
        out.append('None.')
    out.extend(['', '## Change notes', ''])
    for note in contract['change_notes']:
        import json
        out.append('- ' + safe(json.dumps(note, ensure_ascii=False, sort_keys=True)))
    if contract.get('advisory_notes'):
        out.extend(['', '## Advisory notes (nonbinding)', ''])
        out.extend('- ' + safe(n) for n in contract['advisory_notes'])
    if manifest:
        out.extend(['', '## Selected sources', ''])
        for source in manifest['sources']:
            out.append('- ' + safe(f"{source['source_id']} {source['role']}: {source['relative_path'] or 'stdin (frozen)'}; SHA-256 {source['sha256']}; authority: {source['declared_authority']}"))
    return '\n'.join(out) + '\n'
