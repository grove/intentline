# Intentline 0.5 implementation handoff

12 October 2026. This report separates feasible engineering from unavailable
independent empirical work. The user authorized commit, push and five focused PRs. Those effects are complete;
Experimental 0.5.0rc1 source preparation and qualification followed the initial
exact-head engineering CI gate.
No paid inference, new scoring framework, coding-agent controller, participant
impersonation, fabricated approval, merge or tag/package release was performed.

## Baseline and effect boundary

Starting main:
`587ef061287f02d4d7328f7c291bf57b85892603` (Intentline 0.4.0).
Remote main was fetched/rechecked and matched. No open Intentline PR was observed.
Baseline local suite: 120 tests on Python 3.14.8 and standalone 3.11.17, 119 pass
and one actual-Windows API probe skip on macOS. Exact baseline CI
[38258294929](https://github.com/grove/intentline/actions/runs/38258294929) passed
all six OS/interpreter cells. No GitHub Release was observed; PyPI publication
was not verified.

The user approved publishing the five concrete review units. They are stacked in
dependency order, with no merge, force push, tag/package release, inference or
participant outreach authority. The original exact review heads are:

| Unit | Initial commit | PR | Exact-head CI |
|---|---|---|---|
| 01-readiness | `149acde9e797c33a525caa0c829d2f5c89919526` | [26](https://github.com/grove/intentline/pull/26) | [six cells passed](https://github.com/grove/intentline/actions/runs/38274554042) |
| 02-workflow | `5ae1927647e1a99c9f01f9b141f82b9a28f7bad7` | [27](https://github.com/grove/intentline/pull/27) | [six cells passed](https://github.com/grove/intentline/actions/runs/38274553731) |
| 04-native | `711dd8ca9642b473e8912ace60720a178a8007d3` | [28](https://github.com/grove/intentline/pull/28) | [six cells passed](https://github.com/grove/intentline/actions/runs/38274552760) |
| 05-slicing | `7b41bf982d1a8c4940bc1d7e285549a8a15a0030` | [29](https://github.com/grove/intentline/pull/29) | [six cells passed](https://github.com/grove/intentline/actions/runs/38274552919) |
| 06-integration | `46d45d760f22a39930647dc531aba48b09f216ac` | [30](https://github.com/grove/intentline/pull/30) | [six cells passed](https://github.com/grove/intentline/actions/runs/38274553937) |

PR #30 also contains subsequent RC/report qualification commits. Its current
head and checks are available on the PR; a report cannot embed its own commit
identity. The original preparation receipt remains dated and byte-preserved;
engineering-05-publication.json records actual observed initial CI metadata.
Experimental RC commit `756e9560ca5afd3373fcf881b4838d1880a89b21` passed [all six cells](https://github.com/grove/intentline/actions/runs/38275126589).
engineering-05-rc-qualification.json records that observed qualification; later
report-only heads are checked separately on PR #30. No review was submitted or
approval invented.

## Work-package delivery and review boundaries

| Package | Delivered | Paths / proposed review unit |
|---|---|---|
| 01 study readiness | Frozen 0.4 code/skills/docs/schema and representative source/CLI/native/child bytes; existing-validator privacy/chronology fixes; private source research and intake preflight | evaluation/baseline_05, intake_05.py, INTAKE_05.md, planning_02.py, slicing_04.py; new baseline/intake/study-guard tests; distinct planning registration/readiness receipts |
| 02 actual user path | Supported whole-tree direct-file entry retained; stale current merged-code guidance corrected; real first-use protocol and expanded installed manual controls | README, docs/AGENT_GUIDE.md and DEVELOPMENT.md; evaluation/USABILITY_05.md and package_smoke.py |
| 03 conditional semantic correction | No genuine development model outputs or reviewed planning failures available; no semantic skill tuning or dummy PR | Three skills and semantic-probes.json unchanged; mechanical failures appended to FAILURE_LEDGER; triage/holdout protocol in INTAKE_05.md |
| 04 native readiness | Current consumer/authority pin, S6 trust stop, guarded operator recipe, retained unverified evidence semantics and additional negative controls | docs/INTEGRATIONS.md, evaluation/PROOFLINE_HANDOFF.md, handoff_02.py, consumer/native not_run receipts, tests/test_handoff_05.py |
| 05 slicing preparation | Existing evaluator/rubric reused; distinct empty development registration, source-bound provisional parents privately; diagnostic NO SPLIT/SPLIT policy | evaluation/SLICING_05.md, cases/registration_slicing_05.json, results/slicing-05-not-run.* |
| 06 integrated QA/report | Preserved contracts/security/historical bytes, expanded package/privacy checks and CI receipt commands; independent decisions | MANIFEST.in, .github/workflows/ci.yml, new public readiness tests, this report and SCORECARD_0.5.md |

All five review units are committed/pushed and unmerged. Their original exact
heads passed the six-cell CI matrix. No empty conditional semantic-correction PR
was created. No other repository was modified. No local peer dirty changes
were used as a released consumer qualification.

## Reproducible engineering evidence

The 0.4 freeze uses main's exact Git blobs and retains original output bytes, not
normalized copies. `evaluation/baseline_05/identity.json` inventories source files
and hashes all prior baselines, results, registrations, original tests and historical
scorecards. Its authored capture inventory binds original request/contract, CLI
schema-1 status/render/review/approval-request outputs, slice status and portable
native/child exports. Ephemeral source origins in these historical captures may
no longer exist; tests compare retained bytes and portable payloads, not a claim
of current origin freshness. Original live-source staleness tests remain intact.

Reproductions before repair showed renamed reference/review content leaking through
dictionary-equality checks, cross-task/instruction leakage and invalid review/scoring
chronology. The new four-test adversarial suite had nine failing subcases before
repair; after repair the 12-test combined evaluator suite passed. Actual new guards
run through planning_02.validate/assess and slicing_04.validate/assess, not a replacement
evaluator. The nearest valid/no-effect controls and unknown-usage/not_run accounting
still pass. Structural hashes cannot detect semantic, partial or encoded answer
leakage; external isolation and independent source review remain required.

Handoff focused validation: 22 tests passed, covering native originals/successors,
adoption/staleness, tracked checkout/context races, child refusal, rehashed omission
against exact adoption, immutable assertion retention and trust-stop usage/coverage.
An opaque fake proof PASS remains authentication unverified. Intentline does not
interpret that as authenticated proof or replace the consumer's final status.

Final full suite: **136 tests on each of Python 3.11.17 and 3.14.8; 135 pass,
one actual-Windows probe skipped on macOS**. Both fresh wheel and fresh sdist
install/manual workflow controls passed on both interpreters. After the original
committed heads passed all six remote CI cells, source
package metadata was set to experimental 0.5.0rc1. The RC passed the same local
suites and fresh wheel/sdist workflow controls on both interpreters, then all six
exact-head CI cells. No distribution was published. Installed
controls cover whole skill links, no context, permitted docs, missing harness as a
gap, material open decision, original source bytes, stale changed source, unchanged
revision/hash reuse, read-only file inventory, successor review, NO SPLIT/SPLIT,
portable native/child inspection and child refusal at the standalone native boundary.
No runtime dependencies were introduced. Final artifact SHA-256 and build/privacy
receipts are in the operator's ignored `.intentline/05/final-qualification.json`, outside
the distribution to avoid self-referential artifact hashes; the final response
reports them. The retained local logs under ignored `.intentline/05` include
baseline, failing guard controls, repaired focused suites and interpreter failures.
Never convert an unexecuted final CI job to passed. Initial per-unit committed
archives also passed 131, 131, 134, 134 and 136 tests respectively on macOS/3.14.8,
each with the actual-Windows probe skip. Applicable validation commands:

```sh
python -B -m unittest discover -v
python -B -m evaluation.planning_02 report evaluation/results/planning-05-not-run.json --private-root evaluation
python -B -m evaluation.slicing_04 report evaluation/results/slicing-05-not-run.json --private-root evaluation
python -B -m evaluation.intake_05 /private/study/intake.json --private-root /private/study
python -m build --outdir /private/fresh-dist
python -B evaluation/package_smoke.py /private/fresh-dist
```

The ambient Python 3.9 is unsupported; its relocated Python 3.11 shim also fails
before importing encodings. A working standalone 3.11.17 was located, without
system edits. Final local qualification uses that and Homebrew 3.14.8. Exact-head
Linux and actual Windows CI passed; Windows passed the
existing secure refusal controls, without qualifying record storage. Initial
integration CI logged 136 unittest methods per cell: POSIX 135 pass/one skip,
Windows 136 pass with POSIX record operations refusing or returning before I/O.
Green Windows jobs do not demonstrate the unsupported POSIX workflow on Windows. Windows continues exit 3 before
record I/O; no insecure storage fallback or rushed backend was added.

## Available task and user evidence

Private study root (operator handoff only): owner-only directory outside the public
repository, with separate restricted gold/review/outcome paths. No independent
gold/reviewer/outcome captures exist. Public receipts contain aggregate counts and
digest bindings, no private requests, actor names, answer keys or model transcripts.
The operator's private intake lists every numbered candidate and missing artifact.

Eleven upstream requests were captured across three projects at full commit pins;
two originals explicitly disclosed AI authorship and were retained as rejected.
Nine selected candidates remain unreviewed. Each retains exact issue JSON/API-body
UTF-8, comments/chronology, pinned original context, license bytes and retrieval
metadata with SHA-256. The raw upstream request and any exposed solution remain
research evidence, not independent gold. Historical source suitability, accepted
policy versus issue proposal and issue-prose license rights require external review.
Four agent-authored parent drafts preserve complete original source streams and
pass the existing native-parent parity validator; no parent is independently
eligible or adopted. Five candidates still lack a provisional parent.

Actual preflight: candidate_count 9, project_count 3, eligible_count 0,
registered_assignments 0, executed 0, missing authors 9, missing checkers 9,
missing independent task/gold reviews 9. Model authorization, host isolation,
blinding and cost permission are missing. Each eligible future task needs all three
planning/slicing assignments; 27 is a **future target**, not an existing assignment
population. There were no real failures/refusals/timeouts because no study attempt
was authorized; future adverse attempts must be retained. Cost/tokens/elapsed/user
burden and comparative findings remain null/unmeasured. No untouched holdout exists.

The P2P planning-only source is pinned at
`17f3deb982a8224f71b12bda74be6b24d86571e4`, skill SHA-256
`29b32d7c0fd72e44bf878dc346f194a40ea0d1fea43f34946b4d3aeed24c6e02`;
slice-contract SHA-256
`de3c8238c0f19f462853876ec0d8577aeb9f0a8b79ef9df76420f94020014976`.
Remote originals were captured; a differing local peer revision was not substituted.
No P2P controller, issue publication or delivery was invoked. The normal manual/agent
entry reuses existing commands and skills; no new path resolver/controller was
needed. Existing host smoke is self-context/unblinded. New 0.5 installed-agent and
real consenting first-use observations are not_run; the prepared observer protocol
separates preparation/install/reads/repairs/audits and actual user effort.

## Consumer trust and authority

Proofline remote main: `023a3d5a380f4659b4459e585f1910604374d2a7`.
Its native validator hash remains
`977a4f24cd1724c780c1a09155d467ae2b34a91ed76f02e14d4d0345cc7838cd`,
byte-identical to the old retained test-only consumer; no blind snapshot update.
PR #6 is merged at `5ab3ff193f3d5d665645d704d9d6d7e410865b91`.
The pinned consumer's S6 report states TRUST GATE FAILED: 69/120 executed,
51 retained unexecuted and one Proofline false acceptance. This producer records
those published findings without claiming to authenticate the private empirical
evidence. No merged independent remediation/scoped native qualification was
observed. Green consumer CI does not lift the gate.

Native live status: blocked_trust_gate. Missing trusted-caller exact adoption,
independently qualified host/isolation/egress and bounded model/time/dispatch/cost
grant also remain blockers. Candidate/reviewer/prover/native final-status receipts
do not exist. The operator recipe is permission-safe preparation, not execution
authority. Child bundles remain advisory/unsupported and cannot prove their parent.
The recorder retains opaque completed assertions unverified; it never establishes
independence, caller authority or behavioral proof from approval prose/PASS.

## Separate release decisions and next step

Engineering: **experimental source RC 0.5.0rc1 qualified for review**. Original
review heads and the RC passed all six CI cells and offline/package checks.
No main merge, tag or package publication is authorized. Review
readiness and empirical usefulness remain separate decisions.

Empirical: unmeasured / blocked_external; observed-usefulness objective unmet.
External accountable task/reference authors, two task/gold reviewers, two blinded
output scorers, historical suitability/license review, actual isolation/settings
and bounded inference grant are required for a genuine diagnostic pilot. Native
consumer trust qualification is an additional independent stop. No superiority,
savings or safely verified live native result is claimed.

The remaining engineering steps are final report-head CI and independent review. Merge
and tag/package publication require separate authorization. The next empirical
action is independent private intake review; no model spending is required merely
to identify missing artifacts. Inference and participant outreach remain separate
effects.
