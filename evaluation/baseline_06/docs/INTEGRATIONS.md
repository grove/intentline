# Optional peers

Normal commands never execute Git, a model, Proofline, Lore, P2P, tests, or a
shell. All peers can be absent. Export creates files only when requested.

`export --format proofline-direct --out HANDOFF` produces exact `source.md`,
stable-ID table `brief.md`, canonical `contract.json`, original source manifest,
individual captures and a final completion marker with every output hash.
It is always a preview/advisory direct brief; an operator assertion does not
become Proofline approved-contract authority. Proofline uses `--source`/`--brief`
on its independently authorized delivery path. Intentline does not run it.

The boundary is one original request. Additional binding contexts require an
explicit `--product-root /exact/downstream/checkout`; their relative paths must
be readable nonsymlink regular files with exact saved hashes. The downstream
checkout must also be clean and contain those references as tracked files:
Proofline independently enforces its clean tracked checkout gate. Intentline
checks file accessibility/hashes, not Git trackedness, without running Git.
Missing/mismatched references fail as unsupported shape. Multiple original
requests, transitive parent chains and runtime prerequisite imports are unsupported.
Evidence gaps remain visibly qualified; material outcome/authority decisions,
adverse audits, stale sources or approval references block export.

`markdown` and `json` formats preserve full canonical contract and all captured
sources too. A directory is complete only with matching `export-manifest.json`;
partial interrupted outputs can be retried with the same identity. Changed exports
need a new output directory; existing files are never overwritten. Output is private
on supported POSIX filesystems. Export only reviewed data to a handoff location.

Proofline compatibility includes exact pinned direct parser and clean tracked
checkout admission controls, complete exported-input identities and downstream
context race rejection. It is not live delivery or model evaluation. See the
source distribution/checkout evaluation/PROOFLINE_HANDOFF.md for read-only
inspection, an operator-run bounded smoke and immutable evidence recording.
No paid execution occurs in normal commands or CI. Live qualification is not_run.
The optional P2P approved-contract exporter is deferred: Intentline assertions
are not authenticated P2P approval and the real approved-contract path has not
been qualified end to end for Intentline.

An experimental read-only [Lore report adapter](LORE_CONTEXT.md) recognizes the
pinned bootstrap schema 1 and initialized schema 5 envelopes. Explicit reports
use existing --context capture, unchanged bytes and unverified authority; no
new prepare flag, peer installation, inference or registry access. The small
inspector reports envelope/identity limits, never binding constraints. Use actual
captured originals for applicable policy and preserve all report qualifications.
No-Lore planning works unchanged; planning benefit is unmeasured.

Native handoff (experimental, offline-qualified): `export --work WORK --format
proofline-native --out BUNDLE [--product-root PRODUCT]` exports a ready input,
never authority. Complete fresh planned evidence, settled decisions and undisputed
current assertions are required, but adoption may be absent. The final
native-manifest.json binds every file, the full current history, original/amended
sources, all necessary ancestors and continuity. Current binding context needs
an exact selected product root. Successors cannot silently fall back to direct
briefs; markdown/JSON exports preserve their archives too.

`inspect-native --bundle BUNDLE --json` validates captured identities without
following historical private origins, writing or executing anything. The exported
`python -I -B BUNDLE/inspect_bundle.py BUNDLE` inspector uses only the standard
library and needs no installed Intentline. POSIX no-follow capability is required.
It reports authorization not_established and consumer_execution not_observed.
The native brief is a deterministic unapproved display of complete canonical JSON.
All file/metadata records are bounded to 2 MiB; total portable payload is bounded
at 44 MiB. Excess refuses without truncation.

Raw audit/approval payloads, actor names, approval paths and references do not
enter native model-visible contexts. Only unauthenticated record/hash qualifications
are included. A separately authorized consumer must validate its own exact
contract/source-chain adoption, current clean product documents, permissions and
candidate receipts. Export/inspection never invokes Proofline or paid inference.

The separate [Proofline native consumer PR #6](https://github.com/grove/proofline/pull/6)
is merged. Current remote consumer main is
`023a3d5a380f4659b4459e585f1910604374d2a7` (12 October 2026); its native validator
is byte-identical to the retained test snapshot at
`2285a434c1c33e73f8d89a6c3267abcaa37e9b95`. Offline compatibility does not qualify
live delivery. Its `inspect-intentline BUNDLE` command reads native
inputs; `deliver --intentline-bundle BUNDLE --adopt-contract-sha256 CONTRACT_HASH
--adopt-source-chain-sha256 CHAIN_HASH --adopt-bundle-sha256 BUNDLE_HASH
--approval-reference ACTUAL_REFERENCE` requires the independently authorized
caller's exact adoption. Never generate that caller assertion from Intentline's
recorded actor, marker, hashes, approved label or exported template alone.
Current binding documents must be regular tracked files matching the clean
product HEAD; deleted, dirty or changed documents stop dispatch. The existing
candidate isolation, review/proof, permission-map and final receipt controls remain
Proofline-owned. Offline fixture roles/receipts do not establish live delivery.

Intentline keeps native original/amendment files separate and declares indexed
combined source displays non-verbatim. No predecessor adoption raw bytes or
private approval-reference text enter native bundles or worker metadata. Its
optional product-root check runs only when explicitly selected. Lore and P2P
remain advisory optional peers; none is a required install or runtime import.

Proofline's current S6 report records a trust gate failure, including one false
acceptance by Proofline. Green consumer CI and the earlier P2P S2 gate do not
resolve that finding or qualify native Intentline delivery. A real native run
requires separately established trust remediation or scoped requalification,
exact trusted-caller adoption, isolation/egress evidence and bounded model/cost
authorization. See the source distribution's evaluation/PROOFLINE_HANDOFF.md.
Intentline does not run or repair the separately owned consumer here.

## Optional 0.4 advisory children

[Portable slice handoffs](SLICING_INTEGRATIONS.md) carry the complete parent and
source chain, whole allocation and integration obligations. They are data for
humans/existing agents. Existing Proofline standalone direct/native paths reject
these bundles; no child adoption adapter or live qualification is supplied.
Neither parent adoption nor a structural plan permits implementation or dispatch.
Lore, Proofline and P2P remain optional, with no runtime dependency or controller.
