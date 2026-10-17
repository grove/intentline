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

## 0.5 readiness

Reuse these evaluators and rubrics; no model runner or new scoring framework.
[Independent intake](INTAKE_05.md) prepares incomplete private packets and a
read-only diagnostic. [First-use observation](USABILITY_05.md) requires actual
consenting participants; [slicing preparation](SLICING_05.md) preserves the matched
full-parent comparison and useful NO SPLIT. [Native handoff](PROOFLINE_HANDOFF.md)
now records the current consumer's S6 trust stop separately from ordinary missing
host/budget prerequisites. The live consumer gate cannot be lifted by producer CI.

Distinct 0.5 public development registrations/receipts have zero eligible tasks,
assignments and executions. Private preparation has nine selected candidates across
three projects and four provisional source-bound parents; two explicitly AI-authored
upstream requests were excluded and retained privately. No authenticated task/gold
author, reviewer, output scorer, isolated host or model/cost grant exists. Source
history/license suitability needs review. All unknown measurements remain null.

```sh
python -B -m evaluation.planning_02 report evaluation/results/planning-05-not-run.json --private-root evaluation
python -B -m evaluation.slicing_04 report evaluation/results/slicing-05-not-run.json --private-root evaluation
```

Content-hash guards now reject renamed and cross-task private answer/review leaks,
including arm instructions and complete parent-file copies. Task reviews must
precede registration; scoring must follow it. These mechanical controls do not
authenticate independence or detect semantic/partial/encoded answer exposure.
Existing schemas, rubric dimensions and historical bytes remain unchanged, with
exact 0.4 source/output and earlier evidence inventories under baseline_05.

## 0.6 AI-only development lane

`ai_development_06.py` is a read-only adapter for already-produced private
AI-development artifacts. It reuses the existing rubric, secure file reads,
assignment accounting and usage primitives, while preserving the formal studies
and their eligibility rules. [Exact record specification](AI_DEVELOPMENT_06.md).
No model runner, inference authority or human-independent validity is added.
`baseline_06` freezes the exact merged 0.5 code/skill/schema/evidence identities
and public authored source/CLI controls; these are engineering fixtures.

[Delegated preparation](CODEX_PREPARATION_06.md), [access gates](AGENT_ACCESS_06.md),
[blind judging](CODEX_JUDGING_06.md), [control types](JUDGE_CONTROLS_06.md) and
[operator runbook](RUNBOOK_06.md) are prepared. Public authored controls and a
reproducible dated empty receipt are separate from private source/AI-ledger work.
Actual planning comparison/calibration remain not_run; see
[scorecard](../docs/SCORECARD_0.6.md). Complete private inputs cannot be mounted to
shared agents and called isolated. No human-independent evidence was produced.

## Issue #41 — optional test-design handoff feasibility (NOT_RUN)

**Status as of 17 October 2026: NOT_RUN.** Zero independently qualified
tasks, zero randomized/matched assignments, zero agent executions, zero
independent scores, and no measured impact on implementation quality, elapsed
time or token cost. The example in the portable planning skill is **authored
instructional material**, not an observed model result. This proposal does not
reopen the historical 0.6 study or authorize spending, source access or tests.

Before any experiment, independently select and freeze a **small pilot** of
fresh real requests (suggest four to six) with negative/compatibility boundaries,
a low-risk control and an unresolved expected-behavior control. Retain exact
source, project version, source permission, private withheld behavioral oracles,
model/agent version, host/tools, total time/token budgets, and stop thresholds.
Qualify genuinely independent task/answer reviewers and keep grader/control
information out of agent context. This planning note is **not a registration**
for a qualified external study.

Predeclare matched comparisons with no extra budget for the treatment:

- **A:** ordinary agent planning.
- **B:** the current baseline portable Intentline planning skill, pinned to its
  pre-change revision.
- **C:** the changed portable planning skill with selective test-design hints.
- Separately consider the inexpensive direct prompt *"identify the most important
  missing negative/boundary tests"* before claiming C adds value over simpler
  prompting; register it as a comparator if resources permit, not as an
  uncounted advantage for C.

For all assigned attempts, retain initial/final outputs, completed and
blocked/refused/interrupted/NOT_RUN outcomes, timing and token use including
setup, and any unknown costs. Have blinded, independent reviewers assess
**source support**, **independent expected results**, **ability to distinguish
plausible defects**, **feasibility of the suggested check**, **appropriate
UNKNOWN rather than invented outcomes**, and **unnecessary low-risk noise**.
Count full-request implementation correctness only if separate authorized,
qualified implementation runs with withheld oracles actually occur.

**Predeclare a useful-gain and acceptable-overhead threshold before any run.**
If C adds no independently confirmed value over B and cheap review, or costs
too much, **SIMPLIFY / STOP**. Choose **KEEP MINIMAL CHANGE** only if its extra
benefit and cost justify doing so; treat underpowered, unqualified or ceiling
results as **INCONCLUSIVE**. Even a positive pilot does not establish general
efficacy or justify a new schema, CLI, runner, or mandatory testing phase.

## Issue #43 — feasible planned-check development examples

The [authored examples](../docs/PLANNED_CHECK_EXAMPLES.md) cover transient versus
replacement history, ordered shared-shadow preservation, a nullable comparison
operand separate from its primary key, an unspecified outcome, grouped equivalent
boundaries and a routine low-risk control. They are advisory **PROPOSED — NOT RUN**,
not observed agent outputs or runtime findings. Instruction/link/packaging checks
do not measure improved agent behavior. No efficacy comparison was run for #43;
any such comparison needs its own actual evidence and all-in cost accounting.
The #41 **NOT_RUN** status and historical study records remain unchanged.

## Issue #44 — original-source grounding development probes

The [authored probes](../docs/ORIGINAL_SOURCE_EXAMPLES.md) in
`original-source-probes.json` extend the existing semantic probes with a
self-supporting audit expectation, an accepted policy and scoped exception
contradicted by a later report, and unavailable
original support. Corrections distinguish original scope, planner inference,
advisory recommendations, outcome decisions and observation gaps. The offline
tests exercise record/citation mechanics and instruction consistency only;
no model evaluation, runtime efficacy or authenticated authority is claimed.
