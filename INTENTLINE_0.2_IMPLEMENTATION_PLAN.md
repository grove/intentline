# Intentline 0.2 — Reliable, Effortless Acceptance Planning

**Implementation-ready specification | 12 October 2026**  
**Repository:** https://github.com/grove/intentline  
**Target:** Intentline `0.2.0` (engineering release with explicitly qualified or unmeasured usefulness)  
**Verified `main` baseline:** `adc404e97dc6a6e37e63e02ccee0cd7409cc38bc` — merged 0.1 PR #7 (2026-10-12 08:48:37 UTC)  
**Upstream references at planning time:** Lore `55ee9830e38fe869669376a089c9fbd4dddca43c`; Proofline `c4d28e4e743adbb261552323e694946f1360a129`; Promise to Proof `17f3deb982a8224f71b12bda74be6b24d86571e4`. Recheck their heads before compatibility work.

## 0. Instructions for the coding agent

**Implement the plan; do not return another plan.** Begin by checking the actual current `main` and reading the source paths listed below. If the head has advanced, adapt to the implementation without overwriting newer work. Deliver PR-sized changes in dependency order. Fix ordinary defects, make reasonable choices, and finish all feasible engineering work without repeatedly asking the operator for decisions. Run the checks available in your environment. Create reviewable PRs; merge only when the operator has authorized merging and the repository's required checks and protections permit it. Do not force-push over others' work or rewrite 0.1 history.

**Do not invent evidence.** A Python test, a mock agent, a manufactured review, a semantic fixture, and a real coding-agent or human study are different things. No authenticated independent reviews, live model quality, user adoption, provider cost, or downstream Proofline acceptance may be claimed without actual corresponding records. Never use ambient model credentials or trigger paid inference merely because credentials happen to exist. Keep external model execution separately authorized, bounded and auditable; do not quietly lower the host's native isolation, permissions or egress restrictions.

**Product boundary:** Intentline authors and manages candidate-independent acceptance agreements. It does **not** edit implementation code, run proof, deliver a change, authenticate user approval, operate a general agent controller, or become a project knowledge database. Lore is optional project intelligence; Proofline is an optional downstream delivery/verification consumer; P2P is a reference implementation and optional benchmark arm. None is an Intentline runtime dependency.

**Implementation style:** Extend the existing **Python 3.11+ standard-library-only** code, records, skills and CLI. Preserve the 0.1 JSON acceptance contract and CLI behavior unless there is a specifically justified, versioned migration. Reuse source captures and immutable records rather than adding a second source-of-truth. No mandatory model-provider SDK, HTTP client, daemon, MCP server, database, agent orchestration framework, or new package dependency in 0.2. Keep optional adapters and evaluation orchestration out of the normal CLI code paths.

### Read these before editing

- Intentline: `README.md`, `docs/CONTRACT.md`, `docs/CLI.md`, `docs/INTEGRATIONS.md`, `docs/TRUST_AND_AUTHORITY.md`, `docs/AGENT_GUIDE.md`, `docs/SCORECARD_0.1.md`, `skills/intentline-plan/SKILL.md`, `skills/intentline-audit/SKILL.md`.
- Intentline implementation: `intentline/cli.py`, `sources.py`, `contracts.py`, `records.py`, `audits.py`, `adoption.py`, `export.py`, `paths.py`, `render.py`; `schema/*.json`; `tests/*`; `.github/workflows/ci.yml`.
- Intentline 0.1 original specification: `INTENTLINE_0.1_IMPLEMENTATION_PLAN.md` (historical, not to be rewritten).
- P2P: `skills/productivity/plan-acceptance/SKILL.md`, `skills/productivity/audit-acceptance/SKILL.md`, and the *relevant* sections of `docs/acceptance-contract-protocol.md`. Borrow minimal proven rules, not the controller, work tree, or entire giant protocol. Maintain Apache-2.0 notices for verbatim/adapted material.
- Proofline: `README.md`, `SKILL.md`, `proofline.py`, `docs/S2-CONTRACT-INPUT.md`, and its actual `tests/test_contract_input.py` / direct-input tests. Revalidate before changing adapters.
- Lore: `docs/V09.md`, `docs/SHARED_INTELLIGENCE.md`, and the schema-1 bootstrap / schema-5 context descriptions. Do not confuse a report with primary documentary authority.

## 1. Current verified state: what 0.1 already does

All eight initial PRs are merged. The latest verified main-branch CI at planning time passed: https://github.com/grove/intentline/actions/runs/38225873497. The 0.1 scorecard records **44 offline tests** on Python 3.11/3.12/3.14 locally, Linux/macOS/Windows CI on 3.11/3.14, and packaged wheel/source distribution smoke tests. Windows secure record storage **intentionally fails closed**; its green CI does not mean Windows recording is supported.

Existing functioning commands: `prepare`, `propose`, `check`, `render`, `status`, `audit-record`, `adopt`, `export`. Current acceptance `schema/acceptance-v1.schema.json` is authoritative JSON with source-bound `R1...` criteria, original exact-line excerpts, boundaries, public seams, independent expected oracles, planned evidence, explicit gaps/decisions, revisions and change notes. `intentline-plan` and `intentline-audit` are agent-facing skills; the deterministic CLI does **not** synthesize requirements. Immutable captures and audit/adoption assertions are SHA-256-bound; a hash authenticates bytes, not authors, independence or approval. Current `export --format proofline-direct` creates original `source.md` and advisory `brief.md` accepted by a pinned *parser* test, **not** an actually qualified delivery or approved contract.

The 14 authored good/bad planning examples are regression fixtures, not a real-model planning study. There are **zero confirmed human adoptions, zero authenticated independent audits, and no live-model usefulness comparison** in the 0.1 release evidence. No GitHub release has been published at planning time.

**Do not rebuild these mechanisms.** 0.2 should make them convenient, assess semantic quality with genuine work, correct concrete weaknesses, and qualify honest downstream handoffs.

## 2. Product hypothesis and outcomes

**Headline hypothesis:** A developer or existing coding agent can provide Intentline one development request and receive a concise, complete, source-grounded and independently falsifiable acceptance plan with less interaction overhead, while preserving project constraints and without increasing invented requirements.

### User-visible outcomes

1. **Single-request planning:** In a supported agent host, a single ordinary request is sufficient for the *agent* to capture the original input, select a few relevant permitted project documents, prepare the work item, author and check a draft, and return a usable plan. No manual JSON editing, hand-entered hashes, or series of CLI commands for the normal agent-assisted path. Manual JSON/CLI remains a supported power-user path.
2. **Better-quality contracts:** Required behavior is not silently omitted or changed; unnecessary new behavior is not introduced; accepted project decisions are not confused with proposals/reports; scoped exceptions survive; the expected oracles do not merely mirror candidate behavior; material uncertainty is identified without inventing blockers.
3. **Natural acceptance boundary:** The normal deliverable is a **draft**, never automatically an approved or proven agreement. An optional independent audit and externally authorized adoption remain separate actions, with accurate identity and trust labels.
4. **Optional downstream use:** The direct Proofline handoff preserves the original promise and material constraints in actual supported workflows. No approved-contract shortcut or synthetic success.
5. **Optional Lore enrichment:** Structured project knowledge can improve a plan when explicitly supplied, but every command and skill still works without Lore, Proofline or P2P installed.

### Provisional quantitative goals, not claims

For an externally reviewed 6–9-task *diagnostic pilot* across at least three real projects, aim for **zero material source-promise omissions**, **zero invented binding product requirements**, and **credible observation or explicitly stated evidence gap for each material requirement** in the independently reviewed Intentline outputs. Track exceptions rather than hiding them. Aim for one normal user instruction and no manually authored JSON in supported agent-host trials. Compare all-in effort and cost with controls rather than assuming a percentage gain. These are targets for diagnosing gaps, not statistical efficacy conclusions or pretexts to adjust test labels.

An unrun or incomplete study does not block well-tested engineering improvements. It *does* prohibit claims that 0.2 demonstrably outperforms conventional planning.

## 3. Non-negotiable compatibility and trust boundaries

- Preserve `intentline.result` schema 1 (`--json`, exit 0/2/3), `intentline.acceptance` schema 1, canonical bytes and hashes, 0.1 revision lineage and stable requirement IDs, source-manifest semantics, `DRAFT` / `STRUCTURALLY_VALID` / `READY_FOR_ADOPTION` / `ADOPTED_ASSERTED` / `BLOCKED` / `STALE` qualifications, and the existing direct Proofline export semantics.
- Preserve exact original request bytes; if the host cannot retrieve the literal original request, tell the user and require a real original-source file or explicit disclosure. Never silently substitute a paraphrase. Captured context is separately classified and may not grant authority. A context snapshot/Markdown quote is not proof of a runtime property.
- Only original user/project authority can adopt material outcomes. A human-readable `approved` string, model response, issue label, agent-asserted actor name, independent-audit assertion or digest **does not authenticate approval**. No automatic `intentline adopt` in the normal planning skill.
- Preserve accepted/proposed/rejected/reported/superseded distinctions, scoped exceptions, conflicting evidence, missing support, and decision relevance. Derived insights do not automatically become adopted requirements. Do not let a Lore status or P2P contract label override underlying source authority.
- Missing evidence of how to check a settled requirement is an **evidence gap**, not automatically a product-decision blocker. A genuine unresolved choice affecting promised outcome or authority is an **open decision** and blocks adoption/handoff as it does in 0.1. Keep independent unaffected findings useful.
- Normal read-only CLI commands must not write records, bytecode, caches, credentials, Git files, or call subprocess/network/model APIs; document `python -B` for strict read-only runs. Mutations require explicit CLI actions; retain POSIX no-follow/locks/fsync semantics, preserve unsafe Windows refusal, and do not broaden file access.
- No CI, fixture replay, default plan command or install may cause real paid inference or GitHub writes. Evaluation operators supply real execution credentials and budgets separately, outside source/control fixtures.
- Maintain deterministic offline usability with Python 3.11+ and no required external programs or services. Existing semantic agent instructions may use their *host's* tools under that host's grants; Intentline CLI itself does not spawn agents.

## 4. Intended user experience and interface

### 4.1 Normal agent-assisted flow

A developer asks a capable agent:

> Use Intentline to plan acceptance for: “Add configurable payment retries while preserving existing behavior unless explicitly changed.”

The agent invokes the installed `intentline-plan` skill **once**, not a series of user-facing setup steps. It accesses the verbatim request or operator-supplied source file, reads relevant permitted project files if necessary, runs existing deterministic CLI actions, and returns the short plan, the important decision/gap (if any), and an exact saved work-item reference. It does **not** automatically implement, verify, approve, or send anything to Proofline.

Expected ordinary result structure (human-facing summary, not a new contract schema):

```text
Acceptance plan: Configure payment retries
- R1  Explicit configuration changes the documented retry behavior.
- R2  Omitted configuration preserves the existing behavior.
- R3  Applicable accepted retry/idempotency constraints and scoped exceptions hold.
- R4  Negative/limit behavior has an independently observable expected result.
Open decisions: [actual unresolved choice, or none]
Evidence gaps: [actual unavailable observation, or none]
Saved draft: .intentline/work/<work-item>  [exact contract/source digests]
Next action: [one useful supported action]
Status: DRAFT (not approved, executed or proven)
```

Only include requirements genuinely supported by the request or applicable context; the example above is illustrative. Do not manufacture specific limits, APIs or policy changes from the prose.

**Host portability:** Skill entry/installation differs by Codex, Claude Code and other hosts. Do not claim a literal `/intentline-plan` slash command works in every host. Implement a copy-pastable neutral instruction and verify an installed skill works in at least one actually available supported host when authorized. Fall back to existing manual CLI on unsupported hosts. No new network-connected `intentline plan` executable is required.

### 4.2 Existing deterministic/manual path stays unchanged

```bash
python -B -m intentline prepare --source request.md --context docs/policy.md \
  --root /absolute/project --out .intentline/work/task --json
# Agent/human authors a schema-1 draft from frozen sources, then:
python -B -m intentline propose --work .intentline/work/task --draft draft.json --json
python -B -m intentline check --work .intentline/work/task --json
python -B -m intentline render --work .intentline/work/task
python -B -m intentline status --work .intentline/work/task --json
```

The standard skill should orchestrate these **within the existing host**. There must be no second authoritative representation, auto-approval, hidden model call from the CLI, or automatic modification of `.gitignore`/agent instructions. If a project cannot safely ignore private captures, use an operator-selected private output root outside the repository; avoid silently writing sensitive captures into tracked paths.

## 5. Work packages and dependencies

| PR | Priority | Work package | Main result | Dependencies |
|---|---|---|---|---|
| **01** | P0 | Frozen baseline + meaningful planning-evaluation protocol | Real-task eligibility, blinded scoring, fair arms, offline receipts | None |
| **02** | P0 | One-request agent-native planning | A practical, no-manual-JSON normal path in an existing agent host | 01 for baseline evidence |
| **03** | P0 | Failure-driven semantic planning and audit improvements | Repair actual missed promises, unjustified scope and weak evidence paths | 01/02; only tune on development material |
| **04** | P0 | Qualify Proofline direct handoff | Source/brief identity and actual optional local-delivery verification | 02; coordinate with Proofline support boundary |
| **05** | P1 | Optional read-only Lore context adapter | Correctly qualified source-linked intelligence without peer dependency | 02/03; may run in parallel with 04 |
| **06** | P0 | Integration, documentation, CI and release scorecard | Completed 0.2 engineering release and truthful outcomes | All P0; include 05 if finished |

Deliver separate PRs where possible. An extra small regression/compatibility PR is acceptable if an actual defect needs isolation. If genuine human/model work remains unavailable, record `not_run` and complete the independent engineering packages rather than inventing substitutes.

### PR-01 — Freeze 0.1 baseline and establish honest usefulness evaluation (P0)

**Purpose:** Before changing instructions, make it possible to tell whether they improve acceptance planning rather than merely produce more words or meet a schema.

**Implementation locations:** add `evaluation/README.md`, `evaluation/planning_02.py` (or a comparably small standard-library inspection/scoring CLI), `evaluation/rubric_02.md`, `evaluation/cases/` with *development* manifests only, `evaluation/results/` with an initial `not_run` receipt; expand `tests/` for offline harness mechanics. Preserve 0.1 examples/tests/scorecard unchanged.

**Tasks:**

1. Freeze the existing 0.1 CLI/schema/renderer/skill behavior using exact, reusable offline snapshots (capture hashes, representative positive/negative outputs, existing 44-test expectation and platform limits). Do not preserve wall-clock times as byte-equality requirements.
2. Specify a **real-project** pilot: preferably **9 tasks from ≥3 distinct pinned repositories** (minimum 6/3 to begin). Each must depend on actual pre-existing project evidence (accepted vs proposal, scoped exception, historical rule, negative case, regression/invariant, or a real ambiguity). Pin full source commit, license, original request, the *same original documents* available to every arm, selected scope and allowed task-specific context. Distinguish historical source truth from a checker author's desired answer. Private gold/score records must not enter any arm's model context.
3. Publish *eligibility and review requirements*: task author and independent checker/expected-outcome author are distinct wherever feasible; two additional independent reviewers review the task, key constraints and reference outcome with recorded timestamps, conflicts and source-citation corrections. If these people or authenticated records are unavailable, label the slot ineligible/not_run; do not fabricate identities or count public Intentline fixtures as reviewed real tasks.
4. Predeclare three comparable arms: **ordinary agent planning without Intentline**, **same agent with Intentline 0.2 skill**, and **P2P `/plan-acceptance` skill alone** (not P2P delivery controller). Keep model/version/reasoning limits, project sources, task presentation, host tool capabilities and time budgets as matched as the systems permit. Record unavoidable differences and attribute preparation/installation costs. P2P need not be installed to use Intentline; it is an optional benchmark arm.
5. Score *semantic quality*, not formatting conformity. Rubric dimensions: complete material promise coverage; applicable project-constraint preservation; unjustified new requirements/exclusions; correct decision/scope/lifecycle; credible falsifiable oracle/negative cases; identification of material missing evidence; unnecessary blocking; agent/user actions required; elapsed wall time, model calls and reported tokens/cost when available. Treat unknown provider usage/billing as `null`, not zero. Have reviewers compare blinded substantive outputs, with IDs mapped to original sources, rather than rewarding the Intentline/P2P-native schema.
6. Provide deterministic `validate`, `assess` and `report` operations on **already produced external results**. These verify manifest/snapshot bindings, assignment completeness (including failed/refused/timeout/not_run), score coverage, reviewer conflicts, output integrity and study provenance. They never invoke paid models, run repo tests, authenticate an actor, or upgrade a declared independent review to verified independence. Add bound private output paths and sanitized public aggregates; protect private original sources/answers and avoid committing prompts with secrets.
7. Record an immutable initial `not_run` evaluation receipt and exact blockers. If live models and independently reviewed tasks are available with explicit spending authorization, run the pilot; otherwise preserve the readiness state and continue engineering. Register held-out tasks (separately) before tuning to avoid test leakage.

**Required offline controls:** missing task/source pins; reused/development tasks disguised as real; leaked private gold; same task/checker/reviewer identity; mismatched source/context across arms; missing, failed or timed-out assignment; absent token/billing fields; changed score file/subject digest; unblinded scoring records; interval math and denominator correctness; no subprocess/network invocation during read-only assessment.

**Exit:** documented evaluator/rubric, reproducible baseline, initial truthful real-run status, offline mechanical tests. A synthetic fixture may check scorer mechanics but **may not populate empirical success figures**.

### PR-02 — Make planning work from one ordinary request (P0)

**Purpose:** Turn the current eight-step skill instructions into a coherent, practical existing-agent workflow. This is a *skill UX improvement*, not a new hosted model runtime.

**Primary files:** `skills/intentline-plan/SKILL.md`, `docs/AGENT_GUIDE.md`, `docs/TUTORIAL.md`, `README.md`, possibly a small deterministic helper in `intentline/` only when it removes a real friction point; corresponding `tests/test_skills.py` / CLI integration tests.

**Tasks:**

1. Rewrite the skill to start with the concrete output: preserve the request; select only necessary accessible context; author the minimal complete schema-1 plan; validate; correct structural errors; render; return a concise decision-ready agreement. Keep advanced sections linkable instead of forcing every task through a long ritual.
2. Prefer an **explicit source file** for reproducible requests. When invoked from chat, capture the exact current message text only if the host makes the original bytes available. If not, label non-verbatim capture and ask for the exact source only when source fidelity materially requires it. Do not present a paraphrase as an authenticated user request.
3. Choose a fresh private output path or an existing matching fresh work item; ensure it is excluded from Git commits. Do not automatically edit project `.gitignore`, `AGENTS.md` or `CLAUDE.md`. Respect existing file/no-follow permission checks. If no safe output can be selected, provide the useful draft in the response and name the incomplete persistence boundary honestly.
4. Handle normal small requests with **one semantic planning pass** and **zero mandatory separate model audits**. Run deterministic validation/identity checks; repair only actual validation failures. Reuse fresh unchanged drafts. Escalate one material outcome/authority ambiguity, otherwise complete the supported plan with clearly limited scope. No endless follow-up questions or blanket refusal because a future test suite does not yet exist.
5. Include precisely the plan's `R` obligations, decisive scope/boundaries, important evidence gaps, meaningful unresolved decisions, one next action, exact saved location/identity and **DRAFT** status. Preserve richer evidence in JSON/Markdown for drill-down. Do not invent claims that an audit, test, approval or model review was performed.
6. Give explicit, tested installed-skill guidance for at least the actually qualified host. Give host-neutral copy/paste instructions for other command-capable agents. Existing installed `share/intentline/` files and relative references must resolve from wheel/sdist installations (not only repository-local paths). Document manual CLI as fallback.

**Tests / acceptance:** Full process from original `request.md` → `prepare` → agent-generated or fixture-authorized draft → `propose/check/render` without user manual JSON; simple exact-lookup/one-criterion task requires no needless extra stages; accepted/proposed historical task includes correct warning/scope; non-verbatim chat capture never claims exact preservation; structural failure corrected without an extra approval; rerun reuses revision when unchanged; absent model or uninstalled skill retains manual usability. Offline fixture automation tests mechanics; real host smoke is recorded separately, not simulated as a live agent.

**Exit:** A real user can ask an existing supported coding agent once for an acceptance plan and receive the draft, without being expected to know the CLI's internal stages.

### PR-03 — Fix semantic failures, not hypothetical architecture (P0)

**Purpose:** Target the highest-impact planning and auditing weaknesses observed in the evaluation development set and one-request workflow. Never tune against registered held-out source-gold.

**Files:** `skills/intentline-plan/SKILL.md`, `skills/intentline-audit/SKILL.md`, targeted `examples/` and `tests/`; small `intentline/contracts.py`/`audits.py` changes **only** when a reproducible *mechanical* defect requires them. Preserve schema 1 unless strong backward-compatible reasoning is documented.

**Tasks:**

1. Create a failure ledger linked to exact task/source/plan revision and reviewer finding. Classify: omitted source promise, incorrect authority, scoped exception lost, scope inflation, weak/tautological oracle, unjustified blocker, wrong revision/freshness, excessive cost/ceremony, or ambiguous input. Keep adverse examples and cost data; do not rewrite failed baseline outputs.
2. For each change, include a **before** failing authored/independently checked semantic probe, a minimal skill or mechanical correction, and an **after** probe. Be explicit whether the check is fixture-only, independent human-reviewed, or actual real-model output.
3. Reuse P2P's valuable rules selectively: *smallest complete contract*, independently falsifiable outcome, specification envelope (completeness vs scope), source-linked criteria, plausible negative boundaries, independent expected oracle, material blocker only, evidence gap distinct from outcome question. Avoid transplanting P2P's planning controller, approval checkpoint machinery, child hierarchy, repeated stage agents and broad universal checklists.
4. Audit skill examines the **same frozen source and exact draft**, checks both omissions and unsupported additions, distinguishes optional advice from binding requirements, and produces findings without editing, approving or proving. Report `self_check` / `unverified_independence` unless the external host has actual independently established identity and isolation. Do not add a mandatory second model call to every normal planning request.
5. Preserve every real failure and every uncompleted evaluation arm; do not tune criteria or source-gold retroactively to make a modified skill pass. Stop when the material problem is corrected; do not request further investigation without an expected decision benefit.

**Targeted negatives:** accepted ADR vs later unapproved RFC; narrow staging-only exception; rejected design reintroduced as mandatory; reported runtime success asserted as fact; an oracle copied from the buggy implementation; one requirement split into many overlapping checklist rows; proposed test commands mistaken for execution; absence of test harness treated as fatal product ambiguity; user explicitly excluded a feature yet planner adds it; changed source while old adoption appears current; embedded malicious instructions in source text.

**Exit:** Reproducible, evidence-linked corrections and an updated failure ledger. No bare assertion that the new prompt is "better" because it passes a regex test.

### PR-04 — Qualify an actual Proofline direct handoff (P0)

**Purpose:** Go beyond the 0.1 pinned parser test without making Proofline a dependency or weakening its approval / host protections.

**Files:** `intentline/export.py` only if an actual bug is demonstrated; `docs/INTEGRATIONS.md`; new offline handoff contract tests in `tests/`; private/offline qualification tooling under `evaluation/`, not the normal CLI.

**Current real boundary:** `intentline export --format proofline-direct` emits exact `source.md`, advisory `brief.md`, contract/captures/hash manifest. Proofline's direct delivery consumes `--source`/`--brief`; its separately authorized `--contract` path currently understands a specifically qualified P2P eight-column Markdown contract and verified approval inputs. **Do not relabel an Intentline draft or `ADOPTED_ASSERTED` as a qualified Proofline approved contract.**

**Tasks:**

1. Freeze a complete handoff compatibility contract: exact original request bytes, unique stable `R` IDs, no loss of material accepted constraints/scope, explicit unknowns, complete source captures/manifests, and output identity unchanged between export and Proofline launch. A shortened `brief.md` is an index only; original `source.md` remains authoritative. A source conflict/missing required context must not be hidden by successful parsing.
2. Verify on a **clean tracked Git checkout** of the sample product (with all relevant source files available to the downstream consumer), honoring Proofline's supported path/no-symlink/host constraints. Test positive and negative direct input admission **offline** without paid inference: tampered source/brief/manifest, missing context, wrong IDs, mismatched checkout, stale acceptance, unsupported parent/prerequisite source, and advisory output mislabeled as approved.
3. Provide an **operator-run** end-to-end smoke recipe and evidence recorder: export → independent authorized Proofline direct `deliver` → `status` of frozen candidate → reviewer/prover outcome, original-source/constraint coverage and available usage. Use only an actually supported qualified host/model (the inspected Proofline docs identify macOS, Python 3.11+, Git, Codex CLI 0.162.1; recheck before execution). Require explicit operator spending authorization, real authentication, supported native isolation and checked source identity. Never run this in ordinary CI.
4. If external real execution is unavailable, record an exact `blocked_external/not_run` receipt and finish the offline adapter tests. Never call parser compatibility a live Proofline proof or use a fake worker as an independent reviewer.
5. Evaluate a **native approved-contract handoff** as a future interoperability RFC, **not** as a 0.2 release requirement. That would need Proofline to explicitly recognize Intentline's authority/identity schema, honor the original promise, and qualify live positive/negative controls. Do not create a misleading P2P-shaped export to evade Proofline's current adapter policy.

**Exit:** Complete, tested direct handoff and an honest live qualification record if permitted, otherwise reproducible external blockers. No added Proofline runtime dependency.

### PR-05 — Optional, read-only Lore intelligence input (P1)

**Purpose:** Let Intentline benefit from Lore's understanding of decisions, exceptions and provenance without becoming Lore-dependent or accidentally turning a derived model answer into project policy.

**Approach:** Accept an **explicitly supplied** Lore report (file or captured bytes) into the normal bounded, source-preserving work-item context. Do not launch `lore init`, `lore update`, `lore context`, network inference or checkout inspection automatically. No direct access to Lore's database, keys or model cache. A small *format-aware interpretation* is preferable to a full client library.

**Possible implementation location:** `intentline/lore_adapter.py` and `docs/INTEGRATIONS.md`, or simply a hardened skill/documented import if the existing `--context` mechanism is enough. **Choose the smaller option after comparing real need.** If a new CLI flag is genuinely warranted, make it opt-in and additive (for example `prepare --lore-report REPORT.json`); do not break existing `--context` or source-manifest schema 1.

**Rules:**

- Recognize only explicitly supported Lore bootstrap schema 1 and initialized context schema 5 as documented at the pinned compatibility revision. Invalid/unrecognized versions and incomplete reports must return a clear limitation or be treated as ordinary untrusted source data, not as authoritative facts.
- Preserve original documentary citations, project/registry identity, lifecycle, scope, current-vs-historical support, source relationships, conflicts, omission counts, capability grants, inference/fallback mode, and static-inspection-vs-execution distinctions. A `fast_fallback` answer is not fresh model judgment; inspected code is not runtime proof; an accepted ADR still needs its own supporting source.
- Generate **candidate context leads**, never auto-accepted criteria or approval. Each project constraint entering an Intentline contract must cite a captured, applicable original source or be explicitly qualified as a necessary inference. If a referenced original excerpt is unavailable, include an evidence gap/lead, not a fabricated exact quote or a silent promotion of Lore advice.
- With no Lore installed, absent report, unavailable inference, stale report, permission denial, or zero relevant result, continue standard planning using selected original files and label what context was missing. No repeated permission prompts or hidden hosted requests.
- Keep report size/file count bounded and no-follow; do not exfiltrate source excerpts. Avoid self-referential Lore context, generated wiki material automatically converted into authority, and new long-lived planning knowledge storage.

**Tests:** accepted vs proposed; narrow supersession; A→B→A source reversion; omitted critical relationship; deleted documentary source; stale registry; schema 1 bootstrap; schema 5 fallback; static inspection; missing evidence witness; unsupported schema; no Lore installed. All offline, no model calls, unchanged source bytes.

**Exit:** Optional enrichment is correctly qualified and does not degrade the no-Lore path. If real evaluation offers no demonstrated benefit, include the safe adapter as experimental or defer it with a concise evidence-backed reason; never hold P0 release engineering hostage.

### PR-06 — Integration, user documentation, version and truthful release (P0)

**Purpose:** Ensure the independently useful product remains simple, installable and honest.

**Files:** `README.md`, `docs/TUTORIAL.md`, `docs/AGENT_GUIDE.md`, `docs/INTEGRATIONS.md`, `docs/DEVELOPMENT.md`, `docs/SCORECARD_0.2.md`, `pyproject.toml`, `.github/workflows/ci.yml`, regression tests and packaging manifests.

**Tasks:**

1. Document the shortest installed agent-assisted path and a no-agent manual path. Explain draft vs audit vs asserted adoption vs independently verified delivery with one concrete example. Show how an agent may offer a useful partial acceptance plan without manufacturing missing decisions or pestering the user for routine details.
2. Version the package as `0.2.0` only after required engineering gates pass; document all material command/contract changes (prefer none). Update proper Apache attribution for adapted P2P material. Package and install skills and their referenced docs on supported Python 3.11+ without a checkout.
3. Run full existing + new offline tests, lint/type checks if already available (do not introduce heavy mandatory developer tooling solely for ceremony), wheel/sdist and freshly installed command/skill resolution smoke tests. Require Linux/macOS/Windows × Python 3.11/3.14 CI at **each final PR head**. Windows recording must remain clearly unsupported/exit 3 unless independently qualified; a green Windows help/parser run is not a record-storage pass.
4. Verify identity/privacy/side-effect controls under interruption, stale input and hostile source content; all read-only CLI paths (including evaluator report commands) remain zero inference, zero network and zero source writes. Confirm no protected private pilot inputs or answer keys are checked into the repo.
5. Publish the **measured/unmeasured 0.2 scorecard**: exact commits and CI runs, unit/fixture counts, real eligible pilot/arm attempts, reviewer provenance, pass/fail/refusal/interruption counts, planning score table where externally reviewed, total effort and known/unknown costs, Proofline handoff status, Lore adapter status and native platform qualifications. Record adverse runs, not just the last green run.
6. Make an explicit release decision: engineering `0.2.0` may ship with usefulness still labeled **experimental/unmeasured** if all deterministic safety/compatibility/release checks pass. Do **not** advertise independently proven effectiveness until the live reviewed pilot and then a separately registered holdout support that claim. No automatic publishing/tagging/merge without authorization.

**Exit:** 0.2 is independently installable and useful as an agent-native planning tool, P0 regressions are green, and every external evidence limitation remains visible.

## 6. Acceptance and negative-test matrix (cross-PR)

| Scenario | Required expected behavior |
|---|---|
| Simple complete request | One request → one concise plan; no required separate model audit, manual JSON or redundant setup |
| Original user wording lost by host | No false verbatim assertion; explicit limitation or real source-file capture |
| Accepted ADR plus later proposal | Only the applicable accepted requirement binds; proposal is historical/advisory unless actual authority establishes change |
| Scoped exception | Retain exception's exact scope and parent rule in the same relevant plan context |
| Rejected approach or reported success | Neither becomes adopted requirement or independently verified behavior |
| Material ambiguous outcome | Specific `open_decisions` and blocked adoption; independently decidable criteria remain useful |
| No credible runnable harness | Explicit evidence gap; never invent executed proof or convert into unrelated product-blocking question |
| False extra requirement | Report and correct scope expansion, even when the format is mechanically valid |
| Weak/tautological oracle | Audit names what cannot actually falsify the criterion and smallest better check |
| Unchanged draft rerun | Reuse current source/contract identity and revision; do not needlessly invoke extra agents |
| Changed source/contract | Old adoption is stale, revisions/IDs map, no silent use of prior audit or downstream approval |
| Audited by same actor | `self_check` / `unverified_independence`, never authenticated independent audit |
| Export to Proofline | Exact original source, stable IDs, material constraints preserved; stays advisory direct input |
| Misuse of Proofline `--contract` | Reject or explicitly report unsupported authority/format; no P2P-approved disguise |
| Missing/stale Lore report | No-Lore path works; no source promotion and no model/spending side effect |
| Truncated Lore scope or conflicting source | Omission/conflict remains visible, not compressed into confident binding acceptance |
| Untrusted prompt injection in documentation | Text is data; cannot authorize tool use, policy change, approval, egress or writes |
| Tamper/TOCTOU/symlink/FIFO/interrupt | Refuse inconsistent/unsafe identity without overwriting immutable records |
| Windows unsupported storage | Explicit exit 3 until qualified; no hidden weaker fallback |
| Unavailable real study input/host | `not_run` / `blocked_external` with exact missing prerequisite, never an efficacy pass |

## 7. Evaluation protocol and interpretation

### 7.1 What counts as a genuine pilot

Use genuinely sourced engineering requests where existing source history matters. Each task has: original request, historical repository+full commit, relevant license, selected sources available to *all* arms, authorized host grants, immutable contract/scorer revision, reference interpretation with independently reviewed source citations, and private reviewer/checker captures. Different named actors and hash-shaped fields are **not** proof of independence. Reviewer/authentication limits must be reported.

Use the same work-item presentation and knowledge opportunity for all comparison arms. Baseline agents may inspect/read the same original files; do not unfairly starve them of relevant documents. Avoid leaking answers via task filenames, prior examples, repository agent instructions, caches or pre-solved patches. Source/prompt/model changes invalidate comparability unless separately attributed.

Register the development pilot and untouched holdout separately *before* reading outcomes. P2P arm uses only its acceptance planning skill, not its paid implementation/review/proof machinery. Intentline arm costs include selection/agent drafting/CLI calls/audits actually used; do not count only the successful final render. Ordinary agent arm must be asked to produce a comparable acceptance plan, not intentionally denied instructions to plan. Audit and scoring must use the original request and independent project sources rather than trusting either plan's self-description.

### 7.2 Metrics and honest statuses

**Primary:** independently judged material-omission count and material-invented-obligation count per request, plus whether the entire planned result preserves binding project constraints. **Secondary:** falsifiable check quality, unnecessary blockers, effort to reach a usable draft, failed/refused/timeout rate, reviewer effort, model attempts/tokens, and observed or externally billed cost when known. Capture *all attempted* assignments and total preparation/initialization overhead. Separate semantic disagreements and environment failures; include both in the denominator. Retain raw per-assignment records privately and publish only safe, sanitized aggregates.

A 6–9-task pilot can reveal failure types and implementation priorities; it **cannot establish broad statistical superiority**. If sufficient paired held-out data later exists, preregister estimates and uncertainty intervals; report exact numerator/denominator, interval method and model/cost uncertainty. Never invent elapsed time, model identity or billed amounts.

### 7.3 If external prerequisites are blocked

No authorized hosted/local model, independent participants, authenticated isolation, or operator spending approval? Run all deterministic engineering validations, keep the study in `not_run` state, and explain the precise blocker. **Do not** substitute the existing 14 public fixtures or a fake Codex executable for real-agent quality evidence. Continue PR-02/03/04/05 and the engineering scorecard.

## 8. Safety, cost and integration constraints

- Planning is primarily a **skill running in the caller's existing agent**. Do not add a model SDK or independently instantiated agent merely to run `intentline plan`; do not multiply model passes unless independent pilot failures justify them.
- Semantic audit is optional and separately invoked for consequential decisions; mechanical `check` stays free, deterministic and clearly non-semantic.
- Provider/authentication/egress changes are host responsibilities. No implied consent from ambient environment variables, existing skills, source documents or repo configuration. The evaluator may execute separately authorized agents only in a qualified externally enforced environment; local subprocess policy filters are not OS isolation.
- External refs and private project source bytes stay within the operator's selected privacy boundary. Original captures may contain secrets; do not publish them or render them into public evaluation reports by default.
- `ADOPTED_ASSERTED` is still an *operator assertion*, not an authenticated approval; independent auditor actor fields remain unverified absent a qualified trust anchor. Plan or assessment status never becomes a proof verdict.
- Do not create a new mandatory `review`/`adopt` stage as a condition for a harmless ordinary planning draft. Likewise never send a `DRAFT` to Proofline as an approved contract.
- Maintain exact source quote, lifecycle, scope, document revision and evidence gap boundaries while minimizing the ordinary output. Omitted critical evidence must be explicit rather than silently dropped for compactness.
- Preserve data-only reporting for interrupted evaluations. A release scorecard must never retroactively turn a failed experiment into an unattempted one.

## 9. Release matrix and definition of done

| Gate | Requirement for engineering 0.2 | Evidence / qualification |
|---|---|---|
| No regressions | All 0.1 tests plus new suites pass; CLI/schema-1 snapshots preserved or explicit migration accepted | Exact PR-head offline results |
| One-request usability | Agent-host workflow creates a source-bound draft without manual JSON; manual fallback remains | Real smoke when available, mechanical fixture tests otherwise with honest labeling |
| Semantic changes | Each meaningful tuning change has a tied failure case and reviewed rationale | Before/after fixture and actual pilot results when available |
| Integrity/privacy | No source mutation, hidden network/inference, stale adoption or unsafe path fallback | Negative tests and CI |
| Proofline direct | Exact source+brief parser contract and full negative admission cases | Offline pass; live outcome separately observed / blocked |
| Optional Lore | No peer required; correct authority and fallback labels | Offline adapter controls or explicit deferral |
| Cross-platform | Linux/macOS/Windows Python 3.11/3.14 matrix at exact release head; qualified POSIX storage | CI URLs; Windows secure storage remains unsupported unless separately proven |
| Package | Installed CLI, docs and skills accessible from wheel + sdist | Fresh isolated installation smoke |
| External study | All genuine slots/attempts, status, review eligibility and costs visible | Live report **or** immutable `not_run` receipt; no fabricated benefit |
| Release status | Engineering complete and honest about unknown benefit | `docs/SCORECARD_0.2.md`, tagged only with authority |

### Completion report format (must be supplied by the implementing agent)

```markdown
# Intentline 0.2 implementation handoff
- Base commit / final main commit:
- PRs (number, purpose, head, merged/unmerged, required CI):
- New or changed user-visible behavior:
- Schema/CLI compatibility and migration (if any):
- Offline tests and exact platform/build results:
- Real agent trials: eligible tasks / assignments / completed / failed / refused / not_run:
- Independent audits/authentication actually available (or unverified):
- Main semantic failures identified, corrections, unchanged holdout status:
- Proofline: parser/offline gate; actual supported-host deliver/status and cost (or precise blocker):
- Lore adapter: shipped/experimental/deferred and relevant reasons:
- Measured cost/latency/correctness; unknown fields explicitly marked unknown:
- Security/authority and Windows qualifications:
- Release/tag/package publication status:
- Remaining blockers and smallest next action:
```

**Definition of complete 0.2 engineering work:** A normal command-capable agent can produce a concise source-bound draft from one request, the deterministic CLI and trust/identity mechanisms remain safe and compatible, concrete planning/audit failure modes have targeted corrections, Proofline direct inputs have reproducible qualification, optional Lore context is correctly isolated or explicitly deferred, and the project states exactly which real planning outcomes have—and have not—been independently observed.

**Explicit non-goals for 0.2:** P2P's delivery controller, a new semantic LLM runtime, mandatory MCP, long-lived service, mandatory GitHub issue integration, generated implementation code, proof execution, credential acquisition, automatic approval, arbitrary parent/child decomposition, automatic backlog slicing, built-in hosted egress, a new database/knowledge graph, native Windows secure storage without a proper qualification, and a universal claim of efficacy from a handful of tasks.
