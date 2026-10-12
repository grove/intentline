# Intentline 0.5 — Demonstrate Real Acceptance-Planning Usefulness

**Implementation-ready coding-agent handoff · 12 October 2026**  
**Repository:** <https://github.com/grove/intentline>  
**Target:** Intentline 0.5 engineering work plus a **separately gated empirical usefulness decision**  
**Verified Intentline `main`:** `587ef061287f02d4d7328f7c291bf57b85892603` (0.4 PR #25 merged, 12 October 2026 13:48 UTC). The merged-head offline CI succeeded: <https://github.com/grove/intentline/actions/runs/38258294929>.  
**Verified Proofline `main`:** `023a3d5a380f4659b4459e585f1910604374d2a7` (S6 merged, 12 October 2026 13:34 UTC).  
**Verified Promise to Proof `main`:** `17f3deb982a8224f71b12bda74be6b24d86571e4`.  
**Recheck all heads, checks, and open work before implementing.** The identities above describe the inspected starting point, not a guarantee that branches remain unchanged.

> **0.5 product question:** Compared with an equally equipped coding agent planning normally—or using P2P's standalone `plan-acceptance`—does Intentline produce more complete, appropriately scoped, independently checkable acceptance plans with acceptable all-in cost and user burden?

## 0. Mandate for the implementing coding agent

**Implement the engineering packages below; do not only write another plan.** Inspect current source, adapt to changed code, work autonomously on permitted tasks, fix reproducible defects, and run focused and integrated tests. Keep distinct reviewable changes in dependency order, with precise commits and handoff reports. Do not commit or merge, create PRs, tag a release, publish a package, spend money, or modify other repositories unless the operator's actual grant covers that effect. If an effect is unavailable, complete a local PR-ready branch and state its exact remaining authorization. No force pushes, deletion of old study results, or rewriting of historical scorecards.

**A blocked external study is not a reason to stop engineering.** Perform all possible source research, candidate preparation, permission-safe artifact collection, reproducible hashing, offline eligibility checks, packaging and failure-preserving validation. Do not represent independently authored work, reviewed gold answers, isolated model runs, authenticated approval or measured usefulness as accomplished unless genuine externally verifiable evidence exists.

**No inference authorization is implicit.** Existing credentials do not authorize model spending. Host, model, time, token, dispatch and egress permissions are separate operator decisions. Do not run real hosted/local inference with meaningful resource cost, launch a study, or run Proofline delivery without explicit bounded authorization. Deterministic offline CLI/CI and ordinary repo tests are allowed within the implementation environment's grants.

**Keep the projects separate:**

- **Intentline:** candidate-independent acceptance planning, optional independent planning audit, amendments, contract provenance and optional slicing.
- **Lore:** optional evidence-bound project intelligence; never grants policy, approvals or runtime access.
- **Proofline:** optional delivery, frozen implementation candidates, independent review and behavioral proof. It owns the native host boundary and any verification fixes.
- **P2P:** reference implementation and matched planning baseline, not an Intentline runtime dependency.

No new coding agent, task dispatcher, paid-model SDK, GitHub issue orchestrator, daemon, database, required MCP server, or competing evaluation framework is permitted in 0.5. Production Intentline remains Python 3.11+, standard-library-only, local/offline and model-free at the CLI boundary. Preserve Apache-2.0 attribution when reusing P2P material.

## 1. Verified 0.4 baseline and actual gaps

### 1.1 Implemented behavior—reuse, do not rebuild

Intentline 0.4 has three host-readable agent skills:

- `skills/intentline-plan/SKILL.md` — one-request source-grounded acceptance draft.
- `skills/intentline-audit/SKILL.md` — optional review of exact original promises versus planned obligations, with truthful independence labels.
- `skills/intentline-slice/SKILL.md` — default `NO SPLIT`, or flat 2–8-child advisory decomposition when a concrete extra verification/delivery boundary is justified.

The CLI implements `prepare`, `propose`, `check`, `render`, `status`, `review`, `approval-request`, `amend-source`, `reconcile`, `audit-record`, `adopt`, `export`, `inspect-native` and `slice` actions. It preserves exact source captures, stable requirement IDs, immutable revisions and successors, full source-line citations, disputes, narrow authority semantics, and portable source-bound exports. Proofline already supports experimental native **standalone** Intentline contract inspection/adoption; Intentline **child** exports remain **advisory** and are rejected by existing Proofline direct/native delivery paths.

Relevant implementation paths:

| Existing concern | Reuse these actual modules / contracts |
|---|---|
| Source capture and safety | `intentline/sources.py`, `paths.py`, `records.py`, `amendments.py` |
| Contract identity / amendment | `intentline/contracts.py`, `continuity.py`, `review.py`, `schemas.py`; `schema/acceptance-v1.schema.json`, `continuity-v1.schema.json` |
| Audit / adoption | `intentline/audits.py`, `adoption.py`; `schema/audit-v1.schema.json`, `approval-v1.schema.json` |
| Handoff | `intentline/export.py`, `native_handoff.py`, `native_inspect.py`, `slice_export.py`, `slice_inspect.py` |
| Slicing | `intentline/slicing.py`, `slice_records.py`, `slice_audits.py`, `slice_impact.py`; `schema/slicing-v1.schema.json` |
| Agent workflow | `skills/intentline-{plan,audit,slice}/SKILL.md`; `docs/AGENT_GUIDE.md`, `SLICING.md` |
| Existing planning experiment | `evaluation/planning_02.py`, `rubric_02.md`, `cases/registration_03.json`, `results/planning-03-not-run.json` |
| Existing slicing experiment | `evaluation/slicing_04.py`, `rubric_04.md`, `cases/registration_slicing_04.json`, `results/slicing-04-not-run.json` |
| Existing optional consumer assessment | `evaluation/handoff_02.py`, `evaluation/PROOFLINE_HANDOFF.md`; Proofline's own `checks/intentline_input.py` and `docs/S2-CONTRACT-INPUT.md` |
| Quality receipts | `docs/SCORECARD_0.4.md`, `docs/IMPLEMENTATION_0.4.md`, `evaluation/FAILURE_LEDGER.md` |

The 0.4 local suite is recorded as **120 tests** (119 pass, one actual-Windows API test skipped on macOS); Linux/macOS/Windows × Python 3.11/3.14 CI passed at the merged head. Green Windows jobs **do not** qualify secure Windows record storage; it still refuses record operations with exit 3. A GitHub Release or package publication was **not observed** in the repository inspection; do not silently assert one exists. Some 0.4 documentation retains pre-merge wording: correct the *current product guides* using actual GitHub state while preserving historical handoff documents as dated evidence.

### 1.2 The missing evidence is the central 0.5 task

- The registered planning and slicing comparisons have **zero independently eligible real tasks and zero real assignments** in their dated public `not_run` receipts.
- Public good/bad fixtures and self-context installed-skill smokes establish mechanics, **not** real-model planning quality, user mastery, independent reviewer identity or efficacy.
- No actual authorized Intentline-origin **native Proofline** delivery, candidate, reviewer/prover receipt and final status has been established in the Intentline evidence.
- **New external safety fact:** Proofline's current S6 experiment (<https://github.com/grove/proofline/blob/main/docs/S6-RESULTS.md>) stopped at a trust gate after **69 of 120 assigned runs**, including **one false acceptance by Proofline**. This is **not evidence of an Intentline defect**, but it means no 0.5 integration result may be called safely verified merely because a Proofline workflow reports acceptance. Check the consumer's subsequent trust remediation before any authorized live integration.
- Broad usefulness, comparative time/cost and slicing gains are **unmeasured**. Unknown token counts, billed USD, human attention and missing runs remain unknown/null, not zero.

## 2. Product objectives and two separate release decisions

**Engineering objective:** Make actual independent trials straightforward and auditable; remove observed one-request friction without adding ceremony; retain trustworthy offline contracts, package/evaluation reproducibility and relevant regressions.

**Empirical objective:** Complete and independently assess a small genuine matched planning pilot, then decide whether further features are justified. A six-to-nine-task pilot is *diagnostic*. Claims of broad superiority need a separately registered untouched holdout, adequate independent sample size and uncertainty analysis. Never describe authored fixtures as real tasks or make strong statistical claims from a single small pilot.

**Release decision A — engineering:** Versioned 0.5 candidate / RC may be prepared with passing tests, cross-platform CI, source/authority safety and truthful `not_run` evidence, even if external human/model prerequisites are blocked. An unavailable pilot must not be concealed by an apparently successful engineering scorecard.

**Release decision B — observed usefulness:** A 0.5 release or headline that **claims improved acceptance planning** requires actual eligible independently evaluated task runs, a measured matched comparison, full adverse-attempt accounting and accurate limitations. When unavailable, record `blocked_external` or `unmeasured`, and state that 0.5's empirical objective remains unmet. Never invent a pilot merely to meet a version target.

### 2.1 What 0.5 must enable in the normal user journey

A developer can tell their command-capable coding agent: **“Use Intentline to plan acceptance for this request”** and receive a concise draft with real R IDs, requirements, exclusions, boundaries, evidence methods, decision gaps, exact source/contract identity and one next useful action. The agent handles JSON and CLI stages internally; no mandatory second model audit, human questionnaire, task splitting or Proofline invocation. It does not silently adopt or implement the agreement.

For consequential work, a separate actual reviewer can independently audit the frozen proposal. A legitimate adopter can authorize its exact source and revision by an externally established action; Intentline only records an operator assertion and cannot authenticate it itself. An amended plan or new source generation invalidates prior adoption for that successor. Slicing remains opt-in and defaults to NO SPLIT.

## 3. Work packages and PR order

| PR | Priority | Package | Deliverable | Dependency |
|---|---|---|---|---|
| **01** | P0 | Reproducible study readiness & genuinely eligible task intake | Frozen 0.4 baseline, source-pinned candidate prep, private study handoff, exact readiness report | None |
| **02** | P0 | Actual user-workflow observation and targeted ergonomics | Installed-skill user path, reproducible usability protocol, tested fixes only where evidence supports them | 01 baseline |
| **03** | Conditional P0 | Evidence-driven planning/audit/slicing corrections | Targeted corrections for actual reviewed development failures, with negative controls and holdout separation | 01/02; may be documentation-only if no findings |
| **04** | P1 | Real Proofline trust-gated native handoff readiness | Exact standalone handoff checks, negative controls, separate safe operator recipe and receipt processing | 01; consumer safety gate |
| **05** | P0 | Slicing study preparation and decision policy | Existing 0.4 matched evaluator used intact; NO SPLIT/SPLIT diagnostic rubric and honest assignment accounting | 01; parallel with 02–04 |
| **06** | P0 | Integrated 0.5 engineering / empirical report | Full CI, packaged workflow checks, measured-versus-missing ledger, independent release decisions | 01–05 feasible work |

Packages 03 and live portions of 04/05 are explicitly conditional on real evidence and authorization. Do not add dummy product features simply to fill a PR. PR-sized commits are acceptable instead of empty PRs. Do not merge unreviewed branches or pretend a red test is green.

### PR-01 — Freeze 0.4 and make independent tasks genuinely preparable

**Purpose:** The next improvement is **real study inputs**, not another model launcher or rewritten evaluator. Keep private answers/checker material outside model-visible input and public source control.

**Implementation locations:** Reuse `evaluation/planning_02.py`, `evaluation/slicing_04.py`, `evaluation/README.md`, `evaluation/rubric_{02,04}.md`, `tests/test_evaluation.py`, `tests/test_slicing_evaluation.py`, and baseline captures. Introduce at most one focused **read-only / offline** intake diagnostic under `evaluation/` *only if the existing validators do not already perform that mechanical check*. Add `evaluation/INTAKE_05.md` and `evaluation/results/planning-05-not-run.json` as sanitized, distinct records; never overwrite 0.2/0.3/0.4 receipts.

**Engineering steps:**

1. Pin current `main`, old canonical JSON/result/CLI/source contracts, three installed skills and representative source/review/export/slice bytes. Hash snapshots with SHA-256, retain original outputs, and compare after later changes. Do not normalize away meaningful byte differences to make a baseline pass.
2. Inventory the **existing** study schemas, registration fields and validator limitations. Prefer a checklist and deterministic inspection function over a new evaluator. All new negative controls must feed actual `planning_02.validate/assess` or `slicing_04` APIs where applicable.
3. Write a private task-intake template covering: independent upstream `owner/repo` project; exact full upstream commit and license; real preexisting source documents and chronological decision evidence; exact original request; equal-per-arm permitted source snapshots; task scope; provenance; checker/reference-answer authorship; two additional independent task/gold reviews; conflicts, corrections and timestamped captures; declared host/model permissions; and private-only outcome records.
4. Prepare research-based **candidate** tasks, if feasible from permitted public sources, without fabricating author or reviewer status. Candidate sourcing may locate authentic accepted-vs-proposed rules, scoped exceptions, negative knowledge, regression behavior and genuine decisions in pinned history. An agent-authored or agent-transformed candidate remains `candidate_unreviewed` until separate accountable people really contribute and review it. Prefer six to nine eligible tasks across at least three distinct projects for the initial study; nine is the intended diagnostic cohort, six is the minimum to begin subject to protocol.
5. For each candidate, preserve original documents **verbatim** and hash every byte. Store task drafts/source captures in a new owner-only **private directory outside the tracked repository**. Store independently generated gold/checker/reviewer captures in separate private paths inaccessible to every planning arm. Preserve any possible overlap with Lore's study as a disclosed contamination risk; do not recycle Lore's exposed answer keys or public development fixtures as a fresh holdout. Do not commit private drafts, gold, private actor information or full model transcripts.
6. Pre-register **three matched planning arms** using the existing study contract: ordinary agent planning, same agent with Intentline's exact installed skill, and P2P standalone `plan-acceptance` (not its delivery controller). Pin actual model IDs, revisions, reasoning effort, tool access, time/turn limits, same original sources and presentation. Account separately for preparation, installation, initial reads, repairs and audit effort. Do not fill in unknown model/provider identities with requested CLI flags.
7. Establish source-to-output **blind scoring**: same original source and complete substantive output, arm labels stripped without removing actual requirements, two distinct blinded scorers per eligible completed output, every original promise mapped or marked omitted, every added binding requirement justified or marked invented; every score cites original source and exact output identity. Record reviewer disagreements instead of averaging them out of existence.
8. Validate that every task-arm assignment exists, including `failed`, `refused`, `timeout`, `interrupted` and `not_run`. A run whose provenance or billing is unknown retains null fields. The result is a descriptive pilot, not a causal proof of general effectiveness.
9. Produce an **actual read-only preflight report**: `eligible_count`, `candidate_count`, `registered_assignments`, `executed`, `missing_authors`, `missing_independent_reviews`, `model_authorization`, `host_isolation`, `blinding_ready`, `cost_permission`, each with exact evidence/path or blocker. Do not count an empty study as an eligible cohort.
10. If independent humans, model access or spending authorization are missing, complete the source/candidate/validator work possible and publish a precise sanitized `not_run` status, not an invented participant or completed pilot.

**Negative tests:** missing task/gold or reviewer capture, duplicate/conflicted actors, incorrect source commit/license, different arm context, private gold in model-visible bundle, tampered hashes, review after scoring, missing blind output ID, missing failed assignment, ineligible public fixture, inconsistent usage, unsafe symlink/FIFO/traversal, arbitrary claims of external host authentication. Test that `not_run` never produces effect-size or savings claims and that original 0.2/0.4 registrations stay byte-identical.

**Exit:** A participant/operator can determine exactly which independent artifact remains missing for each candidate without reading private answers or launching inference; baseline tests and existing evaluator remain intact.

### PR-02 — Make the existing agent workflow actually easy to use

**Purpose:** Improve the user experience through specific observations, not by adding a controller or silently granting capabilities.

**Implementation locations:** `docs/AGENT_GUIDE.md`, `README.md`, `docs/TUTORIAL.md`, `docs/CLI.md`, packaged `skills/intentline-{plan,audit,slice}/SKILL.md`, `evaluation/package_smoke.py`, and focused `tests/test_one_request.py`, `test_skills.py`, `test_workflow.py`, `test_security.py`.

**Engineering steps:**

1. Supply one concise, supported host entry that works with a command-capable agent's installed **whole skill tree**, preserving relative schema/docs references. The current direct-file path is qualified for Codex; do not claim native slash-command discovery or Claude Code parity without actually observing it.
2. Make `README.md` distinguish a verified **merged code version** from actual GitHub Release/PyPI publication. Fix obvious stale current-document wording (e.g. 0.4 described as PRs still open) without retroactively rewriting dated historical receipts.
3. Create a **first-use observation protocol** for real developers (outside CI): install source/wheel, locate skill, ask one task, verify exact request capture, inspect output, optionally amend, optionally NO SPLIT, and optionally export. Record actual user actions, prompts, commands, elapsed time, failures, manual JSON/hash work, missing original bytes, denied grants and unsupported host entry. Get explicit participation permission; treat observer notes as private. A first-party automated self-smoke is **not a human usability study**.
4. Fix deterministic, reproducible mechanical friction exposed by the real installed workflow—broken skill links, bad relative references, confusing CLI status, accidental extra manual steps, or misleading readiness text. A small tested read-only skill-path/help affordance is acceptable if demonstrated useful; do not introduce `intentline plan` that spawns models, automatic AGENTS.md/CLAUDE.md writes or implicit repo indexing.
5. Keep the normal agent interaction **one planning request, one useful draft**, with no mandatory audit, approval, GitHub issue creation, slicing or Proofline call. Preserve truthful `DRAFT`, `BLOCKED`, `STALE` and evidence-gap meanings. Do not force an uninformed user to supply hashes or edit JSON that the host can correctly handle.
6. Repeat a fresh installed-wheel and fresh-sdist smoke on Python 3.11 and 3.14; test task with (a) no context, (b) permitted docs, (c) missing harness disclosed as gap, (d) material open decision, (e) changed source, (f) unchanged rerun reusing the same contract hash. Preserve exact original request bytes or explain why original capture was unavailable.
7. Keep any actual host/model test and its billing or cost separately authorized and bounded. Without a qualified real host, run offline fixtures, leave actual usability and agent-efficacy observations `not_run`, and document the precise supported manual fallback.

**Negative tests:** source instructions trying to enable egress, auto-approval, dependency installation or file editing; missing original chat bytes mislabeled exact; model-written approval; absent Lore treated as blocking; read-only path creates bytecode/cache/locks; repeated unchanged plan needlessly revises identity; easy task automatically split; missing harness turned into a product blocker.

**Exit:** A first-time user has a single concise documented way to invoke planning in one supported host, plus a dependency-free manual fallback; actual observed versus simulated ease-of-use is labeled separately.

### PR-03 — Correct *observed* planning errors, not benchmark-shaped speculation

**Purpose:** If genuine development cases reveal wrong recommendations, fix the smallest supported failure without rebuilding the planner.

**Implementation locations:** principally the three skills, `evaluation/FAILURE_LEDGER.md`, `evaluation/semantic-probes.json` and focused tests. Modify production validators only for an actual deterministic defect with a negative reproduction. Keep `schema/acceptance-v1.schema.json`, original canonical records and unchanged output contracts stable by default.

**Engineering steps:**

1. Triage real **development** planning/audit/slicing failures against frozen original requests: omitted promised behavior, invented obligation/exclusion, lost accepted scoped exception, proposed rule promoted to authority, weak candidate-derived oracle, missing evidence gaps, unnecessary blocker, or false-positive split.
2. For each failure retain: exact source/plan/revision/hash, task status, real run/model/host provenance (or explicit authored fixture), independently documented expected answer when available, a plausible wrong behavior and the smallest correcting change. Never label an authored bad plan as observed model failure.
3. Write at least one focused **before/after** test that fails for the original defect and passes for the proposed fix. Include the nearest negative or valid-alternative control to ensure the change does not create overblocking, invented scope or unnecessary inference.
4. Prefer precise skill wording, output presentation or deterministic structural validation over another model call, generic heuristic checker, multi-agent approval loop or second authoritative store.
5. Run old regression suites and compatibility tests. An improvement on seen development tasks is not an improvement on untouched held-out tasks. Register holdout identities before tuning and prohibit lookup/use of their gold or outputs during changes.
6. If genuine development cases are unavailable, **do not manufacture product corrections**. Complete known offline correctness/security fixes if actually reproduced; otherwise deliver a triage protocol and preserve the code as-is. An empty PR must not be created just to satisfy the numbering.

**Exit:** Every functional change is tied to a documented real/mechanical regression, with source-cited controls, preserved prior failures and exact result comparisons. No regression is attributed to nonexistent study results.

### PR-04 — Safe native Proofline handoff qualification, not a new verifier

**Purpose:** Determine whether an actual accepted Intentline agreement can survive a separately authorized delivery without losing the original promise. Respect the consumer's **current trust gate** and keep the Proofline runner outside Intentline.

**Implementation locations:** `intentline/native_handoff.py`, `native_inspect.py`, `export.py`, `evaluation/PROOFLINE_HANDOFF.md`, `evaluation/handoff_02.py`, `evaluation/results/`, `tests/test_native_handoff.py`, `tests/test_integration_03.py`, existing compatibility snapshots. In Proofline, inspect `checks/intentline_input.py`, `proofline.py`, `docs/S2-CONTRACT-INPUT.md`, S6's observed false-acceptance report and any later independent trust-remediation PR; **change Proofline only for a demonstrated generic consumer defect and in its own separately authorized PR**.

**Engineering steps:**

1. Re-pin the **current consumer**, its native input/authority contract, qualified OS/Codex/model boundary and current S6 trust findings. The earlier Intentline 0.3 native tests pin a different Proofline revision; refresh compatibility **only after reviewing actual behavioral differences**, never by blindly accepting a new hash.
2. Use 0.3's **standalone native** format for this gate. Keep child bundles **advisory/unsupported** in Proofline; 0.5 does not introduce child dispatch or claim parent completion. The complete current original/amended source, constraints, exclusions, history and R IDs must be inspected and revalidated at consumer admission and final status.
3. Add/retain zero-dispatch offline negative controls: no actual caller adoption, changed contract, changed source chain, swapped document, stale successor, rehashed missing exclusion, changed candidate, counterfeit approval text, forged `ADOPTED_ASSERTED`, missing native input, hidden child `S#` package, disallowed fallback to `--source/--brief`, dirty product checkout, simulated false acceptance. A fake proof role's `PASS` must **not** be interpreted as authenticated proof.
4. Explicitly gate any real run on **consumer trust remediation or scoped verification qualification addressing S6's false acceptance**, plus actual task-specific trusted-caller adoption of exact contract/source-chain/bundle bytes, independently qualified native host, external isolation/egress evidence, fixed CLI/model/reasoning and time/dispatch/cost authorization. A current GitHub branch/tag, passing unit suite or previous S2 result alone is not that qualification.
5. Only when all those gates exist, run **one bounded native local-only** Intentline-origin delivery on a clean tracked test project under Proofline's documented command. Capture every attempt, retained source, candidate SHA, exact native run/status receipts, real reviewer and prover results, independent behavioral observations and any false-acceptance/false-blocking finding. No PR/merge, remote effects or deployment are part of this diagnostic.
6. If execution is unavailable or trust-gated, create a truthful `not_run` / `blocked_trust_gate` private record and sanitized public summary, including exact absent authorizations, host captures, identities or qualifications. **Do not substitute fake-host tests for positive live receipts**, and do not weaken the runner's sandbox to get a green status.
7. If a generic consumer defect is demonstrated, isolate it in Proofline, fix it with a failing negative-control test and separate independently reviewable PR, and requalify the native path under the consumer's own policy. Intentline never takes ownership of independent proof or code delivery.

**Exit:** Complete runnable, permission-safe operator recipe and offline negative coverage; live result only if separately authorized, independently checked and not blocked by unresolved trust concerns.

### PR-05 — Use 0.4 slicing study; do not create another benchmark

**Purpose:** Decide whether optional slicing selects better delivery boundaries or adds unnecessary verification cycles.

**Implementation locations:** Reuse `evaluation/slicing_04.py`, `evaluation/rubric_04.md`, `evaluation/cases/registration_slicing_04.json`, `skills/intentline-slice/SKILL.md` and existing `slice` contracts. Add a dated 0.5 study registration/`not_run` receipt without modifying the earlier 0.4 registration. No new scheduling/execution framework.

**Engineering steps:**

1. Source candidate parent agreements from real pinned projects, with clear and ambiguous decomposition cases, genuine `NO SPLIT` cases, parent-level interaction obligations, cross-cutting constraints and at least one necessary compatibility/prerequisite boundary. Review suitability independently; no constructed task is counted as genuine held-out material by relabeling it.
2. Match three slicing arms: ordinary agent decomposition, Intentline's optional slice skill, P2P `slice-contract` alone. Each sees the **identical complete parent agreement and original documents**, not a selectively weakened ordinary baseline. Follow the existing private gold, two-scorer, blind-ID and matched model/tool/budget rules.
3. Use the existing adverse dimensions, especially `false_positive_splits`, `missed_necessary_splits`, `lost_parent_requirements`, `invented_child_obligations`, `constraint_leakage`, `missing_parent_integration`, `prerequisite_errors`, `avoidable_verification_cycles`, `weak_oracles` and `missing_gap_disclosures`.
4. A larger number of children or more detailed breakdown is **not a success metric**. Record extra implementation/review/proof cycles expected by the proposal and actual downstream work only when separately authorized and measured. `NO SPLIT` is a successful outcome on appropriate tasks.
5. Never create issue trees or invoke delivery to demonstrate slicing. Child handoffs remain advisory, no code implementation/proof is invented, and accepted child results cannot certify a parent.
6. With external prerequisites missing, finish candidate research and private packaging as far as permitted and maintain a precise `not_run` receipt instead of altering the old evaluator or inventing reviewers.

**Exit:** An exact, fair slicing-evaluation handoff with eligibility counts and private/public boundaries, plus actual descriptive outcomes only when independently observed.

### PR-06 — Integrated 0.5 scorecard, QA and two release decisions

**Purpose:** Deliver an internally coherent versioned engineering result and tell the user what has—and has not—been demonstrated.

**Implementation locations:** `README.md`, `docs/AGENT_GUIDE.md`, `docs/DEVELOPMENT.md`, `docs/INTEGRATIONS.md`, a **new** `docs/SCORECARD_0.5.md`, `docs/IMPLEMENTATION_0.5.md`, `evaluation/README.md`, `evaluation/FAILURE_LEDGER.md`, `.github/workflows/ci.yml`, `pyproject.toml`, `tests/*` and packaging smoke. Preserve 0.1–0.4 historical scorecards, source snapshots and receipt bytes.

**Engineering steps:**

1. Keep `intentline.acceptance` schema 1, `intentline.result` wrapper/schema 1, existing exit status meanings, source-manifest v1/v2, continuity, revisions, canonical SHA-256, existing CLI commands, portable native/child formats, audit/adoption truth semantics and original work records **backward compatible**. Any incompatible repair needs an explicit proposal and migration test, not silent mutation of old records.
2. Maintain separate measurements: offline regression pass; package/OS qualification; normal manual/agent experience; real independently eligible planning study; slicing study; actual verified Proofline handoff; separate consumer trust qualification; authenticated adoption/review status; billing/cost. Use `passed`, `failed`, `not_run`, `blocked_external`, `blocked_trust_gate`, `unsupported` accurately. Never turn an omitted/unknown field into zero.
3. Run focused tests after each code change, and the full standard-library unittest suite after the final functional change. Run wheel/sdist build and fresh installs; verify installed skill/docs/schema links, complete manual planning + optional NO SPLIT + successor review + exported native/child refusal on an isolated sample, byte-bound identity, no model calls and zero unauthorised effects.
4. Require exact-head GitHub CI on Linux, macOS and Windows with Python 3.11 and 3.14; Windows must continue its secure no-I/O refusal unless a separately qualified secure backend is actually implemented. Preserve failing runs and skips as failures/skips, not passing outcomes.
5. Verify before publishing that private task/source/gold/reviewer/model records, credentials and raw approval/Proofline receipts have not been staged. Only public authored fixtures and sanitized aggregate/status records belong in the public repo. Source snapshots may be sensitive even when SHA-256 named; filenames and IDs can leak information.
6. Report the exact 0.5 engineering status independently of the empirical decision. Set package version only after all engineering requirements pass; label the release experimental/RC if usefulness remains unknown. Do not claim stable empirical success, superiority, validated independent review, live Proofline qualification or release publication without real evidence. Tag/package publication requires separate operator authority.
7. Preserve reproducible failure triage, including false acceptance and false blocking. A result from the original candidate evaluated after the fact cannot be quietly reclassified as a fresh held-out success.

**Exit:** Reviewable change set with full tests/CI, complete reproducibility inventory, exact permissions/budgets and one concise final engineering+empirical completion report.

## 4. Acceptance and negative-control matrix

| Scenario | Expected accepted behavior | Must be rejected / preserved qualification |
|---|---|---|
| Exact request retained | Original UTF-8 bytes and matching line/source identities | Summarized chat text passed off as exact original |
| Agent draft from one request | Clear source-backed R obligations and next action; no manual JSON in supported host | Auto-generated adoption, delivery or extra model agent |
| Authority conflict | Explicit open decision, unaffected requirements retained | Proposal/report silently replaces accepted scoped rule |
| Missing verification harness | Honest evidence gap, useful settled obligations preserved | Product blocker or invented test execution |
| Identical rerun | Existing current revision and hash reused | Fake amendment or silent new R IDs |
| Amended request | Distinct successor with complete continuity and fresh adoption boundary | Inherited old approval after A→B→A |
| Source context changed | Stale/witness-qualified advice; fresh applicable evidence needed | Historical quote treated as current policy |
| NO SPLIT | No children; coherent direct delivery; reason/next action | Splitting by counts, files, perceived difficulty or long prompt |
| SPLIT | Every parent R and inherited condition accounted for; final integrated verifier named | Lost exclusion, invented child product, child acceptance labeled parent proof |
| Planning study | Distinct authors/checker/two reviewers, same sources, matched arms, blind scoring | Fixture promoted to real task, hidden gold shown to agent, fake reviewed task |
| Adverse study attempt | Failure/timeout/refusal/unexecuted retained; null unknown cost | Deleting failures to improve denominator or billing set to zero |
| Native consumer admission | Exact authorized standalone source/contract/bundle; frozen candidate/status | Mock proof mistaken for independent proof; forged caller adoption |
| Proofline trust gate | Live run blocked pending real trust qualification | S6 false acceptance ignored; sandbox weakened or false PASS promoted |
| Unsupported Windows storage | Exit 3 before record I/O, install/help still work | Falling back to unsafe filename/path operations |
| Read-only command | No writes, subprocess, egress or model use | Hidden cache, `.pyc`, lock, Git mutation or network call |
| Private corpus | Original/gold/reviewer/model raw bytes isolated and not committed | Public private answers, role captures or confidential task text |

Use negative tests against **real production validators** where possible; textual assertions in skills alone are insufficient for security invariants. Preserve valid-alternative and unchanged-behavior controls so a new guard cannot pass by rejecting everything.

## 5. Study methodology and decision criteria

### 5.1 Planning pilot eligibility and comparison

- **Population:** target nine genuinely independent acceptance-planning tasks from at least three licensed, exact-pinned original software repositories; at least six from three projects for a bounded diagnostic start. Reject purely synthetic restoration fixtures and repeated near-duplicates. Include accepted versus proposed, scoped exceptions, historic policy changes, negative cases, explicit exclusions, ordinary simple tasks and consequential design changes. Avoid overfitting to tasks that require Lore.
- **Originals parity:** Every arm sees the same exact original request, permitted project documents and code where permitted. Only the workflow/skill changes. Same model/version/reasoning, tool/egress grants, horizon, reset state, and recorded source access. Differences must be disclosed; do not characterize unbalanced observations as causal.
- **Reference:** Independent accountable task author, independently authored checker/reference, plus two distinct additional reviewers with source-citation and conflict records. Task review happens before the execution registration; answer scoring is blinded by outputs. The operator and model cannot impersonate those roles.
- **Assignment accounting:** Every task gets all three arms, including not-run and failed outcomes; 9 × 3 means 27 registered attempts before any extras. Keep all attempts, retries and failures. Reruns are new declared studies, not silent replacements.
- **Rubric:** Reuse seven `rubric_02.md` dimensions; evaluate a critical failure separately from stylistic quality. For each original promise check output coverage; for each output obligation check original support. Independent expected behavioral oracle must not be derived from proposed implementation. Scorer disagreements remain visible.
- **Cost:** Capture total human/agent interactions, preparation/setup, end-to-end elapsed time, model calls/turns, input/output/cached tokens where available, and actual billed USD only when truly supplied. Compute ratios only over observed, comparable denominators. Do not declare missing billing to be zero or infer dollar invoices from a requested model name.
- **Inference:** This diagnostic pilot does not establish broad efficacy. Pre-register a distinct untouched holdout before changing semantic skills based on pilot outcomes. General claims require adequate genuinely new held-out tasks, matched uncertainty estimates and honest audit of possible leakage. Preserve negative results; improvement is not a precondition to publishing truthful findings.

### 5.2 Slicing study is separate

Re-use `slicing_04.py` and `rubric_04.md`; do not pool results with planning scores or treat a good `NO SPLIT` as missing output. Consider independently checked extra full delivery/verification cycles and downstream outcomes only if measured through a separately authorized system. A flat decomposition does not grant implementation permission or prove any accepted parent outcome.

### 5.3 Release decision rule

- **Offline engineering pass:** product + all preserved compatibility/security/packaging/CI gates pass at the exact final head. If some external studies remain unavailable, record precise `blocked_external`/`not_run` without stopping unrelated work.
- **Empirical diagnostic observed:** independent task and output reviews plus genuine real-model assignments exist and are re-auditable; provide arm-by-arm counts, failures, missing measures and uncertainty, with no invented superlative claim.
- **Trust:** a native Proofline false acceptance, unchecked caller adoption, leaked gold or source/contract tampering is a *material stop*. No green CI, a better average score, or a low latency number overrides it. A repaired consumer must separately demonstrate requalification; the producer cannot self-attest its adequacy.
- **Strong usefulness/superiority claim:** defer until a prespecified held-out comparison supports it and no critical trust defect invalidates the interpretation. If results show equal/worse planning quality with more overhead, recommend reducing ceremony instead of adding new features.

## 6. Non-goals and architectural restrictions

No recursive slicing, automatic issue publication, project-tracker integration, autonomous implementation, test execution from the production CLI, Proofline child-bundle admission, novel cross-project intelligence store, background monitoring, first-party hosted inference client, implicit spending, generalized host runner, mandatory human quiz, or forced use of Lore/P2P/Proofline. Native Windows record storage remains a separately qualified security project rather than a rushed 0.5 feature. Avoid shipping a second authoritative representation for the same contract or broadening authorizations through repository text or model responses.

## 7. Completion report format — required from the coding agent

Create `docs/IMPLEMENTATION_0.5.md` and `docs/SCORECARD_0.5.md` as truthful engineering/empirical summaries. Also provide a final response with:

1. **Baseline:** exact starting `main` SHA and original full-suite/CI observation, and exact final SHA.
2. **Delivered PRs:** work package, branch/PR URL or local commit, changed paths, merge state and CI for each exact head. Explain any conditional/empty PR omitted.
3. **Engineering results:** actual focused/full test counts, platform-specific pass/fail/skip, fresh wheel/sdist checks, source/history/privacy regression, failed tests and repairs retained, validation commands and actual artifact digests.
4. **Pilot evidence:** candidate versus independently eligible tasks, assigned versus executed, failures/refusals/timeouts, roles and available authenticated independence, original and outcome hash bindings, blind scoring, exact missing external prerequisites and untouched holdout. Never print private gold or person identifiers publicly.
5. **User experience:** what has been observed on a real installed host versus documented/manual/self-check-only behavior, and measured friction/effort if available.
6. **Proofline:** consumer revision, S6 trust-gate disposition, standalone native input coverage, positive/negative live gate status and real candidate/review/proof receipts only if observed. No child/parent proof claims.
7. **Two decisions:** engineering ship/RC status and independently observed usefulness status, each with an explicit pass/fail/not_run/blocked justification.
8. **Residuals:** precise next operator grants, task/reviewer requirements and security/host limitations; one next supported action for each open gate.

**Definition of done:** All feasible P0 engineering preparation, safeguards, regressions, packaging and reproducibility work completed and reviewed; empirical claims only where independent actual evidence exists. Missing reviewers or model-budget authorization may block the empirical milestone, but cannot turn completed offline engineering into an all-or-nothing failure, nor be disguised as an independent study.
