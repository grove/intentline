# Intentline 0.4 engineering scorecard — 12 October 2026

This is optional acceptance-preserving allocation, not measured slicing efficacy.
Initial/main commit: `0ff076576317745aad66dab60a4f1bb9eb2db4b3`.
Main remains unchanged until explicitly authorized merges. No release/tag/PyPI
publication or paid inference is performed. Five stacked PRs preserve review scope.

| Package | PR / exact head | Six-cell PR CI |
|---|---|---|
| 01 NO SPLIT / frozen baseline | [21](https://github.com/grove/intentline/pull/21), `dc2b9bde04bde82785eceee0839eddb22210b377` | [38252285522](https://github.com/grove/intentline/actions/runs/38252285522), success |
| 02 SPLIT coverage / DAG | [22](https://github.com/grove/intentline/pull/22), `a6b58d28d1bc11c7f96276cf65d111d2a3db17d6` | [38252429269](https://github.com/grove/intentline/actions/runs/38252429269), success |
| 03 Skill / disputes / impact | [23](https://github.com/grove/intentline/pull/23), `e2f0c480ef0d29b654b0ab89ab9cad0394d9690a` | [38253737289](https://github.com/grove/intentline/actions/runs/38253737289), success |
| 04 Portable child data | [24](https://github.com/grove/intentline/pull/24), `12af895689b7c0fc6ea903e88094408af026b02e` | [38253866513](https://github.com/grove/intentline/actions/runs/38253866513), success |
| 05 Integration / 0.4.0 packaging | [25](https://github.com/grove/intentline/pull/25), engineering head `0bac73a0d182992ce2a8b914e851ff899681832b` | [38256691558](https://github.com/grove/intentline/actions/runs/38256691558), success |

Each matrix runs Linux/macOS/Windows × Python 3.11/3.14, build, fresh wheel/sdist
install, CLI/skill links and full offline tests. Windows qualifies installation,
no-I/O refusal and the actual narrow Win32 handle probe, not secure storage.
The first/third packages had failed Windows runs; exact heads, runs and repairs
remain in [FAILURE_LEDGER](../evaluation/FAILURE_LEDGER.md). No gate was weakened.

Local final engineering code: 120 tests on Python 3.11.17 and 3.14.8, 119 passing
and one actual-Windows probe skip on macOS. The original 86 tests are unchanged.
Fresh wheel and sdist build/install pass on macOS/Python 3.14.8, including all
three installed skill links, new schemas, source-distribution captures, both slicing
routes and isolated native/child inspection. Final CI also runs this smoke in every
cell; distribution hashes identify each actual build, not a separately published release.
Security, source/history, audit/adoption and native compatibility regressions remain
in the full suite. New no-effect assertions intercept write opens, subprocesses
and socket calls for preview/status/render/impact/inspect; both manual and packaged
skill conventions are covered without model execution.

Frozen 0.3 code/schema/skill/CI/test identities: SHA-256 `d537ddfb52be261e0786fafca7f1cee90bd21b02e853eccd9b085b5f8f8106ef`.
Exact authored old-producer contract/source/result/native captures are additionally
preserved in evaluation/baseline_04/captures with a digest inventory. They are
produced by the frozen 0.3 code, not retrospectively asserted model results.
Acceptance and result schemas 1, canonical original hashes, source manifests 1/2,
continuity, original audit/adoption and standalone export interfaces remain compatible.
New separate schemas are slicing-v1, slice-audit-v1 and slice-handoff-v1.

Positive engineering scenarios: idempotent NO SPLIT; complete flat SPLIT with
qualified local criteria, distributed and parent-only ownership, enabling work
and explicit gaps; transitive successor impact; optional disputes retained;
portable child inspection without importing Intentline. Negative scenarios:
missing/invented/orphan R/C IDs, lost boundaries/exclusions, false full roles,
unsupported recursion, cyclic/false prerequisites, corrupt/rehashed output,
missing ancestors, unsafe/hard-linked/FIFO/symlinked input, stale sources,
source deletion/reintroduction, concurrent writers and interrupted/raced markers.
Existing Proofline native/direct admission rejects child bundles before dispatch.
All positive/negative examples are authored fixtures; semantic sufficiency remains
unverified and parent acceptance remains unestablished.

Independent slicing pilot: [dated not_run](../evaluation/results/slicing-04-not-run.json),
0 eligible tasks and 0 assignments; unknown usage/effort/billing null. The original
planning_02 study/evaluator and every 0.1–0.3 receipt remain unchanged.
A separately registered read-only slicing extension reuses evaluator conventions
and validates exact shared complete parent/source payloads, input parity, private
gold separation, score provenance and adverse attempt retention. No held-out task,
real review, adoption, downstream outcome, empirical benefit or cost saving exists.

Child consumer qualification: [separate not_run](../evaluation/results/slice-consumer-04-not-run.json).
No child-adoption protocol or live Proofline run was added. Proofline main
`5ab3ff193f3d5d665645d704d9d6d7e410865b91` and P2P
`17f3deb982a8224f71b12bda74be6b24d86571e4` were actually rechecked.
Pinned upstream native consumer bytes equal the preserved compatibility snapshot.
P2P slicing principles are selectively attributed in THIRD_PARTY_NOTICES; no
peer runtime, issue management or delivery controller is imported.

Residual gates: explicit merge authorization plus exact required checks;
separate release publication authority; genuine eligible tasks, distinct checker,
two additional independent reviewers, blind scorers, qualified isolated hosts,
pinned matched models and explicit inference budgets. No independent reviewer is
claimed. Windows secure storage, owner-resistant tamper, network filesystem
semantics and power-loss durability remain unqualified. Offline child inspection
checks a frozen snapshot, not live source freshness or action permission.

Public artifacts contain only code, documentation, authored public-source fixtures
and sanitized zero-assignment receipts. Private sources/gold/reviews/outputs must
stay in owner-only external study/work storage; exports omit raw approval/audit
payloads. No unknown billing value is reported as zero.

## Recorded final engineering gate

The repaired integration head `0bac73a0d182992ce2a8b914e851ff899681832b` passes
both push [38256685087](https://github.com/grove/intentline/actions/runs/38256685087)
and PR [38256691558](https://github.com/grove/intentline/actions/runs/38256691558)
matrices: all six cells green. Linux/macOS run 120 tests with the single actual
Windows API probe skipped; Windows runs 120 with that probe actually passing.
The POSIX evaluator receipt workflow step is intentionally skipped on Windows,
where secure record operations refuse. Package build and fresh wheel/sdist install
checks pass in all six cells. No skip is reported as a functional storage pass.

The [recorded engineering self-check](../evaluation/results/engineering-04-self-check.json)
and digest retain exact code head, job URLs and actual local artifact hashes:
wheel `0a82a699c95dae9620dd4a2e27b4915fa36beaaf8279083670774efda8ec810e`,
sdist `432f7c2ac2d875e5b5608bb59f4929a38876664704b18b2425ce5d132795b241`.
These local build bytes include the final code/tests/skill but precede the appended
CI failure ledger/report. CI separately builds the exact committed head. The final
report-only commit is checked in the same matrix and bound in PR #25's description;
this document does not assert its own future CI result. All five PRs remain OPEN,
with no actual independent approvals or merge/publication authorization.
