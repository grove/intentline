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
