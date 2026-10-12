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

Lore's pinned bootstrap schema 1 and initialized schema 5 were inspected in
V09, SHARED_INTELLIGENCE and AGENT_INTEGRATION. The P1 Lore adapter is deferred.
You may explicitly select an ordinary generated report using `--context`;
its bytes remain unverified advisory source content. No Lore-specific schema
interpretation, inference, database access, init/update or policy promotion is
claimed. A semantic agent must preserve revisions, provenance, exceptions,
omissions and fallback qualifications; missing original evidence is a lead/gap.
