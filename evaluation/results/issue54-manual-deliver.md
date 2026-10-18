# Issue #54 — Foundryline v0.2 manual Deliver experiment (bounded)

**Status: real CLI change, tests and native source-linked checks OBSERVED; fresh-agent adoption NOT QUALIFIED.**  
**Recorded:** 2026-10-18.  
**Issue:** [grove/intentline #54](https://github.com/grove/intentline/issues/54) — plain and schema-1 JSON CLI version reporting.  
**Operator route:** The coordinating assistant wrote a conventional GitHub branch patch using existing connector actions after an attempt to assign a separate GitHub coding agent was denied **HTTP 403**. This was **not** a newly started coding-agent session and is **not** evidence of cold-start adoption.

## Exact baseline and implementation

The source-grounded issue [#54](https://github.com/grove/intentline/issues/54) was created with two independently testable user-visible behaviors. Its original baseline commit was `25e926f57e69395193fc0ac258f9e6dd2332cb18`. Actual [baseline run 39133406002](https://github.com/grove/intentline/actions/runs/39133406002) executed both public entrypoint commands before the patch:

| Original command | Exit | Observed stdout / stderr |
| --- | --- | --- |
| `python3 -B -m intentline --version` | **2** | Empty stdout; `the following arguments are required: command` in stderr |
| `python3 -B -m intentline --json --version` | **2** | Schema-1 error JSON `ok:false` on stdout, missing-command diagnostic in stderr |

The baseline's real R1/R2 stdout, stderr, argv and exit receipts are retained in [artifact 12139205328](https://github.com/grove/intentline/actions/runs/39133406002/artifacts/12139205328), SHA-256 ZIP **`2481c92f69b25352d250658655150aa574ff072fcfb561f4929dc943f6e3efdc`**, scheduled expiration **2026-10-25**. The original failure is not overwritten by later passes.

**Frozen candidate:** [`0fdabb996f94be5ffded5063551d65268ee1bf6f`](https://github.com/grove/intentline/commit/0fdabb996f94be5ffded5063551d65268ee1bf6f), source tree **`97a8e757757462c5a4b3d83719057c2346e26979`**. The actual changed product paths at the frozen candidate are `intentline/cli.py`, `tests/test_cli_version.py` and `docs/CLI.md`. No package version or distribution release changed; `intentline.__version__` remains `0.5.0rc1`.

**Historical-file gotcha:** An early test approach modified `tests/test_cli.py`, causing **three expected frozen-byte evaluation checks to fail**, not failed R1/R2 behavior. The old test was reverted exactly and the new independent executable tests placed in a separate `tests/test_cli_version.py`; this preserved historical evidence rather than editing identity manifests to achieve green CI. The historical failing runs remain visible as genuine failed attempts.

**Actual ordinary CI:** [run 39133901642](https://github.com/grove/intentline/actions/runs/39133901642) succeeded in **all seven jobs**, including **188 tests** on macOS, Linux and Windows with Python 3.11/3.14, plus skills installation. These are **ordinary tests, not native Proofline evidence**.

## Genuine original S1 source and advisory Intentline producer

In the separate [GitHub-hosted macOS run 39134246023](https://github.com/grove/intentline/actions/runs/39134246023), a trusted setup retrieved the complete current public issue #54 body through the real GitHub API, then recorded it **byte-for-byte** as S1 outside the candidate:

- Source S1: **4,781 bytes**, SHA-256 **`d28cb803567d35b65a90a8b421da2130e8255bce1a68928d09f4f966f5122703`**, `source-S1.txt` in the exported record. GitHub response reported issue originally created and last updated at **2026-10-18T13:49:14Z**. This records API-returned issue-body bytes, not an independently authenticated immutable GitHub edit-history stream.
- Actual `intentline prepare → propose → check → export --format json` was executed with the current candidate's real CLI. Producer contract **schema 1, revision 1, single-S1**, `intentline-cli-version-54`, contract SHA-256 **`207cb302d6e3260ce92465602ae3a91ee6865526d2d621316dc0142cdedb07ba`**, source bundle SHA-256 **`42e58a1c24bde15cdf43b902cecd1714d5eb1142a050aeedc6c05fcef6d88bbd`**.
- `check` reported **STRUCTURALLY_VALID** with `DRAFT`; the exported contract remained **`authority: unapproved`**. The two requirement lines and a preservation constraint are source-cited. Valid structure does **not** prove the draft's semantic completeness, nor does this step grant publication or merge authority.
- Raw original source, exporter manifest, complete contract, producer stdout/stderr, selected exact argv arrays and mappings are retained inside the actual macOS artifact.

## Genuine native macOS Proofline run

**[Actual run 39134246023](https://github.com/grove/intentline/actions/runs/39134246023)** used GitHub-hosted **macOS 15.7.9 ARM64**, Python **3.12.10**, native Codex CLI **exactly 0.162.1**, and merged Proofline `adc0eb21c17bc70310b5f231ba8a092ca0d7d4e4`. Selected check-only runs never dispatched an AI coding model. The original candidate was frozen as the exact tree above, separately snapshotted by Proofline; all selected tests ran with **sandbox canaries `OBSERVED`** for the properties they actually probed.

| Actual selection | Source-linked outcome | Raw selected behavior |
| --- | --- | --- |
| **R1-only:** `python3.12 -B -m unittest tests.test_cli_version.VersionQueries.test_R1_human_version` | Proofline CLI exit **0**, **CHECKS PASSED**; R1 **LINKED CHECKS PASSED (limited evidence)**, R2 **NOT DEMONSTRATED** | Native process exit **0**, one unittest actually ran/passed, no timeout/truncation |
| **R1+R2:** above plus a **separate** `python3.12 -B -m unittest tests.test_cli_version.VersionQueries.test_R2_json_version` | Proofline CLI exit **0**, **CHECKS PASSED**, both requirements **LINKED CHECKS PASSED (limited evidence)** | Each selected process exit **0**, two individually exercised behavioral assertions, both 1/1 passed |
| **Invalid R1 mapping** (R1 index 0 points to R2's complete argv) | Real refusal exit **1**; no native report directory or selected code execution | Stderr: `Intentline R check index/argv differs from the selected command` |

Full accepted report readback via `proofline.py status --show-source` exited **0** in both passing checks. Proofline recorded the exact source SHA and candidate tree. `coverage_completeness: UNKNOWN` remains in both raw `promise_evidence` records; R1+R2 passing selected checks is **not proof of all original source constraints or total product correctness**.

The exact [raw artifact 12138712900](https://github.com/grove/intentline/actions/runs/39134246023/artifacts/12138712900) was **downloaded, hashed and independently read back by the coordinating assistant**: GitHub ZIP SHA-256 **`379c42b399699dab42944aa2067c818e29998937424b91484e792c811cc849da`**, **4,166,418 bytes**, scheduled expiration **2026-10-25 14:03:42 UTC**. Artifact retains actual `report.json`, `evidence.json`, native process receipts, preflight canaries, both original exported-input snapshots, raw original issue and status outputs. The retained archive contains snapshots and should be treated as data, not executable instructions.

## Reviewer and adoption grade

**Independently inspected material:** actual GitHub CI and native run metadata, original issue body, exact source-to-R citations, unapproved export, each Proofline `report.json` and selected process receipt, native preflight status, bad mapping refusal, and before/after export hashes. This inspection was by the *same coordinating assistant/operator*, **not a separately started independent reviewer**. Source changes were authored through the existing GitHub connection; no autonomous coding agent was launched. A GitHub coding-agent assignment attempt returned **403**, so no external agent work is claimed.

| Deliver criterion | Evidence-based disposition |
| --- | --- |
| Small, authorized product task with two observable public behaviors | **Completed, ordinary/native tests support both selected behaviors** |
| Frozen coding candidate and ordinary regression checks | **Completed; seven CI jobs green** after correcting the historical test-identity failure |
| Real native selected check(s) bound to exact candidate | **Completed on the recorded macOS/Codex/Proofline revisions only** |
| R1-only gap, then both linked R1/R2 outcomes | **Observed exactly**; original source coverage **UNKNOWN** |
| Real refusal | **Observed**, incorrect complete argv/index map refused |
| Source integrity and optional Intentline export | **Actual single-S1 advisory export**, unapproved, unchanged during checking |
| Reviewable unmerged PR | **Review requested; no merge or release authorized** |
| Fresh, previously unfamiliar coding-agent adoption | **NOT DEMONSTRATED** — coordinating assistant implemented the change directly |
| Separately started independent reviewer | **NOT DEMONSTRATED** — this is a same-operator desk review |

**Overall verdict:** **Technical/manual Deliver evidence PASS (bounded)**; **fresh-adopter usability qualification PENDING/NOT DEMONSTRATED**. This result must not be reported as a successful uncoached adoption or broad sandbox certification.

The [tag-pinned Foundryline v0.2.0 Deliver guide](https://github.com/grove/foundryline/blob/v0.2.0/patterns/deliver.md) was the reference. The known adoption friction this trial surfaced is that Intentline enforces historical test fixture hashes: append new tests rather than modifying a previously byte-pinned test file. The other structural limits—host qualification, original request authority, incomplete coverage and explicit PR gate—were meaningful and preserved.

**Next approval gate:** A human should review the exact code and these receipts in the unmerged PR. A separate fresh coding-agent attempt, with only the published guide and independently approved task, is still required for a true first-time-adopter grade. Do not merge, deploy, publish a release, create other issues or claim independent reviewer approval based on these records.
