# Intentline 0.6 — AI-Only Empirical Usefulness Evaluation

**Implementation-ready coding-agent handoff · 12 October 2026**  
**Primary repository:** <https://github.com/grove/intentline>  
**Goal:** Make a small, source-grounded **Codex-only development experiment** possible and reproducible; use its actual results to guide the next product improvements, without misrepresenting AI critiques as independent human validation.  
**Inspected Intentline `main`:** `8c17d093ae77e2b1588f9671fc586aa733a0a801` (0.5 PR #30 merged, 2026-10-12 16:18 UTC). Six-cell merged-head CI: <https://github.com/grove/intentline/actions/runs/38276513783> (success). `pyproject.toml` currently says experimental `0.5.0rc1`; no published GitHub Release was found.  
**Inspected Proofline `main`:** `46c503ae23bef70ae410eac67f1b9e62bd1c62e3` (S6 follow-up trust defects remain); see `docs/S6-FOLLOWUP.md`.  
**P2P reference:** `grove/promise-to-proof` at `17f3deb982a8224f71b12bda74be6b24d86571e4` for the frozen 0.5 planning-only arm; recheck the actual upstream revision and bytes before an experiment.  
**Source audit:** check live repository heads, CI and documentation again before modifying or running anything; these hashes describe the inspected baseline, not future branch state.

> **Product question:** On genuine historically grounded software requests, does an agent using Intentline produce materially more complete, correctly scoped and falsifiable acceptance plans than the same agent planning normally or using P2P's standalone planning skill? What additional time, actions, tokens and money does that quality cost?
>
> **Evidence statement:** The release targets an **AI-assisted development diagnostic**, not a human-independent study and not a claim of broad effectiveness. Actual agent runs and source-based observations are empirical development evidence. Separate model contexts, different agent names and a second AI judge do not authenticate human or organizational independence.

## 0. Instructions to the implementing coding agent

**Implement this plan; do not reply with another plan.** Start from actual current `main`; read the specific code and documents below. Finish feasible source analysis, deterministic preparation and tests autonomously. Make focused PR-ready engineering changes in order. If explicitly authorized to create PRs, create real PRs and verify their URLs; merge only under separate authorization and required passing checks. Do not assume GitHub permission equals permission to merge, tag, publish or spend money. Keep exact commit/test/CI identities and record unsuccessful attempts as well as successful ones.

**Experiment permission is separate from engineering permission.** Do not initiate paid Codex/model inference merely because a CLI, API key, session, subscription or connected plugin is available. Require an actual operator-supplied model/provider grant, a total experiment spending cap (or explicitly identified subscription usage limit), a time/call cap, an authorized host and permitted sources. Before such a grant, finish every offline work package and publish an accurate `not_run` receipt. If a grant is provided in the subsequent implementation task, execute within it, retain every outcome and stop at the predefined gates. Never silently change model, reasoning effort, tools, privacy boundary, dataset, task or budget to obtain a more flattering result.

**Scope:** Intentline remains a Python 3.11+ standard-library-only deterministic/offline acceptance tool. Its `intentline-plan`, `intentline-audit`, `intentline-slice`, original source capture, revisions, adoption, slicing and portable export remain independent of all model providers. Implement **no embedded Codex SDK, agent runner, orchestration server, database, provider client, new acceptance schema, or competing evaluation engine** in the production package. Codex subagent orchestration belongs in an external, separately authorized operator environment. New repository code may validate/import **already-produced** experiment artifacts and emit **sanitized read-only reports**.

**Trust and evidence rules:** Never fabricate real historical requests, original upstream authorship, independent humans, signed reviews, authenticated model runs, costs, proper isolation, actual consent, adoption or native Proofline proof. Use exact original files and source snapshots, cite accepted decisions versus proposals and scoped exceptions, and label reconstruction/AI interpretation honestly. Do not commit private research, gold, prompts containing answers, completed model outputs, tokens, transcripts, private host receipts or participant identities to the public repository. Do not replace or edit dated evidence and frozen experiment registrations from 0.1–0.5.

### Required first reads

- Intentline: `README.md`, `pyproject.toml`, `docs/{CONTRACT,CLI,AGENT_GUIDE,TRUST_AND_AUTHORITY,SLICING,SLICING_INTEGRATIONS,SCORECARD_0.5,IMPLEMENTATION_0.5}.md`.
- Existing evaluation: `evaluation/{README,INTAKE_05,USABILITY_05,SLICING_05,PROOFLINE_HANDOFF,rubric_02,rubric_04,FAILURE_LEDGER}.md`; `evaluation/{planning_02,slicing_04,intake_05,package_smoke}.py`; `evaluation/cases/*05*`, `evaluation/results/*05*`, `evaluation/baseline_05/`.
- Code: `intentline/{paths,records,sources,contracts,audits,adoption,continuity,native_handoff,native_inspect,slicing,cli}.py`, all existing `tests/`, `.github/workflows/ci.yml`.
- The three **entire** pinned instruction packages: Intentline `skills/intentline-plan/SKILL.md` plus linked docs/schema; P2P `skills/productivity/plan-acceptance/SKILL.md` plus legitimately required files; ordinary planning instructions. Do not use P2P's controller or Proofline as a scoring authority.
- Current Codex host delegation documentation: <https://developers.openai.com/api/docs/guides/agents-api/multi-agent>, <https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted>, <https://developers.openai.com/api/docs/guides/agents-api/environments/security>. Verify actual Codex CLI/host support and limits at execution time; do not assume the API and CLI expose identical interfaces.
- Proofline follow-up trust status: <https://github.com/grove/proofline/blob/46c503ae23bef70ae410eac67f1b9e62bd1c62e3/docs/S6-FOLLOWUP.md>. **Do not treat a positive Proofline verdict as calibrated independent proof.** Proofline is not used in the primary planning comparison.

## 1. Why this release differs from 0.5

0.5 has useful infrastructure and honest negative evidence: **136 offline tests** in the final engineering suite (135 passing with one real-Windows-only probe skipped on local macOS); six-cell green CI; nine private candidate tasks across three projects, but **zero independently eligible tasks and zero model assignments/runs**; four provisional AI-authored slicing parents; human first-use study not run; native Proofline blocked at a trust gate. The 0.5 source distribution is tagged `0.5.0rc1` in package metadata, not an independently published final release. The existing formal study's requirement for independent human task/checker/reviewer roles cannot be satisfied by naming different Codex subagents.

**Decision:** Establish a **separate, explicitly AI-only development evidence lane** so that we can evaluate actual planning behavior now. Reuse the existing acceptance-quality rubric, snapshot/citation checks, secure file reads, assignment accounting, Wilson interval helper and slicing evaluator where applicable. Preserve the formal human-eligible protocol unchanged and never set its `eligible: true` from AI-only participants. The AI lane must stay visibly outside it.

Three nested but separate questions:

1. **Engineering reproducibility:** Do we capture immutable source/prompt/output/usage identities safely and report all failures?
2. **AI-development diagnostic:** Can source-anchored mechanical checks plus *calibrated, blind AI critics* identify material planning mistakes and directional differences across the three arms?
3. **Externally validated efficacy:** Do authenticated, independent people and an untouched study support a wider conclusion? **Out of scope for 0.6**, and must remain unknown rather than false-positive.

### Intended results, not promised outcomes

- **Minimum development cohort:** three actual historical requests from **three different licensed/pinned repositories**, one complete arm-visible corpus per task. Use relevant entries from 0.5's nine private candidates only when actually accessible and source-appropriate. If the private packet is unavailable on the implementation host, say so and reproduce the source research without inventing retrieval or provenance.
- **Three planning arms:** ordinary Codex planning, the same Codex configuration with Intentline's planning skill, and the same Codex configuration with P2P standalone planning. For three tasks this yields **nine intended assignments**, including failed/blocked/not-run assignments in the denominator.
- **Source-grounded gold:** A private obligation ledger anchored in verifiable original bytes and/or independently executable behavior, challenged by at least one separate AI critic. Treat uncovered interpretation as uncertainty; the ledger is **AI-derived**, not authenticated ground truth.
- **Reliable automated judging:** Calibration on fixed positive/negative source-grounded examples **before judging arm outputs**; two separately initialized blinded AI judge sessions where possible; deterministic citation and coverage cross-checks; explicit unresolved disagreements.
- **Expansion decision:** Only after the initial judge and host gates pass, run a separately registered **six-to-nine-task** diagnostic across at least three projects. Keep development tasks exposed to tuning separate from genuinely unused follow-up cases. A fresh case is not automatically a formal human-reviewed holdout.
- **User/cost signal:** Measure real prompts/actions/manual interventions, model calls, known tokens, elapsed time and available billing. Report null when unavailable, preparation/judging cost separately and in full study cost; never claim zero cost for missing usage.
- **Optional slicing diagnostic:** Reuse `evaluation/slicing_04.py` and its rubric only if credible source-bound parent agreements, budget and source-separated environments are already available. The 0.6 *primary* release gate is acceptance planning, not completion of a child-consumer study.

## 2. Architecture: leverage existing evaluation, not another product

### 2.1 Evidence lanes and status names

Use these exact conceptual distinctions in the new private-record schema and public reports:

| Status | Qualifies | Does **not** qualify |
|---|---|---|
| `offline_prepared` | Source captures, hashes, validity/control fixtures; zero model runs | Usability or model effectiveness |
| `ai_development_unqualified` | Actual agents may have run, but gold isolation, judge calibration or provenance failed | Reliable scored comparison |
| `ai_development_observed` | Actual measured assignments, source-based controls, calibrated blind AI judgments under declared access boundaries | Independent human review, general superiority, authenticated completion |
| `blocked_external` / `not_run` | Exact missing host, budget or source/access prerequisites | Model run, negative model result or a usable empirical denominator |
| `human_independent` | Reserved **only** for a future, separate formally reviewed protocol | **Never produced or inferred by 0.6** |

The existing `intentline.planning-study` and `intentline.slicing-study` formal schemas, `eligible` flag, registered score records and `planning_02.assess`/`slicing_04.assess` semantics stay intact. Their published historical receipts remain immutable. 0.6 outputs a separate record such as `intentline.ai-development-study`, `schema_version: 1`, `mode: ai_only_development`. Do **not** fill the formal `author`, `checker`, `reviews` or `eligible` fields with fictional humans or rebrand subagents as independent reviewers. AI roles use `agent_role`, `model_id`, `run_or_session_id`, `environment_id` (if actually observed), `context_access` and `record_sha256`.

### 2.2 Proposed thin read-only adapter

Add `evaluation/ai_development_06.py` (or a comparably focused evaluation-local module). It must **not** call models, run tests, execute Git, install packages, create files, edit captured data or access the network. It validates privately supplied development-only records and computes sanitized descriptive summaries. Reuse:

- `planning_02.snapshot`, `require`, `private_inputs`/equivalent corpus cross-task hash protection, `number`, `interval`, `DIMENSIONS`, `METRICS`, `STATES` and canonical SHA-256 from `intentline.records`.
- Existing `rubric_02.md` definitions and source-to-output mapping semantics, rather than a second contradictory semantic rubric.
- `slicing_04.parent` plus `rubric_04.md` only for an explicitly separate optional slicing development file.
- `intake_05` for candidate provenance/readiness, without changing its `eligible_count: 0` for AI-prepared packets.

The adapter may have `validate`, `assess`, `report` read-only subcommands, consistent with current evaluators. Propose a private record with bounded, exact fields:

```json
{
  "record": "intentline.ai-development-study",
  "schema_version": 1,
  "mode": "ai_only_development",
  "phase": "development",
  "registered_at": "offset-aware actual timestamp",
  "registration": {"path": "relative/private.json", "sha256": "..."},
  "tasks": ["bounded source/AI-gold/citation/provenance entries"],
  "arms": {"ordinary": {}, "intentline": {}, "p2p_plan_only": {}},
  "assignments": ["every task-by-arm outcome, including not_run"],
  "judge_calibration": {"status": "observed/not_run/failed", "receipts": []},
  "isolation": {"mode": "host-enforced/shared/unverified", "receipts": []},
  "preparation": {"nullable usage and effort" : null},
  "limitations": ["AI-derived oracles and critics are not human-independent"]
}
```

**The above is an illustrative record shape, not existing executable JSON and not a claim of execution.** Define complete exact versioned types before implementing. A private artifact reference is relative to one secure root and binds exact bytes, size, kind and SHA-256. Key fields must be explicit and type-checked; no arbitrary actor-declared `independent: true`. Name the visible-source snapshots, reference ledger, evidence/disagreement records, per-run prompt/output/transcript receipts and actual model configuration separately. Use bounded counts and paths comparable to the existing evaluator; preserve the 2 MiB read bound and reject unsafe/symlink/hardlink/FIFO inputs. Never read gold to create a model-visible artifact in this process.

Prove as tests that malformed or missing records refuse, no unknown usage becomes zero, no failed attempts disappear, post-registration reference changes are rejected, identity swaps across tasks/arms fail, blank/provisional controls cannot be counted as qualified, and all read-only commands have **zero writes/subprocesses/network**. Only aggregates, labels, anonymized IDs and cited publicly shareable short explanations may reach stdout/public docs; source/gold text, participant/host paths and raw outputs stay private.

### 2.3 Codex delegation and *actual* isolation boundary

Use Codex subagents for **bounded role specialization during preparation**, not as a substitute for host security. Recommended delegation:

- Coordinator: chooses source snapshots, allocates private task IDs, schedules stages, hashes receipts and checks gates; never acts as a scorer on its own model-visible output.
- Source researcher: collects accepted decisions, historical exceptions, conflict chronology, upstream request and license/provenance evidence.
- Task drafter: packages an agent-visible request and narrowly permitted source documents, without access to the oracle ledger.
- Oracle/checker agent: derives source-backed obligations **from originals alone**, without any planner output, draft gold answer or previous checker response.
- Adversarial critic: challenges the checker with alternative interpretations, edge cases, scoped exceptions and source citations; preserves disagreements.
- Calibration designer and blind judges: prepare/use fixed independently sourced controls; judges see source + anonymized plan only, not approach labels, other judges' responses, operator expectations or gold author deliberation.

Codex's Agents API permits subagents with separate contexts, **but subagents in one environment share its filesystem and tools**. A new subagent is not a new secure environment. Prefer host-provisioned separate containers/users/mount views for model-visible preparation, gold storage, plan arms and judging. The *trusted host/operator*, not a planning agent, constructs inputs from pinned allowed paths. Use per-run read-only input mounts, distinct writable scratch and independent new sessions; no repo/network/secrets outside the explicit grant. Keep gold and model-judge calibration answers outside **all** planning-arm mounts. Remove/deny ambient MCP, GitHub, egress and tool credentials not authorized for the comparison. Record actual effective permissions and verify canaries. Owner-only sibling directories under the same OS identity, different prompts, separate threads and different subagent names **do not enforce isolation**. If host separation cannot be demonstrated, mark the study `ai_development_unqualified` and do not present it as leak-resistant blind evidence.

Multi-agent does not imply comparable inference spending: record root and all subagent usage or keep it unknown. **For fair planning arms, use three separate, fresh, top-level Codex sessions/environment instances**, with the same model/version/reasoning/time horizon/tools and identical source bytes. Subagents may prepare tasks and critiques; planning arms should use equal agent/delegation privileges or document any irreducible skill-driven difference as part of the measured workflow. Do not accidentally give only Intentline extra tool access, researcher context or model turns for free.

## 3. Required experiment sequence and stop rules

### Gate A — Source validity before model comparisons

From 0.5's nine *private* candidates, choose three prospective requests from three separate projects **by a frozen, source-based rule** (e.g. one with an accepted-versus-proposed decision, one with a scoped exception, one with a negative/regression constraint). Record all nine's eligibility/contamination observations and why each of the three was selected *before seeing 0.6 planning outputs*. Do not choose or replace tasks based on which approach wins. If the candidates are unavailable, research publicly verifiable requests and retain the fact that the original 0.5 packet was inaccessible.

For every selected task, capture privately:

1. Upstream repository, exact 40-hex commit, license text and source copyright/provenance; exact request body/API representation, issue/decision timestamps, repository documentation as it existed at the pinned historical state. An API-extracted body is not invented author keystrokes; an AI-authored upstream request must be labeled as such and excluded from any claim of independently human-authored origin.
2. A *single* canonical ordered input snapshot shared across arms: verbatim request and same selected documents. Keep accepted, proposed, rejected, superseded and scoped-exception chronology visible; do not sneak later solutions, answer keys, post-fix implementation, grading hints or task-specific gold into any input.
3. Source-grounded **obligation ledger**: stable opaque obligation IDs; material promise (including exclusions and negative cases); exact source/file/revision/line excerpts; applicability/scope; severity; independent observable expected result or credible testable method; uncertainty flags. Derive this from the source before model outputs. An AI-authored ledger is a development hypothesis, not authenticated truth.
4. Mechanically verifiable anchors whenever feasible: verbatim requirements/exclusions, deterministic program interface expected values, accepted ADR precedence, negative cases and a plausible violating alternative. Do not equate code behavior with normative specification without the cited source. Never use implementation-under-test output as its own expected oracle.
5. AI critic challenge (in a separate context, with original sources): enumerate missing obligations, source contradictions, unnecessary requirements, wrong authority and alternative valid expected outcomes. Resolve differences only when documentary evidence justifies it; otherwise retain `contested` and omit the unresolved point from decisive pass/fail counts.
6. An immutable private manifest with hashes for source, gold, challenges, AI session/version, exact original source access and every revision. Test all file boundaries before any run.

Gate A passes for *development* only if each of the three tasks has a license/provenance decision, source coverage ledger, no known gold leak into visible sources, a mechanically checked corpus and a challenge log. It does not make a task human-independent. If fewer than three projects qualify, report them and stop the cross-project comparison rather than padding with fabricated tasks.

### Gate B — Judge calibration, **before** real arm outputs

Prepare a small **fixed development control set** grounded in these tasks and source passages, with at least:

- **Positive controls:** two substantively different correct acceptance representations per task (different wording/order/tests; not merely repeated model output), each annotated as *AI-authored development fixtures*, and source-falsifiable expected behavior.
- **Negative controls:** omissions of a material promise, loss of an explicit exclusion, incorrect accepted/proposed authority, deletion of a narrow exception, a candidate-derived oracle, invention of a binding requirement and an unnecessary blocker caused by a missing harness. Include at least one incorrect but superficially plausible plan and one valid alternative the critic must not reject.
- **Deterministic checks:** unchanged source/quote hashes, plan output IDs, existence and polarity of required obligations, permitted required-versus-optional scope, and known source-based negative behavior. A regex/string hit alone cannot certify semantic compliance; it is a supporting control.

Freeze each mutant and its expected observation *before* critic invocation; record the full positive/negative population, not only cases judges get right. Run two fresh blinded AI judge sessions where the host permits, with identical original sources but no arm labels, gold-author transcript, other judge outputs or generated reference essay. One judge may be a different model if authorization and comparable accounting permit; otherwise disclose same-model correlation. Require exact source-line justification and mapped output IDs for every adverse finding. Disagreements produce unresolved items or a separately recorded third AI critique, **never** automatic consensus/independent human certification.

**Predeclared calibration gate:** judges must identify all intentionally seeded *critical source-promise/authority omissions* in this small control set and must not classify either type of grounded correct alternative as a critical defect. Record all secondary errors, ambiguous source interpretations and reliability variation. If the gate fails, label `judge_unqualified`, preserve raw predictions and stop before *using their scores to rank arms*. A correction to the judge or control rubric requires a new pinned control version and a newly registered run; old failures remain. Do not tune controls against concealed arm outcomes. This is a strict smoke criterion, not a claim of statistical reliability from a tiny calibration sample.

### Gate C — Actual nine planning assignments (3 tasks × 3 arms)

**Freeze before the first model call:** exact task/source/corpus hashes; all three frozen skill/instruction trees; model ID/version/reasoning effort; host/CLI version; tools/permissions; context and file mounts; timeout/max turns/dispatches; budget and stopping rules; arm order/randomization seed; output format normalization and identity policy; judge calibration version. Write a sealed manifest/registration inside the **private AI-development study** (never mutate the formal human study registration or public 0.5 declarations).

Run all three arms from fresh sessions, using identical source bytes and equal tool opportunities:

| Arm | Input/instructions | Exclusions |
|---|---|---|
| `ordinary` | Ordinary Codex acceptance-planning instruction and full same permitted source set | No Intentline/P2P skills |
| `intentline` | Whole installed Intentline skill tree, `intentline-plan` and its actual CLI; same originals | No mandatory separate audit, automatic adoption or delivery |
| `p2p_plan_only` | Whole exact P2P `plan-acceptance` instructions/references; same originals | No P2P controller, issue automation, implementation or proof |

Obtain only an acceptance plan, not an implementation. Keep all relevant source and scope obligations; ask for stable rows, citation/seam/oracle/evidence/gaps/decisions. Do not normalize *away* materially absent content merely to make format uniform. Redact visible arm/skill branding for judges while preserving every criterion, exclusion, uncertainty and source reference. Freeze original raw output, stripped output, redaction mapping and SHA-256. A failure to produce parseable output is an adverse outcome, not an excuse to hand-correct or omit the task. No retries unless their policy was frozen, bounded and applied equally; failed attempts stay charged and recorded.

Run first one task as the **declared first assignment batch**, inspect any mechanical/host blocker and stop if source isolation or identity fails; do not silently rerun it or replace it. If healthy, complete the remaining six assignments. Retain full registered denominators even if a gate stops the study early. Actual reference timing and native usage must be captured as reported by the host, including calibration and prep overhead. Internal model API requests may remain unknown; a Codex session count is not a provider request count. Missing tokens/billing are `null`, never zero. Keep a separate total for tasks, preparation, calibration and scoring and an all-in observed-cost subtotal only when every applicable component is known.

### Gate D — Blind scoring and diagnostic decision

After all available assignments have their immutable outputs, apply the **already frozen** two-judge rubric plus source-based deterministic checks. Use the existing seven `rubric_02.md` adverse dimensions:

- `material_omissions`, `invented_obligations`, `constraint_losses`, `decision_errors`, `weak_oracles`, `missing_gap_disclosures`, `unnecessary_blockers`.

For each material source promise cite the plan row(s) or an omission; for each binding plan row cite supporting original text or an invented requirement. Distinguish a *source-certain* critical failure from an AI-contested interpretation. Preserve judge pairs and disagreement counts; publish no single unqualified "accuracy" number. Do not let the judge's own favored implementation become the requirement. Report paired *per-task* comparisons, criterion-level differences, adverse severities, judge reliability/control errors, model cost/latency, operator steps and every refusal/timeout/interruption/not-run attempt. A small three-task diagnosis can identify bugs; it cannot establish general superiority, significance or verified correctness. Empty/blocked runs cannot be silently excluded from any reported completion denominator.

A useful descriptive report includes:

1. Task count, repository diversity, tasks pre-exposed to prompts, exact frozen identities and **AI-only** provenance label.
2. Each arm's assigned/completed/failed/blocked/timeout/not-run counts and judge-qualified vs unresolved counts.
3. Paired critical obligation coverage and unsupported binding requirements by task; clear, source-cited examples and plausible counterexamples where sharing rights allow.
4. All-in and execution-only actual elapsed time, actions, known tokens and billable spend; null or ranges where costs cannot be fully observed. Include model/delegation overhead.
5. Judge control pass/fail, positive-alternative rejection rate, cross-judge agreement and any unadjudicated critical disagreement.
6. A predeclared choice: `fix_specific_defect`, `simplify_overhead`, `insufficient_or_unqualified_evidence`, or `expand_new_tasks`. Record negative/neutral results without burying them.

### Gate E — Expand conditionally, without changing the first outcome

Only if Gates A–D passed and budget is available, prepare a **new, separate registration** for at least three additional never-used source tasks (six distinct tasks total, preferably nine), spanning at least three projects. Freeze task selection, model, judge, rubric and costs before reading their arm outputs. The three development tasks may be used to tune production skill guidance **only after their first results are permanently retained**. Do not claim later tasks are untouched if any source/answer/solution/AI outputs were previously exposed to the planner, oracle author or judge. Report such contamination explicitly. A new failed gate stops expansion and remains visible.

Do not introduce random replacement tasks to rescue a bad score. For any changes to Intentline's skill, create a distinct post-change study rather than rescoring or rewriting earlier outputs; no cross-version pairing without a clearly declared frozen design.

### Optional Gate F — Slicing, only if justified

If qualified parent acceptance contracts and remaining budget are available, run a **separate AI-only slicing diagnostic** with ordinary decomposition, Intentline's `intentline-slice`, and P2P's `slice-contract` against the same frozen full-parent input. Reuse `evaluation.slicing_04`'s input checks and `rubric_04.md`, but keep AI-only eligibility and score labels separate from formal human validation. Include deliberately coherent NO SPLIT cases, unnecessary-cycle controls, inherited exclusions and final integrated parent ownership. Never count child plan success as verified parent delivery and never dispatch advisory child bundles to unsupported Proofline input. If setup requires inventing approved parent agreements or exceeding the granted budget, mark `not_run` and keep the primary study result intact.

## 4. PR-by-PR implementation plan

A PR is a **review unit**, not permission to publish. If PR creation is not authorized, leave PR-ready commits in an isolated local checkout. Prefer the following dependency order; a conditional PR may be omitted honestly.

### PR-01 — Freeze 0.5 and create an explicitly AI-only development evidence adapter (P0)

**Paths:** `evaluation/baseline_06/` (only public and permitted deterministic fixture identities), `evaluation/ai_development_06.py`, `evaluation/AI_DEVELOPMENT_06.md`, `tests/test_ai_development_06.py`. Amend `evaluation/README.md` by *appending* the new lane.

**Work:**

- Freeze the exact 0.5 source/result/schema/skill/evaluator byte identities and representative accepted/refused source-identity CLI outputs. Preserve earlier baselines/scores/receipts byte-for-byte. Make self-contained fixture snapshots immune to host-specific absolute temp paths.
- Implement a small read-only validation/report bridge with its own `record` and `mode`, leveraging `planning_02` data types and helper functions. Formal existing human-eligibility/evaluator semantics are unchanged.
- Validate task/arm/score/agent provenance, absolute boundary denial, private-source leakage, exact declared output hashes, calibration identities, chronological registration, duplicate/cross-task source keys, required attempt population and coverage. AI critics never populate formal independence/authentication fields.
- Make output sanitized aggregates only. Exercise hostile noncanonical input, duplicate keys, alias/symlink/hardlink/FIFO, wrong source, swapped gold, rehashed reference, omitted failed attempt, forged actor, fake native-run receipt, missing usage and unknown billing.

**Tests/exit gate:** existing entire suite passes; new positive AI-development fixture with honestly AI-authored gold is inspectable, and all negative controls refuse. `not_run` with zero attempts is valid only with precise blockers; an arm attempt cannot be mislabeled a completed eligible human study. No model inference in CI.

### PR-02 — Codex delegated case-preparation instructions and source-isolation checks (P0)

**Paths:** `evaluation/CODEX_PREPARATION_06.md`, `evaluation/AGENT_ACCESS_06.md`, `evaluation/cases/ai_06/` for public-license-safe **authored controls only**; `tests/test_ai_case_prep_06.py`; optional minimal read-only file-layout validator integrated into the PR-01 adapter.

**Work:**

- Supply ready-to-use prompts for coordinator, source researcher, task author, independent *AI* obligation drafter and adversarial challenge role. Each prompt specifies **exact allowed input artifact names**, output shape, citation format and no-effect scope. Label role identity, actual model/session and environment. No role may invent independent people.
- Define the private packet directory (`sources/`, `visible/`, `restricted/gold/`, `restricted/critiques/`, `runs/<arm>/<task>/`, `judging/`, `receipts/`) with a trusted host producing **separate actual mounts**. Do not assume a sibling folder is private from another Codex agent.
- Provide a concrete access-control matrix and executable **negative access canaries** the operator can run before inference, with no secrets or gold revealed. Fail closed if a planning agent can read a private sentinel, inspect another arm's session, access the operator answer directory, or invoke unauthorized network/connected apps.
- Specify how to qualify three source-grounded historical tasks across three repos, how to handle the 0.5 shortlist if unavailable, and how to retain rejected/contaminated or AI-authored upstream requests. Freeze source selection and all edits before arm outputs.

**Tests/exit gate:** deterministic packet/source manifests preserve original full commits and exact text; role outputs cannot overwrite each other or model-visible sources; known positive and negative path canaries are validated in the *actual* host if such a host is available. Document any unqualified access/isolation property rather than pretending unit tests certify sandbox behavior. No private case/gold committed.

### PR-03 — Judge calibration, blinded normalization and trustworthy scoring interface (P0)

**Paths:** `evaluation/CODEX_JUDGING_06.md`, `evaluation/JUDGE_CONTROLS_06.md`, `tests/test_ai_judging_06.py`, and focused extensions to `evaluation/ai_development_06.py` only; **do not replace** `rubric_02.md` or `planning_02.py` with a new evaluator.

**Work:**

- Define exact positive/negative control records with source anchors, expected faults and independent correct alternatives. Build deterministic checks for missing/contradictory citations and observable exclusions; accept alternative wording/test methods where source-equivalent.
- Validate opaque blind-ID mapping and format-neutral representation without discarding material content, review timestamps after registration, two unshared judge sessions and stored contrary findings. Require all seven scoring dimensions, source citations, output IDs and full critical-failure adjudication state.
- Implement automatic **calibration summary** (counts per control, critical miss, false rejection, agreement) from supplied judge outputs; no judge or model calls from this module. Calibration failing prevents qualified comparative scores but still allows preservation/report of unqualified actual agent runs.
- Reuse existing safe interval and usage helpers; distinguish all-attempt costs from success-only costs and never treat unknown pricing as zero.

**Tests/exit gate:** seeded omission and authority defects cannot score as qualified clean, a substantively valid alternative isn't penalized merely for formatting, reviewers cannot read hidden labels via redaction metadata, judge dissent remains unresolved, changed judge rules demand a new version, and an unqualified control set blocks ranking. No AI results asserted by authored controls.

### PR-04 — Execute and retain the bounded AI-only development comparison (P0 if separately authorized; otherwise complete prep + `not_run`)

**Paths:** private experiment root **outside** Git, `evaluation/RUNBOOK_06.md` in repo, sanitized `evaluation/results/ai-development-06-*.json` and immutable digest **only if actually produced**, `tests/test_ai_study_report_06.py` for aggregate redaction and denominator handling.

**Work:**

- Document the actual Codex orchestration/delegation workflow and exact transport tested. Use subagents for research/challenge and separate fresh isolated Codex sessions for planning and judging. Host controls alone dispatch; production Intentline never launches a model. Verify actual host/model/tool/privacy capabilities before invoking.
- Pre-register/capture a three-task, three-arm development study including every assignment. Freeze model/version, reasoning, prompts, tool privileges, contexts, time/call/spending limits, role separation, task order and judge calibration **before** task execution. No surprise retries.
- If authorized and all source/access/judge gates pass, run the real nine planning attempts, blind and score them, then optionally register fresh tasks for the expanded six-to-nine cohort. Record actual elapsed, per-role dispatched model turns/calls, known token categories, cost, denials, timeouts, manual interventions, contamination and confidence limits.
- If not authorized or source isolation/calibration fails, preserve real preparation and write a **dated** sanitized `not_run`, `blocked_budget`, `blocked_host`, `blocked_isolation` or `judge_unqualified` receipt with `0` actual assignments when none registered, and `null` actual usage where unknown. Never claim an executed comparison.
- Keep all raw inputs/outputs/gold/transcripts/permission logs private and immutable; CI must not run these stages. Only source-safe summaries and aggregate statistics may be committed once actually observed.

**Tests/exit gate:** reproduced report from exact immutable inputs matches the frozen algorithm; all registered assignments (including not_run) remain; no fabricated host/model/billing; the result explicitly states **AI-only, development, unverified human independence**. If no real run was possible, engineering qualification may still pass while empirical gate is unmeasured.

### PR-05 — Targeted semantic repairs from *observed* development mistakes (conditional P1)

**Paths:** `skills/intentline-plan/SKILL.md`, `skills/intentline-audit/SKILL.md`, `skills/intentline-slice/SKILL.md` **only when actually warranted**; selected existing code and focused `tests/test_*` where a concrete mechanical defect is reproduced; append `evaluation/FAILURE_LEDGER.md`.

**Work:**

- For each actual development failure, retain the exact source/plan hashes, blinded evidence, why it is source-violating, one counterexample, the smallest change likely to address it and a regression preventing recurrence. Track failures from all arms, including unsupported judging, not just defects attributed to Intentline.
- Prefer minimal skill/doc correction to another stage or schema. If plain Codex performs as well at lower cost, **consider simplifying** instructions rather than adding mandatory audit/planning cycles. Retain equivalent correct alternatives and unaffected requirements.
- Do not modify frozen baseline runs, reference answer, scored outputs, judges or task selection after seeing results. Tune only on explicitly development-exposed cases; any post-fix measurement is a newly declared study.
- **Omit this PR** if there is no observed and defensible Intentline defect. Do not manufacture a fix to complete a roadmap.

**Tests/exit gate:** failing-before/passing-after targeted tests plus full regression, no reduction in legitimate coverage, and a change log explicitly separating a mechanical improvement from unmeasured model-quality benefit.

### PR-06 — Integration, packaging, truthful product/empirical scorecard and release (P0)

**Paths:** `README.md`, `docs/AGENT_GUIDE.md`, `docs/DEVELOPMENT.md`, `docs/SCORECARD_0.6.md`, `docs/IMPLEMENTATION_0.6.md`, `evaluation/README.md`, `evaluation/package_smoke.py`, `.github/workflows/ci.yml`, `pyproject.toml` **only if a separately justified version/build decision is authorized**.

**Work:**

- Explain to a new user exactly what Intentline 0.6 offers: existing three agent skills and deterministic CLI unchanged; separate Codex-only development evidence pathway; how to run and inspect *read-only* results; how the AI-only diagnostic differs from formal independent human validity. No claim of first-user human usability or certified correct planning.
- Package docs, versioned AI-development schema/spec and **public-only authored controls** in wheel and sdist without private packets. Maintain Python 3.11+/stdlib/no runtime model dependency and existing source/result schema, source manifest v1/v2, continuity, audit, adoption, parent/child and native/child exports.
- Qualify on Linux/macOS/Windows × Python 3.11/3.14, exact-head CI, source/wheel builds and fresh installed files, all old 136 tests and focused privacy/judge/denominator controls. Windows secure record storage must continue to fail closed (exit 3); green Windows help/CLI/unit tests do not qualify Windows study storage.
- Preserve original 0.1–0.5 frozen evidence; no rewrite of historical study files or claimed source tag. Separate **engineering release decision** from **AI-development evidence decision** and **formal externally validated efficacy decision**.
- If an actual study ran, publish only sanitized aggregate findings, real measured limitations and case-level source-safe interpretation, never private original solution/reference or transcripts. If it did not run, say `not_run` and make 0.6 an *engineering-prepared experimental* release, not a model-efficacy release. No title/tag implying proved superiority.
- Do not change releases/tags/branch protections/PyPI without actual operator permission. No automatic Proofline live dispatch, child execution, GitHub issue creation or remote modification.

**Tests/exit gate:** all applicable CI and installed package gates pass; traceable source/permission/runtime checks exist for measured claims; zero leaked gold/PII/private paths; explicit current `main`, PR/merge and version state verified at delivery.

## 5. Cross-package acceptance and negative-test matrix

| Test | Pass condition | Fail-closed evidence |
|---|---|---|
| Existing behavior | 0.1–0.5 schema/canonical identities and 136-test baseline retained | A changed historical snapshot/hash or unqualified migration |
| Formal-study distinction | AI packets never become formally `eligible: true` or `human_independent` | Auto-filled actor/independence fields or merged formal denominator |
| Provenance | Historical source commit, exact request/decisions, license and context timestamps preserved | Invented upstream original or later fix leaked into an earlier task |
| Source/gold separation | Planning mounts include only allowlisted original inputs and needed skill tree | Host can read private gold, another run, secrets or judge outputs |
| Subagent integrity | Separate contexts are described as contexts, not separate security domains | Shared filesystem asserted independent isolation |
| Same-arm parity | Identical task bytes/model/reasoning/tool/time grants; recorded skill differences | Extra tools, tokens or preread sources given secretly to one arm |
| Judge controls | Critical seeded failures recognized; valid alternate solutions not critically rejected | False positive control or seeded omission accepted; judging stopped |
| Blindness | No approach label/output history supplied to either judge; mapping remains protected | Branding/metadata reveal arm or answers |
| Bidirectional citation | Every material source promise has plan coverage or finding; all binding plan rows have sources | String-match acceptance alone or gold essay treated as proof |
| False authority | A proposed rule, reported success, closure or stale predecessor never becomes binding | Scope/exception or amendment changes incorrectly accepted |
| Failed assignment accounting | Every predeclared arm attempt and stop retained, with null unknown costs | Vanished failure, rewritten attempt, missing denominator |
| Calibration change | Any changed rubric/judge/control requires new manifest and preserved old run | Post hoc judge repair silently rescoring earlier attempts |
| Read-only evaluation | Validate/assess/report write nothing and invoke no subprocess/network/model | Write, Git, command execution, untrusted code or egress |
| Positive report | Only actual authoritatively captured model runs are called measured | Fixture smoke reported as live inference or efficacy |
| Optional slicing | NO SPLIT and parent preservation honored; no child proof inferred | P2P controller/Proofline child fallback/auto approval |
| Consumer trust | Proofline trust gate stays independent of Intentline planning evidence | New planning result used to declare Proofline runtime safe |
| Release | Six CI cells and wheel/sdist private-material scan, tested on exact heads | Unsupported Windows behavior or undisclosed gate skipped |

## 6. Study methods, measurement and reporting rules

### 6.1 Primary comparisons and interpretation

The primary unit is the **same task** presented to all three arms, not independent repeated paragraphs or duplicated subagents. Report per-task paired differences first. Count exact project/task coverage, severe unsupported additions and material omissions; distinguish independently anchored mechanical observations from two AI critics' judgments. The seven existing adverse rubric dimensions are retained. Record an acceptance plan's *falsifiability* by source-derived expected observable result and a plausible incorrect implementation that the criterion would reject; a planned assertion is not executed proof. An unresolved historical authority question must remain an explicit decision, not an invented settled requirement.

A three-task development diagnostic cannot establish statistical superiority. Six-to-nine tasks remain diagnostic. If attempted model assignments are interrupted/failed, the result must include them; do not selectively report "plans successfully generated" as the population. Missing judge confidence, model cost or human consent is not silently inferred.

### 6.2 What we may credibly conclude from AI-only work

**Allowed:** "Across the three pinned historical development cases attempted, the Intentline arm omitted fewer source-cited obligations under our predeclared mechanical checks and two calibrated AI critics, at an observed token/elapsed overhead"—*only if the actual records support this.*

**Disallowed:** "Independently proven correct", "human-reviewed", "statistically superior", "unbiased AI jury", "authenticated approval", "production verification qualified", "real developer first-use confirmed", "Proofline proved these contracts", or any effectiveness percentage generated solely from authored fixtures.

If an AI critic demonstrably fails its calibration, publish that as a **negative finding about evaluation reliability** and stop the comparative success claim. If no material advantage appears, explicitly discuss simplification or discontinuing costly planning ceremony. If opposite arms win different tasks, say so rather than averaging away important missed promises.

### 6.3 Permission and cost discipline

Subagent work may multiply model calls. Default to **three tasks × three arms** plus a strictly bounded calibration set. Predeclare a small budget separately for (a) research/gold/critique, (b) calibration and blind judging, (c) nine planning attempts, and (d) optional expansion. Stop at a cap; unused budget is not permission to enlarge the experiment. Prefer the same actually available Codex model and reasoning effort across planning arms, with at most two calibrated judge sessions and an optional different-model sensitivity check only if approved. Every native stage's reported tokens count toward cost; cached input is a subset of input, not additional tokens. If provider billing rates/usage aren't available, report token/cost coverage and null USD instead of estimates presented as invoices. Host/container provisioning and human operator overhead, when unknown, remain unknown.

The coordinator is not allowed to run paid models through ambient credentials merely to complete a CI gate or satisfy this document. Ordinary engineering CI, packaging, validation and report generation are strictly zero-inference. A grant to prepare a plan or create a PR is not automatically a grant to contact a model provider, write to another repository or publicize private captures.

### 6.4 Isolation and scientific caveats

Source-grounded controls mitigate but cannot eliminate AI-correlated errors, historical answer exposure in pretrained models, paraphrased gold leakage, upstream documentation conflicts and unconscious grader preferences. An AI-only study cannot satisfy Intentline's original human-independent eligibility rules. A separate environment enforces an *access boundary*, not impartiality or independent reasoning. Preserve transparency on same-model dependence and source ambiguities, and never promote all-AI adjudication to objectively authenticated ground truth.

Models may have prior knowledge of the chosen public repositories. Avoid prompting with future solution pages; disclose public-knowledge contamination. Treat AI-authored upstream issues as evidence of real historical text where appropriate, but label them rather than citing them as independently human-authored tasks. A source license may not automatically cover issue discussion content; review reuse before publication and keep uncertain text private.

## 7. Release decisions and implementation handoff requirements

Before concluding, provide **three independent status decisions**:

1. **Engineering status:** exactly which modules, tests, docs, CI cells, wheel/sdist checks and source/schema compatibilities were completed, and what remains broken.
2. **AI-development study status:** number of selected candidates, source-qualified tasks, calibrated judges, real arm attempts, scored assignments, cost known/unknown, actual findings and contamination/limitations. If blocked, precisely which source/host/budget gates remain and the fully prepared private package locations.
3. **External formal evidence status:** still **not independently human-reviewed**, unless future actual externally authenticated records are supplied in a separate protocol. Do not "graduate" 0.6 work into formal 0.5 pilot records.

The final handoff must include:

- Current repository `main` SHA, created PR URLs and actual merge status (or PR-ready local commits if effects not authorized), exact test commands/results and CI URLs. Do not invent a PR.
- Private package directory and digest manifest available to the authorized operator **without exposing gold in Git**; list each retained source/task/artifact and human-independent status qualification in the private inventory, redacted in public reports.
- All real study registration/calibration/run/scoring/host-capability receipts, even for failed/partial attempts. Distinguish recorded model outputs from authored fixtures and operator declarations.
- A short, source-grounded table of what Intentline got right or wrong compared with ordinary Codex and P2P, **only if judged outputs exist**; otherwise a genuine `not_run` conclusion.
- Preparatory and all-attempt resource usage including actual charged cost if supplied, with unknowns left null. Report the judged control-set limitations, cross-judge disagreements, contamination and any adversarial counterexamples.
- Exact remaining blockers and next allowed actions; no request to "wait" for future results and no claim of ongoing background study execution.

**Definition of success for 0.6:** We can honestly reproduce and inspect AI-assisted acceptance-planning observations on real source-grounded tasks—or identify exactly why the first such comparison was blocked—*without weakening Intentline's correctness/authority boundaries, inventing human independence, building another evaluation framework, or treating Codex subagent isolation as more than it actually is*. A demonstrated, trustworthy directional diagnostic is the desired outcome; a mechanically clean but unrun suite is engineering preparation only.
