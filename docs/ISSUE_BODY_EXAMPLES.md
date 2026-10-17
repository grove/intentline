# Concise issue bodies and historical draft identities

These are authored before/after examples for #45, not captured agent outputs or
observed product bugs. Full offline descriptions and issue snapshots are in
`tests/fixtures/issue_body_examples.json`, checked by
`tests/test_issue_body_examples.py`. The checks protect these examples and
instruction delivery; they do not establish provider writes or agent efficacy.
No tracker issue or saved agreement is changed by these checks.

## Two findings from one audit

The authored request S1 promises visible row order (line 1) and parseable fields
containing commas (line 2). The sampled export code S2 appears to use storage order
(line 10) and raw field joins (line 20). These are illustrative source locators,
not links to a real repository or authenticated policy.

**Before:** The issue describes each finding and repeats the same audit account
after each: source inspection at snapshot `fixture-v1`, unknown working-tree
identity, bounded export-path sampling, no tests/builds, unconfirmed runtime
effects, non-verbatim/incomplete request capture, no attached private captures,
and the limits of structural checks.

**After:** Start with the concrete problem: "Downloading a table may lose its
visible order or corrupt fields containing commas. Both concerns need runtime
confirmation." Keep the following finding-specific content, then include the
shared evidence limits once:

- G1 / R1: cite S1:1 and S2:10; require visible order. Verification
  **PROPOSED — NOT RUN**: sort [2,1] to [1,2], download, independently parse and
  require [1,2]. Preserve counterevidence that an uninspected caller may sort.
- G2 / R2: cite S1:2 and S2:20; require a comma-containing field to round-trip.
  Verification **PROPOSED — NOT RUN**: download "a,b" as one field and independently
  parse it as one value. Preserve the missing runnable harness and uncertainty
  about caller-side escaping.
- Keep the open product decision: header naming is **UNKNOWN**.

The full shorter fixture removes only the repeated shared account. It retains
every finding, source locator, acceptance promise, proposed observation,
counterevidence, decision, and evidence limitation. No word count or mandatory
provenance section follows from this example.

## Acceptance refinement with an unchanged historical draft

An authorized update clarifies the existing hidden-row boundary; it does not add
a new promise. The fixture uses hashes of explicitly authored plain-text draft
and source surrogates, **not a validated Intentline record**. They demonstrate
identity preservation without inventing a validation result or private capture.

**Before:** R1 promises visible row order and excludes hidden rows. Its proposed
check says only to compare downloaded order with the visible table. A footer
lists the original contract/source hashes without distinguishing revised text.

**After:** Keep R1 and make the proposed check concrete: display [1,2] with row 3
hidden, independently parse the download, require exactly [1,2], excluding row 3.
Retain both original hash values and add:

> Historical draft identity — the hashes identify the original saved draft and
> source bundle, not the revised issue text. This edit did not create or validate
> a new saved revision.

Keep the non-verbatim/incomplete-source disclosure and "No runtime tests ran."
The unchanged rollout paragraph, title, comments (including the hidden-row
decision), labels, assignees, state, custom fields, attachments, links, and
milestone survive in the full before/after snapshots. Saved draft/source bytes
are identical. The revised description is not newly validated or approved.

A real UPDATE still re-reads affected fields and relevant decisions immediately
before writing, reconciles changes, uses an available concurrency guard, and
verifies the result. A re-read without that guard is not atomic. If preservation
is uncertain, return a patch. Offline snapshots do not exercise those provider
operations. Updating the saved agreement requires a separate request.

## Already concise: UNCHANGED

Before and after are byte-identical in the fixture:

```text
Download visible rows in displayed order. Source: authored request S1:1.
R1 (proposed): Keep visible order and exclude hidden rows.
Verification (PROPOSED — NOT RUN): Parse a download and compare with visible rows.
Evidence gap: the download harness is unavailable.
```

There is no material refinement to make. Report **UNCHANGED** and skip the write;
do not add provenance boilerplate or invoke a CLI to manufacture an identity.

## Complete GitHub issue examples

These complete bodies illustrate the creation default when no repository template
applies. Every source and receipt below is authored and fictional; no runtime
check ran. The first example's receipt is part of its fictional premise, not
evidence produced by Intentline. Existing concise issues above remain unchanged.

### Small bug with an applicable runtime receipt

Premise: request S1:1 requires downloads to preserve visible row order. A receipt
for `example-v1`, with no local changes, records storage rows `[2,1]`, a visible
ascending sort `[1,2]`, and downloaded rows `[2,1]` through the download button.
It records the browser/settings and exact steps. No other candidate is covered.

```markdown
Downloading a sorted table puts its rows back in storage order. The file should
keep the order shown on screen so people do not have to sort it again.

## Evidence

Authored request S1:1 requires visible order. The supplied runtime receipt records
visible [1,2] but downloaded [2,1] on example-v1 with no local changes, using the
download button under its recorded browser/settings. This confirms that case;
other revisions and paths remain untested.

## Acceptance criteria (proposed)

- [ ] **R1:** Downloaded rows retain the visible table's order. Source: S1:1.

## Verification — PROPOSED — NOT RUN

1. **R1:** Retain the receipt's regression: load [2,1], sort to [1,2], download
   through the button, and independently parse the file. Expect exactly [1,2].
   Reuse the receipt within its candidate/scope; no redundant confirmation gate
   is needed. This proposed regression has not run against a repair.
```

### Complex finding that still needs confirmation

Premise: request S1:1 requires a maintained count to equal committed source rows;
S1:2 requires one consumer's recovery to preserve another's pending committed
work. Code sample S2:10 suggests a rebuild might leave already-counted history
eligible for replay. An uninspected caller may advance that history safely.
The sample does not establish runtime failure or a particular repair strategy.

```markdown
Rebuilding a maintained row count may count the same committed change twice,
leaving the count higher than the source rows. This concern comes from source
inspection only; runtime reproduction has not run.

**Confirm before fixing:** Confirm or refute this concern on current code before
changing production behavior; start with Verification below.

## Evidence

Authored request S1:1 requires count/source parity; S1:2 protects another
consumer's pending committed work during recovery. Sample S2:10 suggests that
rebuild may leave already-counted history eligible for replay. Counterevidence:
an uninspected caller may advance that history safely. A later full refresh
could mask duplicate application, so inspect the actual refresh path.

## Acceptance criteria (proposed)

- [ ] **R1:** After rebuild and catch-up, the maintained count equals the committed
  source row count without counting a change twice. Source: S1:1.
- [ ] **R2:** Rebuilding A preserves B's pending committed work so B can reach the
  independently expected count. Source: S1:2. No recovery algorithm is prescribed.

## Verification — PROPOSED — NOT RUN

1. **R1:** Initialize A with one source row and count 1. Pause incremental
   refresh, commit a second row, rebuild A, then resume incremental refresh.
   Independently expect 2 from the committed rows before any corrective full
   refresh. Record the actual path; a masking fallback is inconclusive.
2. **R2:** Initialize A and B at count 1 on the same one-row source. Commit a
   second row and refresh only A; verify B remains at 1 with work pending.
   Rebuild A, then let B catch up. Independently expect B to reach exactly 2,
   with its pending change neither lost nor doubled. Observe retained history
   or an explicit protected baseline; checking only A is insufficient.

Record the tested revision/local changes, material environment/settings, steps,
expected versus actual results, and actual execution path. Add test-only
observation instrumentation if needed; do not incorporate the repair into the
reproducer. If confirmed, record runtime evidence, then repair and retain the
regression within authorized scope. If refuted/already fixed, record
counterevidence and recommend correction or closure. If inconclusive, identify
the evidence gap and keep the concern unconfirmed; a skipped check is inconclusive.

## Open decisions and evidence gaps

Evidence gap: the sample lacks a runnable harness that can pause refresh and
observe replay before a corrective full refresh. The count outcomes are settled;
this is missing observation infrastructure, not an unresolved product decision.

<details>
<summary>Provenance</summary>

Bounded source inspection at authored snapshot example-v1; working-tree identity
unknown. Only the rebuild path was sampled. Request capture is non-verbatim and
incomplete; private captures are not attached. No saved Intentline draft exists.
These notes establish neither whole-repository coverage nor approval or proof.

</details>
```

### Ordinary feature request

Premise: request S1:1 asks for a comma-separated values (CSV) download preserving
visible order; S1:2 requires comma-containing fields to round-trip. People currently
copy the rows by hand. No saved draft, unresolved decision, or evidence gap exists.

```markdown
People currently copy table rows by hand to use them in a spreadsheet. Add a
comma-separated values (CSV) download that keeps the order shown on screen,
so they can transfer those rows without manual copying.

## Evidence

Authored request S1:1 asks for CSV download in visible order; S1:2 requires
comma-containing fields to round-trip. This is a feature request, not a runtime
defect claim. Implementation and verification have not run.

## Acceptance criteria (proposed)

- [ ] **R1:** Downloaded rows retain the visible table's order. Source: S1:1.
- [ ] **R2:** A field containing a comma round-trips as one field. Source: S1:2.

## Verification — PROPOSED — NOT RUN

1. **R1:** Display rows [1,2] after sorting storage rows [2,1], download, and
   independently parse the file. Expect exactly [1,2] in that order.
2. **R2:** Download a row with one field containing "a,b" and independently parse
   it as CSV. Expect one field whose value is exactly "a,b".
```

The small bug and feature omit empty decisions/gaps and provenance. The complex
finding keeps its evidence level and execution status visible while collapsing
the longer audit account. A real existing saved identity would be retained once,
with the historical-draft disclosure above when applicable; no identity is invented
to fill the layout. None of these bodies authorizes implementation or closure.
