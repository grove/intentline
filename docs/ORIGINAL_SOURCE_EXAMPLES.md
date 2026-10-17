# Original-source grounding — development probes for #44

These are **authored development probes**, not observed agent outputs,
authenticated policies or runtime findings. Suggested observations are advisory
**PROPOSED — NOT RUN**. The before/after templates in
`evaluation/original-source-probes.json` extend the existing semantic probes and
exercise capture/citation mechanics through `tests/test_original_source_probes.py`;
passing them does not measure model behavior or runtime efficacy. No new schema,
retrieval service, capture
ceremony, audit stage or adoption/publication authority is introduced.

Each probe has its own illustrative S1 request and S2 selected context. Labels
such as "Original policy" describe the authored scenario, not authenticated
authorship. An audit can locate a promise or propose a repair without becoming
the authority for that promise.

## 44-report: an audit restates its own expectation

S1 line 1: "Repair filtering while preserving the documented comparison results."

S2 contains:

1. "Original policy: preserve query correctness."
2. "Original comparison promise: projecting lhs < 5 returns NULL for NULL lhs,
   TRUE below 5, and FALSE at or above 5."
3. "Agent-authored audit: NULL lhs must return FALSE; use helper X to repair it."

**Before:** R1 cites the broad policy and audit and requires FALSE for NULL plus
helper X. Disclosing that the audit is agent-authored does not support either
detail. Neither a hash, existing code/tests nor structural validity settles it.

**Expected correction:** R1 uses `basis: project_constraint`, with detailed
`source_refs` to S2 line 2. It preserves the scope of a *projected comparison*;
a WHERE-only observation cannot distinguish FALSE from NULL. For nullable `lhs`
values NULL, 4, 5 and 6, plan a public projection expecting NULL, TRUE, FALSE and
FALSE. A FALSE result for NULL would falsify the promise. Do not require helper X.
The request to repair filtering is S1's outcome; applying the comparison promise
to that repair is the planner's explained inference, not a new original quote.
Keep the audit's recommendation and that reasoning in `advisory_notes`.

Use `basis: request` when the request itself specifies the detailed outcome.
Use `necessary_invariant` only for an inference necessary to preserve a cited
original-request outcome, explaining the connection. Do not relabel every audit
recommendation as an invariant or treat a broad policy as its detailed support.
In an issue, cite the same original line beside the proposed criterion and label
the inference and report separately; a saved JSON record is optional.

## 44-exception: a later recommendation contradicts an accepted exception

S1 line 1: "Repair retry scheduling without changing the accepted retry policy."

S2 contains:

1. "Accepted policy: retry failed operations up to three times."
2. "Accepted exception: payment writes must never retry."
3. "Later agent-authored audit recommendation: retry forever, including payment writes."

**Before:** R1 promotes the later report to unlimited retries in every scope.
**Expected correction:** cite S2 lines 1–2 together using
`basis: project_constraint`; retain both the parent rule and payment-write
exception in `constraints` with their scopes. Keep the later recommendation
advisory. Recency and an agent's claim of success do not supersede accepted rules.

Plan to induce failure through the public retry interface: observe at most three
retries outside payment writes and zero retries for payment writes. This catches
both unlimited retries and applying the parent rule inside the exception. The
planner infers that a scheduling repair must preserve both cases from S1; no
independent authority or successful runtime observation is asserted.

## 44-unavailable: useful provisional work with two different unknowns

S1 contains:

1. "Reject empty input."
2. "Decide separately whether tabs-only input is empty."

S2 line 1: "Agent-authored audit: accept tabs-only input; the original whitespace
policy is unavailable."

**Before:** R1 accepts tabs solely on the audit's recommendation and requires
recapturing the request before any planning can continue.

**Expected correction:** return a clearly **provisional** proposal retaining R1,
reject empty input, with `basis: request` and S1 line 1. The missing whitespace
policy leaves tabs-only behavior **UNKNOWN**; retain D1, an outcome
`open_decisions` item citing S1 line 2. Keep the suggested acceptance of tabs in
`advisory_notes` with the missing original support identified. Do not convert the
report into product policy, invent a decision, automatically fetch sources or
require a mandatory capture ceremony before returning useful proposed work.

Separately, this authored setup supplies no callable validator or manual public
observation path. R1's settled empty-input expectation therefore has
`plan_state: gap` and an `evidence_gaps` entry. That infrastructure gap is not the
reason for D1. The corrected saved fixture is structurally accepted but remains
**BLOCKED** by the actual outcome decision; that status does not discard R1.
Without exact original request bytes or an available CLI, return the provisional
text and disclose incomplete persistence rather than inventing a saved contract.

For all three cases, a tracker edit changes only the authorized issue content.
It does not update a saved contract. Disclose that separation when relevant;
use existing revisions/amendments only for a separately requested record change.
Never silently recapture requests, overwrite saved lineages or publish private
captures. Public fixtures here are authored illustrations, not private captures.
