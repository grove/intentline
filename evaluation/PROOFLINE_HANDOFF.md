# 0.5 native trust gate and operator handoff

Current remote Proofline main, rechecked 12 October 2026:
`023a3d5a380f4659b4459e585f1910604374d2a7`. Native consumer PR #6 is merged.
Its `checks/intentline_input.py` is byte-identical to the retained test snapshot:
SHA-256 `977a4f24cd1724c780c1a09155d467ae2b34a91ed76f02e14d4d0345cc7838cd`.
No snapshot refresh was needed; runner/status/trust qualification is separate.
The local peer checkout's uncommitted follow-up work was not used as qualification
or changed. The sanitized consumer pin is in results/proofline-consumer-05.json.

**Live gate: blocked_trust_gate.** The current
[S6 report](https://github.com/grove/proofline/blob/023a3d5a380f4659b4459e585f1910604374d2a7/docs/S6-RESULTS.md)
reports 69/120 assigned runs executed, 51 unexecuted and one false acceptance by
Proofline. These are consumer findings, not an observed Intentline defect. The
consumer's green CI and earlier P2P S2 result do not remediate S6 or qualify an
Intentline native run. No merged trust remediation or separately scoped native
verification qualification was observed; no live run was attempted.

## Required independent gates before any native run

1. Establish consumer trust remediation or scoped verification qualification that
   addresses the S6 false acceptance; preserve its independent source/behavioral
   evidence and exact consumer revision. A commit/tag/unit pass alone is insufficient.
2. Inspect the entire standalone original/amended request, canonical contract,
   constraints/exclusions and lineage. Obtain actual trusted-caller adoption of
   **exact contract, source-chain and bundle hashes**. Intentline ADOPTED_ASSERTED,
   an approval label, template, source prose or agent-authored assertion cannot
   supply it. Raw adoption/approval records remain private.
3. Qualify the actual native host, Codex CLI/model/reasoning, credentials and
   isolation/egress boundary under Proofline S0. Earlier docs name macOS,
   Python 3.11+, Git and Codex CLI 0.162.1; other versions require fresh qualification.
4. Obtain a bounded task-specific model/time/dispatch/cost grant. Keep a clean
   tracked local test product containing exact current binding documents. No
   publication, PR, merge, deployment or remote target is authorized by this recipe.

## Read-only preparation and separately authorized command

Export only when requested and inspect without following private historical
origins or executing the exported inspector at consumer admission:

```sh
python -B -m intentline export --work /private/work --format proofline-native \
  --out /private/native --product-root /absolute/clean/product --json
python -B -m intentline inspect-native --bundle /private/native --json
python -B /absolute/pinned-proofline/proofline.py inspect-intentline /private/native
```

Omit product-root only when no binding current project documents require it.
Inspection reports authorization not_established and execution not_observed.
After **all** gates and grants exist, the operator may run one bounded local-only
diagnostic, substituting the actually authorized values (these are not grants):

```sh
python -B /absolute/pinned-proofline/proofline.py deliver \
  --repo /absolute/clean/product --intentline-bundle /private/native \
  --adopt-contract-sha256 EXACT_AUTHORIZED_CONTRACT_HASH \
  --adopt-source-chain-sha256 EXACT_AUTHORIZED_CHAIN_HASH \
  --adopt-bundle-sha256 EXACT_AUTHORIZED_BUNDLE_HASH \
  --approval-reference 'Actual privately inspected caller adoption reference' \
  --map 'Task-specific public seams and permitted verification commands' \
  --seconds 900 --stage-seconds 240 --verification-reserve 120 \
  --dispatches 3 --output /private/new-native-attempt
python -B /absolute/pinned-proofline/proofline.py status /private/new-native-attempt/report.json
```

Do not execute this before trust qualification or infer a budget from these example
limits. Do not combine native input with --source/--brief/--contract or fall back
when it refuses. Advisory child S# bundles remain unsupported; child success never
proves the parent. Optional approval-file/hash must be actual externally inspected
bytes. Keep approval references out of public command logs.

Retain every attempt, source/contract/bundle/permission/candidate binding, native
run and final status, actual reviewer/prover receipts, independent behavioral
observations and all adverse findings. Re-inspect input and candidate at final
status. Record missing usage null; a fake role's PASS is not proof. The existing
`handoff_02 record` retains opaque externally supplied assertions **unverified**;
it does not authenticate native receipts or replace consumer status/independent
behavioral verification. It now records blocked_trust_gate, rejects execution
coverage for unattempted states, and requires null unattempted usage. The distinct
results/proofline-native-05-not-run.json records the actual stop without deleting
older results.

Offline controls retain no-adoption, source/contract tampering, swapped brief,
stale successor/adoption, exact-hash missing-exclusion refusal, forged assertion,
child rejection, native/no-fallback and dirty tracked checkout cases. Candidate
and counterfeit-role controls remain consumer-owned; our opaque fake-PASS retention
test explicitly proves that a retained assertion stays unauthenticated. These
tests do not substitute for a positive native host/candidate/review/proof receipt.

## Historical direct qualification (0.2; retained context)

Pinned consumer: grove/proofline c4d28e4e743adbb261552323e694946f1360a129,
the 0.2 observation; it is not today's remote main. Consumer docs qualified macOS, Python 3.11+,
Git and Codex CLI 0.162.1 with real authentication and native isolation. Other
host/CLI versions need Proofline S0 qualification before inference. Local peer
checkouts may be newer; never substitute their head without revalidation.

Offline controls: export/inspect match exact request bytes, full source manifest,
all captures, current canonical contract, stable unique R IDs and rendered
constraints/unknowns. Marker and every output are bound; partial/tampered/stale
exports fail. Binding context must exist with its exact hash in the selected
checkout. An export race must not publish completion. The pinned consumer's
actual capture_base/validate_links/git_bytes are extracted test-only with full
function/file hashes and Apache attribution. Tests use a clean committed product
with policy/request available as tracked files, compare exact Git trees, and reject
dirty/unsafe inputs. These are admission checks, not host/model/proof qualification.

The inspection command reads only and never invokes Git or a peer:

```
python -B -m evaluation.handoff_02 inspect --work /private/work \
  --out /private/handoff --product-root /absolute/clean/product
```

Record its stdout privately as inspection.json. It deliberately reports live
execution not_observed and requires the consumer's own clean tracked/native gates.
Review original promise/context completeness semantically before dispatch. Parent
and runtime prerequisite imports are unsupported; do not flatten them into direct
input. Intentline DRAFT or ADOPTED_ASSERTED is not a supported approved `--contract`.
At that historical observation native Intentline interoperability needed a consumer RFC, actual
authority/identity support and live positive/negative qualification, not P2P-shaped
Markdown disguising unverified assertions.

## Operator-run live smoke (separate authorization)

Do not run this in CI or merely because credentials exist. Obtain a task-specific
spending/model/time/dispatch grant, real authentication and a qualified native host.
Keep the original product checkout clean with all binding source files tracked.
Pin/read the consumer docs at the recorded revision, inspect the original source
and export, and preserve inspection hashes immediately before launch. Example:

```
python -B /absolute/pinned-proofline/proofline.py deliver \
  --repo /absolute/clean/product --source /private/handoff/source.md \
  --brief /private/handoff/brief.md \
  --map 'Task-specific public seams, required commands and evidence gaps' \
  --seconds 900 --stage-seconds 240 --verification-reserve 120
python -B /absolute/pinned-proofline/proofline.py status /private/run/report.json
```

The pinned S2 consumer bounds dispatches to three. Select an authorized private
output via the consumer's --output flag if needed. Never weaken isolation/egress or
acquire credentials. Retain adverse/interrupted attempts separately and unchanged.
Afterward re-inspect the bundle, preserve native run/status receipts, frozen
candidate commit and reviewer/prover findings, and map every original promise and
constraint to actual observations. Record available tokens/cost/elapsed time;
unknowns stay null. Local acceptance does not authorize publication or merge.

Use `evaluation.handoff_02 record --evidence evidence.json --private-root /private \
--out /private/retained-evidence` to preserve a supplied evidence record immutably.
Fields are demonstrated in results/proofline-not-run.json and tests/test_handoff.py:
state, blockers, bound inspection/external_records, candidate_commit, coverage,
nullable usage. Retention authenticates bytes only; it cannot turn a declared
completed run into verified proof. Do not use it instead of real consumer status
verification. Keep native receipts/source text private.

Current live gate: not_run / blocked_external. No explicit external spending grant,
qualified authenticated native run or independently observed candidate/status
receipts supplied. No cost/latency/delivery benefit claimed.

Integration also ran three focused offline tests from the actual pinned consumer
checkout (unapproved-contract zero-dispatch admission, unique direct IDs, exact
tracked byte/mode/export-ignore capture). Its native inspect_contract rejected
the exported Intentline advisory brief: “Unsupported contract: expected the
current P2P Markdown heading”. No consumer model path was invoked.

0.3 native bundles add a portable inspector and full successor continuity, separate
from the pinned direct compatibility path above. Native offline inspection is
not live delivery, authentication or independent proof. Native consumer qualification
belongs to a separate Proofline PR. No task-specific paid inference grant exists;
the live gate remains not_run. Never auto-degrade a failed native request to direct.
