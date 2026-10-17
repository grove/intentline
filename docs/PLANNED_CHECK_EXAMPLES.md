# Feasible planned checks — development examples for #43

All sources and handoffs below are **authored illustrations**. They are not
captures of pg-trickle issues, observed agent outputs, executable tests or
runtime findings. All suggested scenarios are advisory **PROPOSED — NOT RUN**.
Text/packaging regressions check instruction delivery, not improved agent behavior.
These examples refine the existing semantic pass and issue verification fields;
they introduce no schema, artifact requirement, audit or model stage.

Each example has its own illustrative S1 source. Expected results come from
that quoted source and the stated inputs, never from the implementation under
review. Evidence methods are suggestions, not additional product obligations.

## 1. Transient history is not replacement history

Authored S1, line 1: "After polling refresh, the consumer must match committed
source rows, including transient INSERT→DELETE, same-key replacement and rolled-back
changes; replaying intermediate operations is not required."

**R1:** Match committed source rows. Keep these histories as boundaries of R1,
not three requirements. Start each variation with known rows `(1, 'old')` and
`(9, 'keep')` in source and consumer, and pause polling until the stated commits
or rollback finish. Observe consumer rows through its public query after refresh:

- **Transient:** insert previously absent `(2, 'temp')`, commit; delete key 2,
  commit; then refresh. Expect exactly `(1, 'old'), (9, 'keep')`, with no key 2.
  A stale inserted row would falsify R1. A replacement scenario does not exercise
  this genuinely transient history, even if both use INSERT and DELETE.
- **Replacement:** delete key 1, commit; insert `(1, 'new')`, commit; then refresh.
  Expect exactly `(1, 'new'), (9, 'keep')`. A missing or old key 1 falsifies R1.
- **Rollback:** insert `(2, 'temp')` in a transaction and roll it back before
  refresh. Expect exactly the initial rows; a visible key 2 falsifies R1.

All three checks cite S1 line 1. Final rows are the promised observation; do not
invent an intermediate-event replay obligation. If polling cannot be paused or
the refresh completion cannot be observed, record that missing harness as an
`evidence_gaps` entry for R1, not an unresolved product outcome.

## 2. Preserve a second consumer's pending work

Authored S1, line 1: "Repairing consumer A must restore A to committed source rows."
Authored S1, line 2: "Consumer B sharing the polling shadow must retain its pending
changes and show them at its next refresh after A's repair."

**R1:** Restore A (line 1). **R2:** Preserve B's pending changes (line 2).
These are distinct independently acceptable outcomes, so R2 can have its own
stable ID. Adding more setup detail to either row creates no further requirement.
One ordered scenario can cover both rows:

1. Initialize source, A and B to exactly `(1, 'old')`. Pause both consumers;
   use the harness's supported setup to place A on the repair path. B must
   still share the same polling shadow and must not refresh during the repair.
2. In a source session, insert `(2, 'pending')` and commit. B has not consumed
   this change. Invoke A's repair and wait for completion before resuming B.
3. Query A: expect exactly `(1, 'old'), (2, 'pending')` (R1).
4. Refresh B, wait for completion and query B: independently expect exactly
   `(1, 'old'), (2, 'pending')` from the fixture and S1 line 2 (R2).

A destructive shared-shadow reset may make step 3 correct while leaving B with
only `(1, 'old')` at step 4. Merely creating B, checking A, inspecting shadow
metadata, or computing B's expectation from A would miss the preservation outcome.
If the harness cannot hold B pending or select A's repair path, retain that
specific evidence gap; do not pretend the ordering is feasible in that harness.

## 3. A nullable comparison operand separate from the primary key

Authored S1, line 1: "For lhs < 5, return SQL NULL when lhs is NULL, TRUE below 5,
and FALSE at or above 5."

**R1:** Preserve the stated comparison results (S1 line 1), grouping NULL,
below, equal and above boundaries in one row. Use `id INTEGER PRIMARY KEY` and
a separate nullable `lhs INTEGER`. Seed `(id, lhs)` as `(1, NULL), (2, 4),
(3, 5), (4, 6)`. Plan to project `id, lhs < 5 AS matches` through the selected
comparison execution path and inspect results by id. Independently expect
`(1, NULL), (2, TRUE), (3, FALSE), (4, FALSE)`.

This catches coercing UNKNOWN to FALSE or mishandling the equality boundary.
A primary-key `lhs` cannot carry the NULL case. A WHERE filter alone removes
both FALSE and UNKNOWN, so it cannot distinguish the promised projected results.
Confirm the fixture reaches the selected comparison path without an earlier
NULL filter. If that path has no observable projection seam, record R1's missing
harness in `evidence_gaps` (`plan_state: gap` if no credible path exists).
The source already settles NULL behavior, so this is not an outcome decision.

## 4. Unspecified outcome control

Authored S1, line 1: "Select rows whose non-null score is below 5; the treatment
of NULL scores is undecided."

**R1:** Select non-null scores below 5 (S1 line 1). A planned public-result check
with scores 4, 5 and 6 expects only the score-4 row; it catches an inclusive
comparison. **D1, outcome:** Should a NULL score row be selected? Expected result
for NULL is **UNKNOWN**. Retain D1 in `open_decisions`; do not copy SQL semantics
from example 3 into this different source. No invented pass/fail assertion and
no evidence gap in place of this genuine outcome choice.

## 5. Equivalent boundaries share an existing scenario

Authored S1, line 1: "Reject empty and whitespace-only usernames; leave valid
usernames unchanged."

**R1:** Reject empty/whitespace-only usernames. Keep empty, spaces and tabs in
one row's `boundaries`. If an existing scenario E1 already submits `''`, `' '`
and `'\t'` through the public validator and expects rejection from S1 line 1,
reference E1 in `planned_evidence`; do not duplicate it as three R rows or impose
a per-boundary test quota. E1 catches a spaces-only trim that accepts tabs.
**R2:** Leave valid usernames unchanged (same source). Plan to submit `'alice'`
and compare the observed username with that exact input, catching blanket rejection
or mutation. Grouping R1's variations must not erase the distinct preservation
promise in R2.

## 6. Routine low-risk control

Authored S1, line 1: "Rename the button label from Save to Save draft."

**R1:** Show "Save draft" on the button (S1 line 1). Its existing fields suffice:
`seam`: rendered button; `oracle`: exact source-specified label;
`planned_evidence`: inspect the rendered button text and compare with "Save draft".
No extra scenario list or separate handoff is useful. Do not invent click behavior,
new requirements or a framework mandate. This remains a plan, not an executed check.
