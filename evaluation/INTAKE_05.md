# 0.5 independent-task intake

This is preparation for the existing `planning_02.py` and `slicing_04.py`, not a
new evaluator, launcher or independence authority. The public registrations are
development readiness declarations with no tasks or assignments. Model/version,
reasoning, tools and budgets are null/undeclared until actually established.
They do not authorize a pilot. Nine candidates are a research shortlist, not
nine eligible tasks or 27 registered attempts.

## Private packet template

Create a fresh owner-only directory **outside this repository**. Keep a separate
arm-visible source bundle and restricted gold, reviews, outcomes and raw host
receipts. Mode 0700/0600 protects against other OS users; it does **not** isolate
models or agents sharing the owner's account. Arrange actual separate host mounts
or identities and capture the isolation/egress evidence before any run. Never
give a planning arm the entire study root. Do not copy private sources, filenames,
actor identities, answer keys or model transcripts into Git or public issues.

For each prospective task, retain the following privately:

| Item | Required evidence |
|---|---|
| Original project | Independent `owner/repo`, full 40-character upstream commit; exact license text, retrieval URL/time and applicability to issue prose |
| Original request | Exact captured issue/API/chat bytes and independently established provenance; extracted API body identified as that representation, not original keystrokes |
| Context and chronology | Verbatim permitted original documents/code, SHA-256 for every byte stream, timestamps and accepted-versus-proposed decisions, scoped exceptions and rejected approaches |
| Historical suitability | Why the selected source commit represents the actual task; pre-fix snapshot where needed; record any exposed implementation, answer or later decision |
| Study-task author | Accountable independent author capture, task scope, original-source citations, corrections, conflicts and timestamp; upstream issue authorship alone is insufficient |
| Checker/reference | Separately authored private oracle/reference and its authorship/conflict capture; expected behavior must not be derived from candidate implementation |
| Two task/gold reviews | Two further distinct accountable reviewers, original and reference citations, suitability, corrections, conflicts and review captures **before registration** |
| Planning parity | Identical ordered request/context snapshots for ordinary, Intentline and P2P standalone planning; complete substantive sources, not selectively shortened baselines |
| Slicing parity | Independently reviewed complete source-bound parent agreement and originals identical across three slicing arms; never a weakened ordinary parent |
| Execution grant | Actual model/provider IDs and revision, reasoning, tool/egress permissions, isolation, reset state, time/turn/dispatch limits and separately authorized cost ceiling |
| Blind scoring | Unique output IDs, arm labels removed without removing obligations, original-source plus exact-output hashes, two distinct blinded scorers; promise-to-output and output-to-source mappings |
| Resource ledger | Setup/install/initial reads/repairs/audits separately from run cost; available input/output/cache tokens, calls/turns, elapsed time, agent/user actions and actual billed USD; unknowns null |
| Contamination | Prior exposure, overlap with Lore, public development examples, exposed answer keys and AI-transformed material; never relabel these as untouched holdout |

Use the existing task, assignment and score field definitions in the evaluators
and [planning rubric](rubric_02.md). Do not fill missing author/checker fields with
invented participants to satisfy a validator. Incomplete packets remain intake
candidates outside the study. `eligible: true` is an operator declaration requiring
external verification, never something a hash or this tool establishes.

The private intake JSON has `record: intentline.task-intake`, `schema_version: 1`,
`captured_at`, `tasks`, zero `registered_assignments`/`executed`, and nullable
snapshot references for `model_authorization`, `host_isolation`, `blinding_ready`
and `cost_permission`. Each candidate has `id`, `status: candidate_unreviewed`,
`repository`, `commit`, `license`, `license_capture`, `request`, ordered `context`,
`provenance`, `scope`, nullable `author`, `checker`, `reference`, `slicing_parent`,
`reviews` and explicit `blockers`. Author/checker/reviews are private **capture
references**, not claimed actor names. References always contain relative `path`
and SHA-256. The actual prepared private packet is the worked template.

Run this read-only diagnostic with Python 3.11+ on qualified POSIX storage:

```sh
python -B -m evaluation.intake_05 /private/study/intake.json \
  --private-root /private/study
```

It reports counts and numbered missing-artifact categories without source text,
task identifiers, paths, answers or actor names. Map numbers to the private ordered
intake locally. Unsafe files, altered hashes, duplicate captures, false eligibility
claims and private content aliases refuse. It does not verify GitHub authenticity,
license interpretation, reviewer identity, semantic correctness or OS isolation.
Malformed/unsafe intake returns exit 3 without exposing private diagnostic text.

## Actual 12 October preparation

Nine selected candidate packets span three pinned licensed public projects. Eleven
requests were researched; two explicitly AI-authored originals were excluded from
the shortlist and retained privately with reasons. Remaining provenance is still
unverified. Exact issue JSON, original API-body UTF-8, comments, pinned documents,
license text, short document history and timestamped retrieval metadata are stored
privately. Closed issues and exposed solution suggestions are contamination risks;
each candidate needs historical suitability and license review before registration.
No Lore gold or exposed study answers were imported. No untouched holdout exists.

The sanitized [actual preflight](results/intake-05-readiness.json) binds the private
inventory by digest in its accompanying receipt. Every candidate still lacks an
independent study author, checker/reference and two independent task/gold reviews.
Private agent-authored parent drafts, when supplied, are provisional source-bound
inputs requiring the same independent review; they are not gold or observed results.
No actual host isolation, model authorization, blinded scoring or cost grant exists.

## Freeze and execute only after external readiness

Target nine tasks across three projects; six across three is the minimum bounded
diagnostic start, subject to protocol. Freeze a **new** pilot registration using the
existing evaluator only after roles, sources, settings and grants are established.
Register every task against all three arms: nine eligible tasks means 27 assignments.
Keep failed/refused/timeout/interrupted/not_run assignments and every later attempt.
Do not mutate a frozen registration to replace failures or improve the denominator.

The evaluator now rejects private reference/review **content hashes** anywhere in
the corpus's arm instructions or inputs, including renamed copies and parent files.
It also rejects task reviews after registration and scores before registration.
These guards cannot detect paraphrased, partially embedded or encoded answer leaks;
external isolation and semantic intake review remain necessary. Actor names,
timestamps and hashed receipts are assertions, not authenticated runtime evidence.
Unknown usage stays null; unattempted usage cannot be zero. Public fixtures remain
development mechanics and cannot satisfy the eligible population.

For scoring, inspect every original promise and added binding obligation, record
omissions/inventions with source lines and output IDs, retain each scorer's complete
score and disagreements. Scoring citations currently receive structural checks;
the evaluator does not prove complete semantic coverage or validate upstream
authorship. Report critical trust failures separately from average adverse counts.
Use measured comparable denominators only. A diagnostic pilot cannot establish
broad superiority. Register a distinct untouched holdout before any semantic tuning.
