# Intentline 0.3 engineering scorecard — 12 October 2026

Engineering release candidate in seven open reviewable work packages. No main
integration, release/tag/package publication, authenticated independent review,
actual user adoption, live native delivery or planning superiority is claimed.
The final integration commit and its exact CI are recorded in the PR description
and implementation handoff after the last commit; this file cannot name its own
commit hash. The separate consumer has its own exact head below.

Inspected original main: Intentline `02603d779dae1ecadcf11dcd65e536c83f0e8424`;
working base with operator-supplied plan `9fbec26598f9d82ab5cd47243e99255d03671592`.
Proofline main: `c4d28e4e743adbb261552323e694946f1360a129`.
The unrelated dirty original Proofline checkout was left untouched; its consumer
work uses an isolated checkout. Neither project imports the other's runtime.

| Package / PR | Exact package head | Exact-head CI (push and PR) |
|---|---|---|
| [01 review #15](https://github.com/grove/intentline/pull/15) | `265edfad7a8b78013ec3c19c4c3506362cce6cce` | [38239335210](https://github.com/grove/intentline/actions/runs/38239335210), [38239324883](https://github.com/grove/intentline/actions/runs/38239324883): 12/12 passed |
| [02 successors #16](https://github.com/grove/intentline/pull/16) | `0e3f317a0803554ba6a119eb2cb08d18c3a0b841` | [38240370860](https://github.com/grove/intentline/actions/runs/38240370860), [38240360055](https://github.com/grove/intentline/actions/runs/38240360055): 12/12 passed |
| [03 agent flow #17](https://github.com/grove/intentline/pull/17) | `3fccdf30059a7a709b171f42fddb9ae79e27e31a` | [38240727964](https://github.com/grove/intentline/actions/runs/38240727964), [38240722043](https://github.com/grove/intentline/actions/runs/38240722043): 12/12 passed |
| [04 native export #18](https://github.com/grove/intentline/pull/18) | `ab581c983e8d6e114057e0819414016b318b0a45` | [38241591794](https://github.com/grove/intentline/actions/runs/38241591794), [38241577615](https://github.com/grove/intentline/actions/runs/38241577615): 12/12 passed |
| [05 Proofline #6](https://github.com/grove/proofline/pull/6) | `2285a434c1c33e73f8d89a6c3267abcaa37e9b95` | [38244558056](https://github.com/grove/proofline/actions/runs/38244558056), [38244551500](https://github.com/grove/proofline/actions/runs/38244551500): 6/6 passed |
| [06 Windows #19](https://github.com/grove/intentline/pull/19) | `856c700f51761ccea893a1eb56cd93e968de2b8c` | [38243202386](https://github.com/grove/intentline/actions/runs/38243202386), [38243189201](https://github.com/grove/intentline/actions/runs/38243189201): 12/12 passed |
| 07 integration | Final PR/commit in handoff | Final six-cell Linux/macOS/Windows × Python 3.11/3.14 runs in handoff |

Intentline branches form the package 01→02→03→04→06→07 stack. Proofline package
05 targets its own main. The integration package pins the separately repaired
consumer and repairs advisory evidence continuity in both producer validation paths.
After authorized stacked merges, retarget subsequent PRs to main as needed and
inspect actual merged-head CI. No merged-head result exists yet. Inspected rulesets
were empty; absence of a server-required check does not waive the plan's CI gates.

| Gate | Measured result / qualification |
|---|---|
| Full Intentline offline suite | 86 tests locally on macOS Python 3.11.17 (isolated) and 3.14.8; 85 passed, one actual Windows-only probe skipped in each run |
| Compatibility | Frozen 60-test 0.2 snapshot, canonical sources/contracts/render/results and original schemas retained; identity SHA-256 `34ae4932a6d91b3806188f9ba6262582cda09f90a64446dc80f35d613ee00be4` |
| Review / authority | Full source and contract display, actual before/after fields and source support state, deterministic unapproved template; read-only paths instrumented against writes/subprocess/network |
| Successors | Exact separate original/amendment streams, current context, sealed full predecessor history, bounded ancestors, supported per-R continuity and marker-last reconciliation; omissions/aliases/interruption/stale inputs fail closed |
| Native export / admission | Portable standard-library inspector; actual producer fixtures and pinned Proofline admission tests; no implicit fallback, raw approval copy, self-authorization or execution verdict |
| Proofline offline suite | 81 tests: default 76 passed / 5 skips; opt-in macOS native security 79 passed / 2 Linux-only skips; all three fixed oracle controls passed |
| Windows | Native handle/API feasibility probe actually ran in both Windows CI cells; full secure storage remains NO-GO/unsupported with exit 3 before record I/O |
| Packaging / installed workflow | Wheel/sdist fresh-install, all CLI/help/skill/schema/doc links, original→successor→native offline workflow, standard-library-only runtime; both fresh-install gates passed locally on macOS Python 3.14.8; exact final CI in handoff |
| Host entry | Installed-file self-context smoke passed (results/host-03-smoke.json); unblinded/current agent, zero extra model processes/adoptions/audits; no product-efficacy denominator |
| Real planning study | Dated `planning-03-not-run.json`: 0 eligible tasks, 0 assignments, 0 completed/failed/refused/timeout/interrupted real arm attempts |
| Live native delivery | Dated `proofline-native-03-not-run.json`: no live candidate/review/proof/status receipts or actual caller adoption; no paid inference initiated |
| Human/model independence | No authenticated independent reviewer/approval or matched arm execution; declared fixture assertions remain unverified |
| Outcomes / usage | Quality, benefit, comparative latency, effort, tokens and billing unmeasured/null; no gain inferred from green engineering checks |
| Holdout | Unregistered, unread and untuned |

Actual adverse engineering attempts and repairs remain in
[evaluation/FAILURE_LEDGER.md](../evaluation/FAILURE_LEDGER.md), including failed
PR-03 CI. They are not hidden or relabeled as successful external evaluations.
All 0.1/0.2 scorecards, registrations, receipts and failure evidence remain immutable.

No migration is required: acceptance schema 1, source-manifest v1, canonical
hashes, current pointers, stable R IDs, result wrapper and exits remain compatible.
Successors alone opt into source-manifest v2; continuity is a separate schema-1
record. Native handoff has its own versioned envelope. Advisory direct export is
preserved for original work; successors must use native/Markdown/JSON export.

Limits: 64 active sources, 2 MiB/file, 8 MiB active bytes, eight generations,
32 MiB unique archived bytes; excess refuses without truncation. POSIX storage
qualification covers cooperative local-filesystem writers; network filesystems,
owner-resistant tamper and power-loss durability remain unqualified. Hashes bind
bytes, not semantic completeness, authenticated people or action authorization.
Proofline caller flags remain an operator assertion boundary. Shared validator
ancestry is disclosed in THIRD_PARTY_NOTICES, not claimed independent review.

Smallest next actions: review and explicitly authorize merges; then inspect
merged-head CI. Separately obtain independently eligible original tasks,
checker/two reviewers and authorized matched isolated model execution for the
planning pilot; authorize a scoped native Proofline live run with real caller
adoption and actual receipts. Those missing external prerequisites do not block
engineering 0.3.0 or justify adding a model runtime, peer dependency or fake review.
