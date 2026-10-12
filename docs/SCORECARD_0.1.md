# Intentline 0.1.0 engineering scorecard

This is an initial implementation candidate, not a published release or proof
of model quality. Exact candidate commit and PR status are reported in the
delivery report; validate with `python -B -m unittest discover -v` at that commit.

| Gate | Observed result |
|---|---|
| Offline unit/integration suite | 44 tests pass on local macOS Python 3.11.17, 3.12.14 and 3.14.8; zero skips |
| Source fidelity, quotation and immutable history | Tested positive/negative controls |
| Staleness, source/approval identity, revision invalidation | Tested |
| Cooperative contention, process termination, interrupted recovery | Tested locally |
| No-follow paths, parent identity replacement, traversal/FIFO/size/binary rejection | Tested locally |
| Read-only CLI writes, subprocesses, network | Instrumented refusal tests pass with Python -B |
| Markdown escaping, canonical JSON and seeded round trips | Tested |
| Pinned Proofline direct-input parser | Exact extracted parser, source/brief byte test passes; no live delivery |
| Wheel/source archive, clean install, installed CLI | Built and smoke-tested locally; no runtime dependencies |
| Linux/macOS/Windows × Python 3.11/3.14 CI | All six jobs pass at `f248209baad4b6eabddf2aa8955927da486c22cd`: [qualification run](https://github.com/grove/intentline/actions/runs/38225370119). Final merge checks are recorded separately in the delivery report |
| Windows secure record storage | Unsupported: explicit exit 3; no unsafe fallback |
| Local Python 3.11 | 44 tests pass using isolated Python 3.11.17; the original broken installation was left untouched |
| Fourteen planning scenarios | Authored good/bad fixture replay; semantic expectations are not model evaluation |
| Independent real-model audit/usefulness evaluation | not_run; no authenticated isolation, human scoring, model budget or spending permission |
| Actual user adoption | None claimed; synthetic approval fixtures exercise mechanics only |
| Model usage, latency, token/billing gains, superiority | Unmeasured; no numeric quality/cost claim |

Remaining: qualify Windows storage before claiming native Windows
workflow support; externally authorized blinded multi-project usefulness
evaluation; optional Lore schema adapter and approved-contract export (P1).
Merges are authorized; exact merge status is recorded in the delivery report.
No release tag or package publication has been performed.

CI is now registered on the default branch, and manual dispatch works. The first
bootstrap run failed because packaging referenced skill files introduced by later
packages; repair PR #8 corrected those entries before subsequent packages merged.
The failed run remains historical evidence and is not counted as a pass.

Engineering results apply to tested local POSIX operations. There is no claim
of network-filesystem locking, owner-resistant tamper authentication, universal
power-loss durability or semantic completeness from structure/hashes.
