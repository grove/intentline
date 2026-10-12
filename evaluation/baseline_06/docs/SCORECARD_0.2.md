# Intentline 0.2.0 engineering scorecard

Engineering release candidate; planning usefulness is experimental/unmeasured.
No authenticated independent review, user adoption, live usefulness advantage or
Intentline-origin Proofline delivery is claimed. No release tag/package published.
Six dependent work packages are reviewable PRs; merge still needs authorization.

Base: main `7c7ba085d9180566b01d99cb580ae36a143630de` (0.1 engineering baseline
`adc404e97dc6a6e37e63e02ccee0cd7409cc38bc` plus the 0.2 implementation plan).
Final integration head and its exact CI are recorded in the implementation
handoff/PR description after the last commit; this document cannot contain its
own commit hash. Earlier final package heads are pinned below.

| Package | Exact head | CI evidence |
|---|---|---|
| [01, #9](https://github.com/grove/intentline/pull/9) baseline/evaluator | `19a745511bb79e8823e546fbcfb0d905fe1e24f7` | [Six jobs passed](https://github.com/grove/intentline/actions/runs/38233789378) |
| [02, #10](https://github.com/grove/intentline/pull/10) one request | `e5267006db4e80f378ad90daa4277fe1f4aed4d1` | [Six jobs passed](https://github.com/grove/intentline/actions/runs/38233794076) |
| [03, #11](https://github.com/grove/intentline/pull/11) semantic probes | `8b7c256e6bc192c9a52008cfde79e014daf4a1dd` | [Six jobs passed](https://github.com/grove/intentline/actions/runs/38234120137) |
| [04, #12](https://github.com/grove/intentline/pull/12) handoff | `6b0ecf30d9b2e670d6371f712c3fe12803d0779b` | [Six jobs passed](https://github.com/grove/intentline/actions/runs/38234565360) |
| [05, #13](https://github.com/grove/intentline/pull/13) Lore | `d863ff7b99f66a2c4281d8e4072f4f0166a7236d` | [Six jobs passed](https://github.com/grove/intentline/actions/runs/38234932753) |

| Gate | Observation / qualification |
|---|---|
| Offline regression suite | 60 tests on final integration code; original 44 retained, new 16 tests; all pass locally on macOS Python 3.11.17 (isolated), 3.12.14 and 3.14.8, zero skips |
| Baseline compatibility | Exact 0.1 CLI/schema/skills/source/contract/result/renderer snapshots retained; no schema-1 migration |
| One-request planning | Host skill handles JSON/capture/check internally; mechanical repair/reuse fixture passes; installed direct-file current-Codex smoke creates one source-bound row with UI evidence gap; self-context/unblinded, not a pilot |
| Semantic planning | Six exact before/after authored probes plus original 14 good/bad scenarios; no real-model quality score |
| Source/privacy/side effects | Existing interruption, lock, no-follow/FIFO, stale/adoption/identity controls; optional report/inspect paths instrumented for zero writes/subprocess/network |
| Proofline | Pinned parser + real pinned checkout admission code exercised offline; complete export identity/tamper controls and context publication race fixed; three focused native pinned-consumer offline tests pass and its actual --contract inspector rejects the advisory brief |
| Live Proofline delivery/status/proof | not_run / blocked_external: separate model budget/spending grant and qualified authenticated run/status/candidate receipts unavailable |
| Lore | Experimental explicit report envelope inspector; ordinary --context preserves all bytes; advisory leads only, not full nested schema/registry validation or demonstrated benefit |
| Packaging | Wheel/sdist built and fresh-installed locally on Python 3.14.8; both CLI/skill-link/manual workflow gates pass; final CI runs the same gates; no runtime dependencies |
| Cross-platform | Six-job Linux/macOS/Windows × Python 3.11/3.14 matrix; exact integration-head results in handoff |
| Windows storage | Unsupported, explicit exit 3; green Windows help/parser/package controls do not qualify recording |
| Real pilot | 0 eligible tasks, 0 assigned/completed/failed/refused/timeout/interrupted real arm attempts; initial immutable not_run receipt; nine development slots are placeholders |
| Independent review/adoption | None authenticated; fixture self_check reports are test data, not real reviews/consent |
| Holdout | Unregistered and untouched; no holdout outcomes read or tuned |
| Usage/cost/quality/latency | External model calls/tokens/billing/effort unknown (null); no semantic benefit or savings estimate |

Adverse engineering runs remain historical: the initial PR-01/02 Windows jobs
failed because Git changed frozen snapshot line endings. PR-01's append-only
repair pins evidence bytes with .gitattributes; the repaired heads passed all
six jobs. Run 38233382288 (PR-01) and 38233648985 (PR-02) are failures, never
counted as passes. Local default Python 3.9 is unsupported; the host's default
Python 3.11 entry is broken and untouched. Select the isolated supported 3.11
interpreter, 3.12 or 3.14 recorded in the handoff. The new context-race test failed
before the root fix, then passed. No adverse model experiments were attempted.

Engineering 0.2.0 may ship after final offline/build/CI gates pass, while usefulness
remains unmeasured. Merge/tag/package publication requires separate authorization.
Required-check and branch-protection state are inspected, not inferred from green
checks. Hashes identify bytes, not authors, independence, authority or semantic
completeness. POSIX qualification covers cooperative local-filesystem writers;
owner-resistant tamper, network filesystems and power-loss durability are unqualified.

Smallest external next steps: source independently eligible original tasks with
checker/two reviewers; register a private pilot and authorize bounded isolated
model execution. Separately authorize one supported native Proofline smoke.
These missing evidence gates do not justify adding a model runtime or peer dependency.
