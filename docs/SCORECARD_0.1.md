# Intentline 0.1.0 engineering scorecard

This is an initial implementation candidate, not a published release or proof
of model quality. Exact candidate commit and PR status are reported in the
delivery report; validate with `python -B -m unittest discover -v` at that commit.

| Gate | Observed result |
|---|---|
| Offline unit/integration suite | 40 tests pass on local macOS Python 3.12.14 and 3.14.8; zero skips |
| Source fidelity, quotation and immutable history | Tested positive/negative controls |
| Staleness, source/approval identity, revision invalidation | Tested |
| Cooperative contention, process termination, interrupted recovery | Tested locally |
| No-follow paths, parent identity replacement, traversal/FIFO/size/binary rejection | Tested locally |
| Read-only CLI writes, subprocesses, network | Instrumented refusal tests pass with Python -B |
| Markdown escaping, canonical JSON and seeded round trips | Tested |
| Pinned Proofline direct-input parser | Exact extracted parser, source/brief byte test passes; no live delivery |
| Wheel/source archive, clean install, installed CLI | Built and smoke-tested locally; no runtime dependencies |
| Linux/macOS/Windows × Python 3.11/3.14 CI | Authored; not_run: no GitHub runs registered; dispatch reports workflow absent on default branch |
| Windows secure record storage | Unsupported: explicit exit 3; no unsafe fallback |
| Fourteen planning scenarios | Authored good/bad fixture replay; semantic expectations are not model evaluation |
| Independent real-model audit/usefulness evaluation | not_run; no authenticated isolation, human scoring, model budget or spending permission |
| Actual user adoption | None claimed; synthetic approval fixtures exercise mechanics only |
| Model usage, latency, token/billing gains, superiority | Unmeasured; no numeric quality/cost claim |

Remaining: bootstrap/run cross-platform CI through an authorized default-branch
workflow publication; qualify Windows storage before claiming native Windows
workflow support; externally authorized blinded multi-project usefulness
evaluation; optional Lore schema adapter and approved-contract export (P1).
No release tag/package publication or merge has been authorized/performed.

Engineering results apply to tested local POSIX operations. There is no claim
of network-filesystem locking, owner-resistant tamper authentication, universal
power-loss durability or semantic completeness from structure/hashes.
