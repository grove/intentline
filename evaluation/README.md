# Planning 0.2 diagnostic protocol

This directory inspects already produced external records. It never launches
models, repo tests, Git, or agents. Python 3.11+ standard library only. Use a
private owner-only directory outside tracked files for original requests, answers,
outputs, registration, provenance and scores. Never commit private pilot data.

```
python -B -m evaluation.planning_02 validate STUDY.json --private-root /private/study
python -B -m evaluation.planning_02 assess STUDY.json --private-root /private/study
python -B -m evaluation.planning_02 report STUDY.json --private-root /private/study
```

All operations read only; report prints sanitized aggregates. Secure file reads
reuse Intentline's no-follow/regular-file/2-MiB limits and fail closed on Windows.
Hashes bind bytes; this tool does not authenticate execution or reviewers.
Study JSON itself must be preserved by the operator in immutable private records.
Every referenced snapshot has a relative `path` and `sha256`; registration and
review evidence are also bound snapshots. The checked development example and
`tests/test_evaluation.py` describe the complete record format. Inputs and results
are bounded by the existing file limit; at most 100 tasks/64 contexts per task.

Register 9 real tasks from at least 3 distinct pinned repositories (minimum 6/3)
BEFORE execution. Separate development/pilot/holdout registrations. Each task
pins full commit, license, scope, exact original request and original documents.
Every arm receives the same request/context and task presentation; private gold,
reviewer notes and scores never enter model context. Give ordinary planning the
same opportunity to inspect sources. Do not leak answers through names, caches,
agent instructions or pre-solved patches. Task requests must depend on genuine
project history, not merely checker preferences.

Task author and checker are distinct; two additional reviewers inspect the task,
source constraints and reference outcome. Retain timestamps, conflicts, citation
corrections and externally established identity/isolation records. Missing people
or records make a task ineligible. Declared eligibility remains unverified by this
program. A source hash, named actor or fabricated host record is not independent
review. Public regression examples are development material, never real trials.

Three preregistered arms: ordinary agent planning; same agent with Intentline 0.2;
P2P plan-acceptance skill alone. Match model/version/reasoning, tools, time budget,
sources and presentation. Attribute all unavoidable differences, installation and
preparation effort. No P2P delivery controller. Every task has all three assignment
records, including failed/refused/timeout/interrupted/not_run; never delete adverse
attempts. Reruns are separate registered studies with retained predecessors.

Scores receive only opaque blind IDs, original sources and substantive outputs
with source-to-output mappings. Remove system/arm clues before independent scoring
while preserving substance; retain the original output hash. Two blinded scorers
record all rubric dimensions and source citations. Subject/score digests are
rechecked. Reviewer disagreement is retained; aggregate adverse counts use the
larger reviewer count per assignment. Failure states remain in denominators.
Unknown usage/billing is null. Sum only fully known metrics, including preparation.
Wilson 95% descriptive intervals are diagnostic, not efficacy claims.

Initial external study: not_run. Missing: independently eligible task/checker/two
reviewer records, qualified isolated hosts and pinned execution models, explicit
external inference budget/spending authorization. No ambient credentials used.
The holdout remains unregistered and untouched; no holdout outcomes were read.

## 0.3 external evaluation status

Reuse the same three-arm protocol and rubric. `results/planning-03-not-run.json`
and its distinct `cases/registration_03.json` bind the 0.3 arm instructions without
rewriting the 0.2 registration. There are zero eligible tasks, zero assignments
and zero completed, failed, refused, timed-out or interrupted real arm attempts.
All unknown preparation/execution tokens, billing, latency and effort remain
null; no efficacy estimate or superiority claim follows from offline tests.
Task/checker/two-reviewer records, isolated hosts, matched pinned models, blind
scorers and explicit inference authorization are unavailable. No holdout is
registered, read or tuned. Public lifecycle fixtures are engineering regressions.

`results/proofline-native-03-not-run.json` separately records live native delivery
as not_run. Offline native admission uses the exact separately owned Proofline
snapshot pinned in `tests/compatibility/native-identity.json`; shared validator
ancestry is disclosed and does not imply independent review. A real run still
needs actual caller adoption, spending/host authorization and candidate/review/
proof/status receipts. No inference or external effect runs in this protocol or CI.

## Separately registered 0.4 slicing extension

The original planning_02 evaluator, registrations, receipts and rubric are unchanged.
`slicing_04.py` adapts that evaluator's record checks and reuses its unchanged secure
snapshot, usage and interval primitives. It never executes an arm. New arms are
ordinary agent decomposition, Intentline slice, and P2P slice-contract alone;
no delivery controller. It requires the same exact parent acceptance/source-chain
payload for all arms, alongside original source documents. A task's `parent`
snapshot stores {envelope, files_utf8}, the data of a complete native parent bundle;
its source streams must match request followed by context snapshots exactly.
The payload is inspected as advisory data; its scripts are never executed.

```
python -B -m evaluation.slicing_04 validate PRIVATE_STUDY.json --private-root PRIVATE_ROOT
python -B -m evaluation.slicing_04 report evaluation/results/slicing-04-not-run.json --private-root evaluation
```

Register 6–9 genuine pinned licensed tasks from at least three projects before
execution, with separate author/checker and two additional independent task/source/
gold reviews. Bind matched model/version/reasoning/tools/budgets and attributable
preparation. Keep private gold, reviews, outputs and blind scores outside tracked
files. Retain failed/refused/timeout/interrupted/not_run assignments and disagreements;
unknown usage/effort/billing stays null. External isolation/identity must be actually
established; names, hashes and this validator do not authenticate independence.
Use the separate [slicing rubric](rubric_04.md); do not modify the registered
three-arm planning comparison or tune a holdout. No model spending is authorized.

The public 0.4 development registration has zero tasks and assignments; it is
readiness evidence only. It preregisters arm instructions and protocol without
claiming a genuine pilot exists. New real tasks/settings require a separate frozen
pilot registration before any run. The dated not_run receipt names missing humans,
qualified hosts, pinned models, budgets and blind scoring. No measured benefit,
actual acceptance, cost savings or independent review is claimed.
