# CLI contracts

`python -B -m intentline` and installed `intentline` accept the same commands.
Use Python 3.11+. `--json` works before or after the subcommand. Each operation
emits one `intentline.result`, schema_version 1 object on stdout:
`command`, `ok`, and `data` for a result; `error: {code, message}` for a diagnosed
failure. Data-bearing status/check/render failures use `ok:false`, data.exit_code
and the process status. Diagnostics are stderr. `--help` uses ordinary argparse
help text even with --json; no filesystem access is needed.

| Command | Required options | Effect |
|---|---|---|
| prepare | --source FILE or -, optional repeated --context FILE, --root ROOT, --out DIR | Capture only explicit inputs |
| propose | --work DIR --draft FILE | Validate and record immutable revision |
| check / status | --work DIR | Read structure, identity and derived flags |
| render | --work DIR, optional --format markdown | Print deterministic view |
| audit-record | --work DIR --report FILE | Bind unverified external audit |
| adopt | --work DIR --expected-contract-sha256 HASH --approval-file FILE | Record explicit operator assertion |
| export | --work DIR --format proofline-direct/markdown/json --out DIR, optional --product-root ROOT | Write advisory handoff |

Prepare defaults: root = current absolute directory, out =
`.intentline/work/request`. Select a different slug for each source identity.
Do not use traversal, dot path components, symlinks, Windows-style paths, NUL,
control characters or ambiguous repeated separators. Inputs: 64 files, 2 MiB
each, 8 MiB total, regular UTF-8. Stdin has no live origin and is explicitly
frozen, not claimed freshly retrieved from an external source.

Exit 0: completed valid operation. Exit 2: invalid/stale/blocked/not-ready input.
Exit 3: operational corruption or unavailable secure filesystem capability.
An evidence gap does not itself block structurally valid planning; material
outcome/authority decisions and adverse audits do. Source changes invalidate
adoption and exports; saved snapshots remain historical.

Read-only CLI logic writes no records, locks, migrations or caches and executes
no commands/network calls. Use `python -B` or PYTHONDONTWRITEBYTECODE=1 to also
suppress interpreter import-cache creation, including before CLI initialization.

Mutations use exclusive `.writer.lock`, sibling stages, fsync and atomic writes.
A killed writer can leave a lock/stage/immutable orphan. Confirm termination
before manually removing its lock; rerun identical inputs to complete publication.
No automatic lock stealing. Existing completed outputs/records are not overwritten.
Existing output directories must already be owner-only; public directories are
refused without changing their permissions. Newly created directories use 0700
and record files 0600, subject to the owner's stricter process umask.
Guarantees cover cooperative Intentline writers on ordinary local POSIX
filesystems. Owner-level hostile edits, network filesystem semantics, power-loss
durability and unsupported Windows primitives are not authenticated/qualified.

`review --work WORK [--against-revision N]` reads the full agreement, source
bytes, audit reports and a mechanical diff (IDs, full changed rows, constraints,
exclusions, decisions and evidence gaps). A first revision has no predecessor.
Matching rows/IDs do not establish semantic equivalence. Reads write nothing.

`approval-request --work WORK --json` returns that exact display and a deterministic
unapproved template with blank actor/timestamp/reference fields. An external
actor supplies actual authority through existing `adopt`; viewing never adopts.

`amend-source --work OLD --amendment FILE --root ROOT [--context FILE ...]
--out NEW --expected-contract-sha256 HASH` captures a distinct successor. Choose
`--refresh-context` instead of `--amendment` for changed/replaced selected context.
Historical context is archived, never presumed current. All current context must
be explicitly selected. Original and amendment bytes remain separate.

`reconcile --work NEW --draft FILE --continuity FILE` binds the initial schema-1
contract and strict continuity schema 1, publishing current.json last under one
writer lock. `propose` still handles later same-source revisions. Successors need
new external adoption; old assertions never transfer, including A→B→A reversion.

`export --format proofline-native` creates an experimental ready native input with
full contract/source/continuity history and protected provenance hashes. It is
inspectable without adoption; its authorization is always not_established.
`inspect-native --bundle DIR` is read-only, offline and requires no peer. A ready
native plan cannot retain evidence gaps; advisory direct export for supported
original work keeps its existing gap semantics. Successor direct handoff refuses.

Windows 0.3 secure storage remains NO-GO: every record operation returns exit 3
before filesystem activity; help/install do not qualify storage. The actual Win32
handle probe in CI is a narrow feasibility observation only. See
[feasibility and missing security gates](WINDOWS_STORAGE_FEASIBILITY.md).

## Optional slice commands (0.4)

| Command | Required options | Effect |
|---|---|---|
| slice preview | --work WORK --proposal FILE | Read-only structural allocation check |
| slice record | --work WORK --proposal FILE --expected-parent-sha256 HASH | Explicit immutable advisory recommendation |
| slice status / render | --work WORK | Read-only applicability/history/disputes |
| slice audit-record | --work WORK --report FILE | Optional unverified report capture |
| slice impact | --work OLD --successor-work NEW | Read-only verified lineage comparison |
| slice export | --work WORK --child S1 --out PRIVATE_DIR | Explicit data-only child snapshot |
| slice inspect | --bundle DIR | Offline data inspection; no bundle script execution |

`--json` works before slice, between slice/action or after the action. The existing
result schema 1 and exits are unchanged. States are NO_PLAN, NO_SPLIT, SPLIT_PROPOSED,
STALE_PARENT or BLOCKED, never approval/proof/consumer readiness. Preview includes
the advisory candidate. Status exposes exact current and recorded parent identity,
plan digest, history_count, freshness and retained unverified disputes. Render
escapes source data in an indented JSON view. See [schema and bounds](SLICING.md).
An old work directory cannot discover future successors automatically; select the
current parent explicitly and use impact to compare archived lineage.
