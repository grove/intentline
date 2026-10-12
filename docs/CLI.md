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
