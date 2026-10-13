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
Current optional Proofline use is check-only with separately authorized commands
and its qualified native host; no extra model/reviewer is required. See
[integration limits](INTEGRATIONS.md). Historical controller qualification and
model-budget recipes remain archived and never run in CI.

## 0.3 integration

Dependency order: review/baseline → successor lineage → agent flow → native
export → separate Proofline adapter → Windows feasibility → integration.
The historical 0.3 and 0.4 stacks are merged. Their dated handoff reports retain
the state observed when written. Current starting main is
`587ef061287f02d4d7328f7c291bf57b85892603`; its six offline CI cells passed in
run 38258294929. Historical Proofline native consumer PR #6 was also merged;
its controller and subsequent S6 trust findings are retained research, linked
from [the handoff archive](../evaluation/PROOFLINE_HANDOFF.md).

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

## 0.5 qualification

Reuse the existing planning/slicing evaluators. `evaluation/intake_05.py` is only
a read-only incomplete-candidate diagnostic; it neither executes nor scores work.
Private intake/source/gold/reviewer/outcome material belongs outside this checkout,
not merely in an ignored public-project directory. See the source distribution's
INTAKE_05.md, USABILITY_05.md and SLICING_05.md. Frozen 0.4 code, skills, docs,
schemas, authored source/CLI/native/child bytes and prior evidence hashes are in
`evaluation/baseline_05`; original records are not normalized or rewritten.

Source/authority/CLI behavior remains compatible. Evaluator repairs now refuse
renamed or cross-task private answer/review leaks and invalid registration order;
handoff retention recognizes a trust stop without inventing execution coverage.
These are offline engineering corrections, not measured semantic improvements.

Use a supported interpreter from a working installation: the ambient macOS
Python 3.9 and relocated 3.11 shim are unsuitable. The standalone 3.11.17 and
Homebrew 3.14.8 were used for local qualification. Store complete failing and
passing logs privately. Before publication, inspect staged filenames/diffs and
distribution inventories for private data. Exact final-head six-cell CI requires
an authorized commit/push/PR; local tests do not replace it. The original five
0.5 heads passed all six cells. Experimental 0.5.0rc1 metadata follows that gate;
subsequent heads require their own checks. Tag/package publication and merge
remain separately authorized, and empirical readiness is independently reported.

## 0.6 qualification

The separate evaluation adapter reuses planning_02 helpers and rubric_02 without
changing formal-study semantics. Historical 0.1–0.5 identities are frozen in
baseline_06; all new fixtures are authored engineering controls. Private source,
gold, model outputs, settings and native receipts remain outside Git. Installed
wheel/sdist qualification includes the optional read-only evaluator, versioned
spec, public controls and sanitized empty receipt. No runtime model dependency.
The package version remains 0.5.0rc1 pending a separate release decision.

Run the ordinary offline suite and fresh build/package smoke above. CI also
reproduces the empty 0.6 report in owner-only temporary storage. It never runs
research/calibration/planning/scoring inference. Actual Windows storage still
refuses with exit 3. See [0.6 implementation](IMPLEMENTATION_0.6.md) for exact
local commands, observed checks and unexecuted remote-CI cells.
