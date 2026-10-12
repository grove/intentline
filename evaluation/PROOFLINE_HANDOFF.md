# Direct handoff qualification

Pinned consumer: grove/proofline c4d28e4e743adbb261552323e694946f1360a129,
remote main rechecked 2026-10-12. Consumer docs qualify macOS, Python 3.11+,
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
Native Intentline approval interoperability needs a separate consumer RFC, actual
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
