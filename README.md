# Intentline

**Make the promise clear before the code changes.**

Intentline helps you turn an original request into a **source-grounded acceptance draft**: a small, traceable description of what must be true, what is out of scope, and what evidence could show the work is done.

Bring your own coding assistant—or write the JSON yourself. Intentline's offline Python CLI captures the original sources, checks the structure, preserves exact identities and revisions, and lets you inspect the result. **It does not write requirements for you, implement code, run tests, or approve anyone's work.**

**At a glance:** Python 3.11+ · no runtime dependencies · local/offline CLI · POSIX storage support · [Apache-2.0](LICENSE)

[Quick start](#quick-start) · [Try it without an agent](#try-it-without-an-agent) · [CLI reference](docs/CLI.md) · [Trust and authority](docs/TRUST_AND_AUTHORITY.md)

## Why use Intentline?

A feature request can be deceptively short:

> Reject empty and whitespace-only usernames.

Before implementation, it helps to make the acceptance promise explicit:

- **R1 — Outcome:** Empty and whitespace-only usernames receive a validation error.
- **Source:** The exact line in the original request supporting R1.
- **Boundaries:** Representative inputs that should succeed or fail.
- **Evidence plan:** How someone could observe the expected behavior independently of the implementation.
- **Open questions:** Genuine outcome or authority decisions, separated from missing test infrastructure.

That is an *illustration*, not a test result. Intentline keeps the full agreement machine-readable, with stable requirement IDs (`R1`, `R2`, …), citations, constraints, exclusions, evidence gaps, and a versioned history. It can validate the shape and identity of the record; a human or agent still has to judge whether the plan faithfully captures the request.

A typical workflow looks like this:

```text
Original request (+ selected project context)
                  |
               prepare        Capture exact source bytes and identity
                  |
      Your agent or you        Write an acceptance draft (schema-1 JSON)
                  |
               propose        Validate and save an immutable revision
                  |
          check / review      Inspect status, citations, gaps, and changes
                  |
        Optional next steps   Audit, external adoption, advisory export, or slicing
```

## Install agent skills with npx

From your target project:

```sh
npx skills@latest add grove/intentline --list
npx skills@latest add grove/intentline
```

Choose `intentline-plan` for routine acceptance planning, `intentline-audit` for an optional review, or `intentline-slice` for optional decomposition. The installer discovers all three from their `skills/` folders. For unattended Codex installation of the planning skill:

```sh
npx skills@latest add grove/intentline --skill intentline-plan -a codex -y
```

**These commands install agent instructions, not the Python runtime.** For actual `prepare`, `propose`, `check`, `render`, `audit-record`, or `slice` commands, separately install Intentline in a Python 3.11+ environment (e.g. `python -m pip install git+https://github.com/grove/intentline.git`) and verify `python -B -m intentline --help`. The existing `SKILL.md` files keep their historical checkout-relative `../../docs` and `../../schema` links. Those linked directories **are not copied by `npx skills`**, so the links will not resolve from a standalone installed skill folder. Give the agent access to the complete checkout or to the separately installed package's `share/intentline` documentation and schemas. The installation smoke test verifies skill discovery and copying, not a complete CLI workflow. No automatic dependency installation or additional model is implied.

## Quick start

### 1. Install from source

Use **Python 3.11 or newer** on Linux or macOS (or another supported POSIX host). From a checkout:

```sh
git clone https://github.com/grove/intentline.git
cd intentline

python3.11 -m venv .venv   # Or another Python 3.11+ interpreter
. .venv/bin/activate
python -m pip install .

intentline --help
```

You can also run commands as `python -B -m intentline ...`. The `-B` flag avoids Python bytecode cache writes. There are no model SDKs, API keys, databases, or peer services to configure for normal use.

**Windows note:** Installing the package and displaying help work on Windows, but secure record storage is **not yet supported** there; record operations refuse with exit code 3. See [platform and security details](docs/CLI.md).

### 2. Ask your existing assistant to plan one request

Save the *original* request as a UTF-8 file, for example `/absolute/project/request.md`. Use an agent that can read files and run local commands.

Find the installed planning skill:

```sh
python -B -c 'import sysconfig; print(sysconfig.get_path("data") + "/share/intentline/skills/intentline-plan/SKILL.md")'
```

Give the assistant that **absolute skill path** and an instruction like:

> Read and follow the Intentline planning skill at `/absolute/path/to/share/intentline/skills/intentline-plan/SKILL.md`. Use Intentline to plan acceptance for `/absolute/project/request.md`. Select only necessary, permitted context. Save the draft privately and return the requirements, important decisions/gaps, and exact source/contract identities. Do not implement or approve anything.

The agent handles the JSON and `prepare → propose → check → render` steps. Its normal result is an **unapproved DRAFT**—useful for planning immediately, without a mandatory second model or audit.

This is a **direct-file skill entry**, not a claim that every agent host automatically discovers skills or supports a particular slash command. See the [agent host guide](docs/AGENT_GUIDE.md) for the supported entry style.

### 3. Inspect the draft before coding

Use the work directory the assistant returned (not necessarily the sample below):

```sh
python -B -m intentline review --work /private/path/to/work --json
python -B -m intentline render --work /private/path/to/work
python -B -m intentline status --work /private/path/to/work --json
```

Read the **original request and the full agreement**. Ask whether every material promise, constraint, and exclusion is represented—and whether anything unsupported was added. `STRUCTURALLY_VALID` means the record passed deterministic checks; it does **not** mean that the criteria are complete, approved, implemented, or proven.

## Try it without an agent

The repository ships a tiny, already-authored [username-validation example](examples/username-validation/request.md). From the repository root, after installation, these commands run the manual path. They **do not** ask the CLI to invent acceptance criteria.

First capture the request:

```sh
python -B -m intentline prepare --source examples/username-validation/request.md --out .intentline/work/username-demo --json
```

Then make a draft from the example template, binding it to the *actual* captured source manifest:

```sh
python -B - <<'PY'
import hashlib
import json
from pathlib import Path

work = Path(".intentline/work/username-demo")
draft = json.loads(Path("examples/username-validation/good.template.json").read_text())
draft["source_bundle_sha256"] = hashlib.sha256(
    (work / "source-manifest.json").read_bytes()
).hexdigest()
(work / "draft.json").write_text(json.dumps(draft, indent=2) + "\n")
PY

python -B -m intentline propose --work .intentline/work/username-demo --draft .intentline/work/username-demo/draft.json --json
python -B -m intentline check --work .intentline/work/username-demo
python -B -m intentline render --work .intentline/work/username-demo
```

You now have a source-bound draft and a readable view of it—not a test run or a claim that the behavior exists. For real requests, author a complete draft against the captured sources using the [acceptance schema](docs/CONTRACT.md). The [step-by-step tutorial](docs/TUTORIAL.md) explains fields, negative examples, exports, and the separate adoption path.

## What can the CLI do?

| Stage | Commands | Purpose |
| --- | --- | --- |
| Capture and draft | `prepare`, `propose` | Freeze explicitly selected source files; validate and record an immutable acceptance revision |
| Inspect | `check`, `status`, `render`, `review` | Check source freshness, show the agreement, and compare revisions |
| Change the request | `amend-source`, `reconcile` | Preserve the original and amendments; publish a successor with explicit obligation continuity |
| Optional oversight | `audit-record`, `approval-request`, `adopt` | Record advisory audit findings, prepare an **unapproved** approval request, or record an actual external adoption assertion |
| Handoff | `export`, `inspect-native` | Produce advisory JSON/Markdown/native handoffs and inspect native bundles offline |
| Optional sizing | `slice preview`, `slice record`, `slice status`, `slice render`, `slice impact`, `slice audit-record`, `slice export`, `slice inspect` | Consider a source-bound decomposition without silently creating or approving child work |

Each command has `--help`; most workflows also support `--json` for versioned, machine-readable results. Start with [the complete CLI reference](docs/CLI.md) and [acceptance contract](docs/CONTRACT.md).

### Revisions, amendments, and approval are different things

- **Revisions** retain immutable history for changes to a draft against the same source.
- **Amendments** capture a changed request as a new source generation. `reconcile` requires explicit continuity of the old obligations; a predecessor's approval does not carry over.
- **Audits** are optional advice. A recorded audit is not authenticated independent review.
- **Adoption** requires actual authority *outside* Intentline. `ADOPTED_ASSERTED` means an operator supplied an adoption assertion; Intentline cannot verify the actor or grant permission.

For a consequential decision, you can invite a separate reviewer to use [`intentline-audit`](skills/intentline-audit/SKILL.md). To propose a smaller delivery boundary, use [`intentline-slice`](skills/intentline-slice/SKILL.md); **NO SPLIT is a good outcome** when the original promise is already coherent. Recording a slice plan is an explicit, separate action. See [slicing](docs/SLICING.md).

### Optional integrations—not required services

- **Proofline:** `export --format json` can provide source-bound promise data for optional check evidence mapping. The current consumer supports only one original request (S1) with an initial schema-1 agreement; amended/child/native lineage is not supported by that consumer. Ordinary coding and Proofline check-only work do **not** require Intentline. See [integration limits](docs/INTEGRATIONS.md).
- **Lore:** Previously produced Lore context may be inspected as advisory input; Intentline does not run Lore or confer authority through its reports. See [Lore context](docs/LORE_CONTEXT.md).
- **AI-development evaluation:** The optional read-only 0.6 evaluation adapter inspects already-produced private records. It does not launch agents or models. See the [operator runbook](evaluation/RUNBOOK_06.md).

## Privacy, trust, and platform boundaries

Intentline is deliberately conservative:

- **Keep private sources private.** Requests and captured context may contain confidential material. Prefer an owner-only directory outside tracked files, or an explicitly ignored `.intentline/work/<slug>/`. This repository ignores `.intentline/`, but **your other repositories may not**. Check their ignore rules *before* capturing anything; Intentline never edits `.gitignore` for you.
- **Identity is not authority.** Exact bytes, source citations, hashes, and stored records help detect changes; they cannot authenticate users, make semantic requirements correct, certify independent reviews, or approve delivery.
- **Planning does not execute.** The CLI does not run models, tests, Git, external services, or code from the request. An export is advisory data, not permission to code, publish, merge, or deploy.
- **Storage support is bounded.** Secure record operations use POSIX no-follow filesystem techniques; they do not protect against a malicious directory owner or qualify network filesystems/power-loss behavior. Windows record storage fails closed.

Read [trust and authority](docs/TRUST_AND_AUTHORITY.md) for the complete model and [CLI/storage details](docs/CLI.md) for limits and exit codes.

## Project status

**Experimental.** The source package currently declares `0.5.0rc1`; this README does not imply a published PyPI package, GitHub release, or a versioned 0.6 product release. The core CLI and three skills remain the user-facing workflow.

Engineering tests and packaging checks are documented separately from claims about usefulness. The bounded 0.6 planning pilot found **no verified overall planning advantage**, and the strict study remained unrun; observed overhead and critique limitations are reported rather than hidden. See the [0.6 scorecard](docs/SCORECARD_0.6.md), [0.5 scorecard](docs/SCORECARD_0.5.md), and [evaluation protocol](evaluation/README.md).

## Documentation map

- **Start using it:** [Agent guide](docs/AGENT_GUIDE.md) · [Manual tutorial](docs/TUTORIAL.md)
- **Understand the records:** [CLI](docs/CLI.md) · [Acceptance contract](docs/CONTRACT.md) · [Trust boundaries](docs/TRUST_AND_AUTHORITY.md)
- **Extend the workflow:** [Slicing](docs/SLICING.md) · [Integrations](docs/INTEGRATIONS.md) · [Packaged planning skill](skills/intentline-plan/SKILL.md)
- **Develop or evaluate:** [Development and tests](docs/DEVELOPMENT.md) · [Evaluation](evaluation/README.md) · [Implementation history](docs/IMPLEMENTATION_0.6.md)

## Contributing

Questions, bug reports, documentation improvements, and carefully scoped pull requests are welcome. If you're new here, a useful first contribution is a clearer example, an edge case reproduced with an exact input, or a correction to a confusing first-use step.

For development, use Python 3.11+ and run the offline unit tests from the checkout:

```sh
python -B -m unittest discover -v
```

See [development and qualification](docs/DEVELOPMENT.md) for package-build smoke tests and platform expectations. Please avoid committing private request files, pilot records, credentials, or source captures.

**License:** [Apache License 2.0](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md).

---

**The goal is simple:** a useful, inspectable promise before implementation—and an honest record of what is still unknown.
