# Optional peers

Normal Intentline commands never execute Git, a model, Proofline, Lore, P2P,
tests or a shell. All peers can be absent. Export creates private files only
when requested; no new export schema, command or runtime dependency is needed.

## Current Proofline support

Proofline supports `check`, `run` and `status`. **Check-only is available without
Intentline:** an existing agent supplies the full original request and selected
executable commands. It requires no acceptance contract, planning audit,
independent AI reviewer/prover or extra model call. `run` is a separate optional
coding attempt, not a required handoff stage.

The optional consumer adapter originally proposed in
[Proofline #23](https://github.com/grove/proofline/issues/23) is now merged in
[PR #27](https://github.com/grove/proofline/pull/27), revision
`32b08893b71eed64e73199d1314f09d56a8a895d` (13 October 2026).
Its [pinned guide](https://github.com/grove/proofline/blob/32b08893b71eed64e73199d1314f09d56a8a895d/README.md#optional-intentline--proofline-handoff)
describes explicit `check --intentline-export` import into the generic
[#13 evidence mapping](https://github.com/grove/proofline/issues/13).
Consumer offline tests passed; this producer change does not claim a live
end-to-end round trip or measured delivery benefit. Native execution qualification
and receipts remain Proofline-owned. The retired `deliver`/`inspect-intentline`
controller is historical, not current support.

## One optional flow

1. If a contract is useful, ask the **existing** agent to use the
   [planning skill](../skills/intentline-plan/SKILL.md), or author a source-grounded
   draft using the [manual tutorial](TUTORIAL.md). Inspect the full captured source,
   contract, constraints/exclusions and gaps. A second agent or audit is optional.
   A fresh DRAFT can be exported without adoption:

   ```sh
   python -B -m intentline check --work /private/work
   python -B -m intentline review --work /private/work --json
   python -B -m intentline export --work /private/work --format json \
     --out /private/json-export --json
   ```

2. Continue ordinary coding and repairs within actual user authorization. Written
   `oracle` and `planned_evidence` are proposed expectations, never executable
   commands or independently established answers. Choose the checks explicitly.

3. Pass the original request and selected checks to Proofline on its supported
   host, using an explicit supported Python interpreter (3.11+). For example:

   ```sh
   python -B /absolute/proofline/proofline.py check \
     --repo /absolute/product --source /private/request.md \
     --command 'python -B -m unittest discover -s tests' \
     --output /private/check-record
   python -B /absolute/proofline/proofline.py status /private/check-record/report.json
   ```

   The output must be new and outside the product. Inspect Proofline's current
   host/command limits before execution. This example grants no execution
   permission. **Without a wanted contract, skip step 1 entirely:** this command
   works without Intentline installed or any export/mapping.

   If using the supported JSON export, the same check can optionally use
   `--source /private/json-export/source-S1.txt` and add
   `--intentline-export /private/json-export`. The supplied source must match the
   complete original request byte for byte. For explicit R-to-check associations,
   optionally add `--intentline-links /private/links.json`; each R ID maps to a
   list of zero-based selected check `index` and complete matching `argv` pairs,
   as documented in the pinned consumer guide. No links are inferred from prose.

With no links, every imported R is **NOT DEMONSTRATED**, even if selected commands
pass. Linked checks provide limited evidence against the frozen candidate;
green commands do not establish full satisfaction or inventory completeness.
Completeness stays **UNKNOWN**. `status` checks retained identities and receipts
for drift. The existing agent owns omitted obligations, fixes and final handoff.

## Minimal existing producer contract

The current optional consumer supports **one unamended original request, S1 only,
acceptance schema 1 / initial revision 1**, exported with `--format json`.
It imports the following files as **untrusted advisory data**, never scripts:

| File / field | Meaning and required identity |
|---|---|
| `source-S1.txt` | Exact original UTF-8 bytes, including CRLF/final newline; never a summary or concatenated amendment |
| `source-manifest.json` | Canonical `intentline.sources`, schema 1, one `request` S1; byte length and SHA-256 bind the capture; root/path/inode fields remain provenance labels |
| `contract.json` | Canonical `intentline.acceptance`, schema 1, contract ID/revision and `source_bundle_sha256`; SHA-256 binds the whole contract |
| `requirements` | Stable unique R IDs, statement/basis, exact `source_refs` (`source_id`, one-based inclusive lines, verbatim quote), boundaries, seam, proposed oracle, `planned_evidence`, `plan_state` |
| `constraints`, `out_of_scope` | Complete source-cited constraints and exclusions, with constraint scope/basis; never silently dropped |
| `evidence_gaps` | Explicit R IDs and reasons; a `gap` row must retain its reason, not become a passing check |
| `export-manifest.json` | Canonical `intentline.export`, schema 1, format `json`, contract ID/revision, `contract_sha256`, `source_bundle_sha256`, `advisory: true`, authority label and every output file SHA-256; completion marker written last |

`source_bundle_sha256` hashes the canonical source-manifest bytes;
`contract_sha256` hashes canonical contract bytes. SHA-256 of the completion
marker identifies the export itself. Quotes may omit only the final line
terminator of their cited range; interior bytes remain exact. Origins are not
consumer file-read instructions. The consumer validates canonical records,
all listed hashes, exact full S1 bytes against its supplied request, citations
and explicit check links. Partial, tampered, extra-file or symlinked inputs refuse.

Revised contracts, S2/project contexts, multiple requests, amended/schema-2 source
lineage, native/Markdown/direct formats and child bundles are **unsupported by
this consumer adapter**. Unresolved decisions also refuse. Do not remove context,
flatten amendments, discard history or fall back to the retired controller to
make an unsupported export fit. Intentline's JSON/Markdown exports still preserve
successor archives; native exports retain full lineage and standalone inspection.
Those producer capabilities do not imply current consumer support.

## Authority and storage

**DRAFT** is an unadopted proposal (fresh status may be STRUCTURALLY_VALID).
**ADOPTED_ASSERTED** records an operator assertion with unverified authentication.
Export reports `unapproved` or `operator_asserted_unverified` respectively.
Actual external user/project authority must be established outside these records.
Exports, structural validity, audit labels, hashes and check results do not approve
work or authorize tests, model calls, PR publication, merge or deployment. Raw
approval records are not exported as authority. Source text outranks incomplete
advisory rows.

Storage and provenance rules are unchanged: secure no-follow POSIX reads/writes,
owner-only output, exact source captures and a final hash-bound completion marker.
Interrupted copies can be retried with identical inputs; changed exports need a
new output directory and existing files are never overwritten. Export only
reviewed data to a private handoff location; source and provenance can be sensitive.
Windows record storage remains unqualified and refuses with exit 3.

## Retained research and other peers

`proofline-direct`/`proofline-native`, their test-only pinned consumer snapshots,
and older qualification findings remain historical offline evidence. See
[the handoff research archive](../evaluation/PROOFLINE_HANDOFF.md) for pinned
original instructions and not-run/trust-stop records. They are not prerequisites
for current check-only use. No S0–S6 certification or evaluation restart is implied.

[Advisory Lore reports](LORE_CONTEXT.md) remain optional exact-byte, unverified
context inputs; use captured originals for applicable policy. The optional P2P
approved-contract exporter remains deferred: Intentline assertions are not
P2P approval. [Portable child handoffs](SLICING_INTEGRATIONS.md) remain data for
humans/existing agents; no current Proofline child adapter is supplied.
