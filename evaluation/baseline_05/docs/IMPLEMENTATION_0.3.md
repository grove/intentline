# Intentline 0.3 implementation report — 12 October 2026

All seven packages are implemented in separate open PRs. The engineering release
candidate is 0.3.0; main integration and publication await explicit authorization.
Exact earlier heads and push/PR CI are in [SCORECARD_0.3](SCORECARD_0.3.md).
The final integration head/CI are bound in its PR description after commit; a
repository report cannot include its own hash. The separate Proofline consumer
head is `2285a434c1c33e73f8d89a6c3267abcaa37e9b95` in
[Proofline #6](https://github.com/grove/proofline/pull/6).

Original main identities, package PRs and dependency order are pinned in that
scorecard. Intentline package branches are implement/03-01-review,
implement/03-02-successors, implement/03-03-agent-flow,
implement/03-04-native-export, implement/03-06-windows-feasibility,
implement/03-07-integration. Proofline uses implement/intentline-03-native against
its own main. No unrelated work was overwritten, no force-push or merge performed.

## Delivered behavior

- `review` displays full current contract, exact source streams/support state,
  gaps/disputes, old/new identities and mechanical before/after fields. Matching
  rows/IDs do not establish semantic equivalence. `approval-request` is a
  deterministic unapproved template with blank external actor/reference/decision.
- `amend-source` freezes original request and every older exact amendment,
  captures the new amendment and explicitly selected current context, and seals
  bounded full ancestor history. `--refresh-context` requires an actual source
  change/replacement without fabricating new user intent. Historical approvals
  never transfer, including an A→B→A reversion.
- `reconcile` validates a separate bound continuity record covering every old
  obligation and every new R ID, before publishing the initial successor pointer
  last under one lock. Changed/retired request obligations require current
  amendment support; documentary changes require current context. Aliases,
  missing mappings and partial publications refuse. Advisory evidence availability
  can change without changing a binding outcome; a gap still blocks ready native
  export. Semantic applicability remains a human/agent audit duty.
- Planning/audit skills handle these stages internally, preserve full streams,
  accepted scoped exceptions/exclusions, and distinguish evidence gaps from
  unsettled behavior. No automatic adoption or mandatory extra model stage.
- `export --format proofline-native` creates a bounded versioned portable full
  contract/source/history/continuity payload, canonical display and standalone
  stdlib inspector. `inspect-native` reads offline. File inventories, references,
  lineage, duplicates, traversal, tampering, symlinks and pre-marker mutations fail
  closed. Export declares authorization not_established and carries no raw private
  approval reference or downstream execution verdict.
- The separately owned Proofline adapter reads native input without importing
  Intentline or executing exported inspector code. Native admission requires
  actual trusted-caller exact contract/source-chain/bundle adoption and current
  clean tracked documentary context before host/model dispatch. Complete inputs,
  canonical scope and permission map are frozen with existing candidate isolation;
  final status rechecks candidate, adoption, all native receipts and input identity.
  Omitted/invented scope, stale candidate/inputs or fabricated approval labels
  fail. Raw external reference stays host-protected; model metadata gets a digest.
- Windows has a factual native API feasibility probe plus no-I/O refusal controls,
  not a qualified storage backend. See [the NO-GO report](WINDOWS_STORAGE_FEASIBILITY.md).

The acceptance schema stays 1; original source manifests stay 1 byte-for-byte.
Only new successors use source-manifest 2. Continuity and native handoff are
separate versioned records. No migration or runtime dependency is added. Existing
Markdown/JSON exports and original-work direct Proofline briefs remain compatible;
successor direct export explicitly refuses rather than mislabeling concatenated
request fragments. Native consumer remains experimental pending merge/live evidence.

## Reproducible engineering checks

From Intentline checkout, select a supported Python 3.11 or 3.14 interpreter:

```sh
python -B -m unittest discover -s tests -q
python -m build --outdir /private/fresh-dist
python -B evaluation/package_smoke.py /private/fresh-dist
python -B -m evaluation.planning_02 report evaluation/results/planning-03-not-run.json --private-root evaluation
```

Locally used `/opt/homebrew/opt/python@3.14/bin/python3.14` (3.14.8) and isolated
`/private/tmp/intentline-python/cpython-3.11.17-macos-aarch64-none/bin/python3.11`.
Each final suite has 86 tests, one Windows-only probe skip on macOS. Frozen
baseline identity SHA-256 is
`34ae4932a6d91b3806188f9ba6262582cda09f90a64446dc80f35d613ee00be4`;
all 60 original 0.2 tests and their snapshots are retained. Package smoke creates
fresh wheel/sdist environments, checks CLI/help/version/links/schema/dependencies,
and exercises installed original→successor→native workflows with zero models.
Installed current-agent host smoke is a separately retained self_check with bound
public source/contract/map files, zero adoption/audit assertions and unknown usage.

From the isolated Proofline checkout:

```sh
python3.14 -B -m unittest discover -s tests -q
PROOFLINE_NATIVE_TESTS=1 TMPDIR=/private/tmp python3.14 -B -m unittest discover -s tests -q
```

Default: 81 tests, 76 passed/5 skipped. Actual opt-in macOS native security:
81 tests, 79 passed/2 Linux-only skips. All three fixed oracle controls also pass.
Offline roles/receipts are authored fixtures, not actual independent reviews.
The shared validator ancestry is attributed, never claimed independently written.
Both repositories' full CI runs only offline checks, no hosted inference/effects.
Failed engineering runs and repairs remain in the appended failure ledger.

## Measured outcomes and remaining limits

Real planning pilot: not_run; zero eligible tasks and assignments, no completed/
failed/refused/timeout/interrupted real arm attempts, no blinded scores. The new
registration binds the 0.3 arm while 0.2 evidence stays immutable. Actual task,
distinct checker/two additional reviewers, matched authorized pinned models,
qualified isolation and blind scorer provenance are unavailable. Quality, cost,
latency and comparative benefit remain null/unmeasured. Holdout is untouched.

Live native Proofline delivery/review/proof/status: not_run, separately dated;
no task-specific spending authorization, actual caller adoption or qualified live
candidate/receipt chain exists. No paid inference initiated. Hashes identify bytes,
not people, review independence, semantic completeness or effect permission.

Windows storage remains unsupported (exit 3 before I/O). Green Windows jobs
qualify installation, refusal and the narrow actual Win32 handle/API probe, not
secure record creation. POSIX qualification covers cooperative local-filesystem
writers; owner-resistant tamper, network filesystems and power-loss durability
remain unqualified. Limits refuse excess without truncation: 64 active sources,
2 MiB/file, 8 MiB active sources, eight ancestors and 32 MiB unique archive bytes.

No Lore/P2P controller, model client, hosted service, automatic authentication,
GitHub synchronization, implementation or proof execution was added to Intentline.
No main merge, merged-head CI, tag, GitHub release or PyPI publication is claimed.
The smallest next step is review plus explicit merge authorization, followed by
actual merged-head CI. Pilot and live native qualification require their separate
real participants, bounded execution authorization and receipts.
