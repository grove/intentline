# Development and qualification

Python 3.11+ standard-library runtime, no peers/models/credentials needed.
Select a supported interpreter explicitly; macOS system python3 may be too old.

```
python -B -m unittest discover -v
python -m pip install build
python -m build --outdir /private/new-dist
python -B evaluation/package_smoke.py /private/new-dist
```

Build is optional developer tooling, not a runtime dependency. Package smoke uses
fresh temporary virtual environments, installs wheel and sdist, resolves every
installed skill/docs/schema link, checks all command help/version/dependencies and
runs the public manual fixture (Windows must refuse storage with exit 3). Building
or isolated sdist install may fetch setuptools/build tools, never paid inference.
Use a fresh artifact directory. CI runs this plus the offline suite on Linux,
macOS and Windows, Python 3.11/3.14, at every final PR head.

0.2 dependency order: baseline/evaluator → one-request skill → semantic probes →
direct handoff → optional Lore report input → integration. PRs are stacked until
merge authorization; append-only repairs preserve prior heads and failed runs.
No force-push, automatic merge/tag/release or workflow dispatch is required.

Original 0.1 fixtures/tests/scorecard are retained. Baseline evidence and
not_run receipts are byte-preserved in Git; do not normalize/rewrite them.
Optional evaluation/handoff tooling is in the source distribution/checkout,
kept off normal CLI paths. The experimental Lore envelope inspector is packaged.

Evaluation report commands read only, never launch agents, tests, Git or inference.
Do not put private pilot source/gold/outputs in this repository. All public probe
records are authored development mechanics; they cannot be counted as real-model
quality. Record failed/refused/interrupted attempts, null unknown usage and exact
subject identities. Full protocol, rubric and failure ledger are under evaluation/.

Installed-host smoke can use the current agent via direct-file entry without
creating a new model process. Label it self-context/unblinded and separate it from
eligible real pilots. No automatic host discovery/slash-command qualification.
Live Proofline qualification requires its independently authorized native host,
model budget and actual receipts; the operator recipe never runs in CI.

## 0.3 integration

Dependency order: review/baseline → successor lineage → agent flow → native
export → separate Proofline adapter → Windows feasibility → integration.
The Intentline PR stack is open; the consumer PR targets Proofline main.
Exact heads and CI links are in SCORECARD_0.3.md and the final PR report.
No main integration or merged-head CI is claimed before authorized merges.

The final package smoke also exercises installed original review, explicit
amendment, continuity reconciliation, native export and isolated standalone
inspection using authored public fixtures. All previous source/schema/hash
snapshots remain unchanged in evaluation/baseline_02 and the original tests.
Windows tests actually run the limited native handle/API feasibility probe; all
record commands still refuse storage before I/O. See WINDOWS_STORAGE_FEASIBILITY.

The test-only pinned Proofline validator is excluded from the runtime wheel and
retains provenance in tests/compatibility/native-identity.json. It proves offline
admission compatibility; it is neither runtime coupling nor independent review.
The 0.3 host smoke is self-context/unblinded, using installed files and the
current agent only. No paid inference, external pilot or live delivery is implied.
