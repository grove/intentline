# Acceptance schema 1

JSON is authoritative. Markdown is a deterministic view. The published
`schema/acceptance-v1.schema.json` matches the standard-library validator's
supported subset: strict objects, arrays, strings, integer bounds, enums,
constants, and patterns. Identity/history checks are additional constraints.

Canonical bytes are UTF-8 JSON, sorted keys, compact separators, literal Unicode,
no non-finite numbers, followed by one LF. Duplicate keys are rejected before
validation. SHA-256 of these bytes identifies a contract revision. The source
bundle digest hashes the canonical versioned manifest, which includes each
capture's byte length, SHA-256, role, ID, declared authority, root, original
location, relative path and filesystem identity. Captures are rehashed on reads.
Relocation creates a new source identity. A stdin request is explicitly frozen;
there is no live origin to revalidate.

Requirements use stable `R1`, `R2`, ... and `planned`/`gap` only. Each includes
statement, basis, source_refs, boundaries, seam, oracle, planned_evidence,
plan_state. Basis is `request`, `project_constraint`, or `necessary_invariant`.
Invariants must point to supporting original-request outcomes. Project
constraints must cite selected context, whose authority remains unverified.
Semantic applicability is for the planner/auditor, not a structural check.

Source references contain `source_id`, 1-based inclusive `line_start`/`line_end`,
and the exact quoted lines (optionally omitting only the final CR/LF terminator).
Constraints contain statement, basis, source_refs, scope. Exclusions contain
statement and source_refs. Decisions contain `D1` IDs, statement, source_refs,
and kind `outcome` or `authority_conflict`; either blocks adoption/handoff.
Evidence gaps contain requirement_ids and reason; they are separate from product
ambiguity. Every `gap` row needs a matching explicit gap. Advisory notes are
optional nonbinding text.

Revision 1 starts with `{"revision":1,"kind":"initial"}`. Subsequent revisions
retain earlier notes and append revision, kind `revision`, reason,
previous_contract_sha256, mappings, retired_ids, claimed_authority. Mappings have
`from`/`to` ID arrays and a reason; deletions must be accounted for exactly.
Changed rows need a mapping; unchanged rows retain IDs; retired IDs never return.
Split/merge mappings explain changes but do not prove semantic preservation.
Any byte-changing proposal needs the next revision and invalidates earlier
current adoption. Exact reruns reuse the same immutable record.

`current.json` atomically points to a numbered immutable revision. Audits and
adoptions live separately and bind exact contract/source hashes. Hashes are
identity, not authority. Structural validation never proves completeness.

Status reports applicable flags: DRAFT, STRUCTURALLY_VALID, READY_FOR_ADOPTION,
ADOPTED_ASSERTED, BLOCKED, STALE. STALE/BLOCKED override advanced statuses.
Historical snapshots do not make changed live sources fresh.
