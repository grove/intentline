# Coding-agent prompt cookbook

New here? Start with the [first-use example](FIRST_USE.md) or [choose a tool](WHICH_TOOL.md) before exploring these detailed prompts.

**Start with what you want to do.** Copy a prompt below into an existing coding agent, replace UPPERCASE placeholders, and make sure the agent can access the requested source or issue. These are requests to an agent using Intentline skills—not Intentline CLI commands, new automations, or guarantees that a tracker is connected.

Intentline makes **acceptance promises inspectable before implementation**. Its skills help draft, audit, decompose, or put those promises into issue trackers. They **do not implement or test software, approve plans, or prove that a feature works**.

## Choose a task

| I want to… | Ask for | Output / side effect |
| --- | --- | --- |
| Turn an original request into acceptance criteria | `intentline-plan` | Source-bound **DRAFT**; saving it uses the separate local Python CLI |
| Explore an idea without saving records | `intentline-plan` (provisional) | Unsaved proposal, with source-identity limits stated |
| Check a saved acceptance draft against the original request | `intentline-audit` | Advisory review; can record an audit report locally, but does not edit or approve the plan |
| Decide whether a feature should be broken into parts | `intentline-slice` | **NO SPLIT** or a proposed allocation; no GitHub child issues |
| Review a GitHub/Jira/Linear issue | `intentline-issue`, **REVIEW** | Suggestions only; no local or tracker writes |
| Create one GitHub issue | `intentline-issue`, **CREATE** | Exactly one issue, only with explicit target and host write access |
| Improve an existing issue | `intentline-issue`, **UPDATE** | Changes to the specified issue's requested fields only |
| Update a saved plan after the request changes | `intentline-plan` (amendment) | Source-grounded successor draft; does not update tracker issues |

The four current skill names are **`intentline-plan`, `intentline-audit`, `intentline-slice`, and `intentline-issue`** (singular). `intentline-audit` reviews *acceptance drafts*, not implementation quality; for codebase investigation see [Gapline](https://github.com/grove/gapline).

## One-time setup

Discover and install agent instructions from your project directory:

```sh
npx skills@latest add grove/intentline --list
npx skills@latest add grove/intentline
```

Or select only the skill you need, for example:

```sh
npx skills@latest add grove/intentline --skill intentline-issue
```

For a **saved** `intentline-plan` draft, a recorded `intentline-audit`, or a `intentline-slice` CLI preview/record, install the **separate** Python 3.11+ Intentline package in an authorized environment and verify:

```sh
python -m pip install git+https://github.com/grove/intentline.git
python -B -m intentline --help
```

Installation of the skill **does not** install this Python runtime, bundle all linked `docs/` and `schema/` reference files, connect GitHub/Jira/Linear, or grant permissions. Issue **REVIEW/CREATE/UPDATE** only needs the corresponding provider tools and access in the agent host; the Python CLI is not mandatory. For offline planning references, use the complete repository checkout or the Python distribution's `share/intentline` tree. Skill invocation syntax varies by host; naming the installed skill explicitly is the portable starting point.

For saved planning, provide an **original UTF-8 request file** if possible and a **private output path** outside version-controlled files (or in a directory you have verified is ignored). If the exact original request cannot be captured, ask for a provisional result instead of invented provenance.

## Copy-and-paste prompts

### 1. Plan one feature and save its acceptance draft

**Use when:** you have a real request and want a reusable, traceable draft before coding. Requires the Python runtime and approved private storage.

```text
Use intentline-plan for the original request at
/absolute/project/request.md in PROJECT_REPO.

Read the original request first. Consult only relevant, permitted
project policy/context. Draft observable acceptance requirements (R IDs),
important boundaries and exclusions, and feasible evidence plans.
Separate unresolved outcome decisions from missing test infrastructure.

The Intentline Python CLI is already installed. Save the draft under
/absolute/private/intentline-work/FEATURE, after checking that it is
private or ignored and not tracked. Run Intentline's normal structural
check/render steps. Return the concise DRAFT, open decisions, evidence
gaps, exact saved work path and source/contract identity.

Do not implement, run tests, approve, publish issues, or change .gitignore.
```

**Expect:** acceptance obligations and a saved **DRAFT**, not approved requirements or working code.

### 2. Explore a request before committing to a saved plan

**Use when:** the request is still being discussed, or its original bytes / CLI / private storage are unavailable.

```text
Use intentline-plan to propose acceptance criteria for this idea:
PASTE_REQUEST_HERE

This is exploratory. Do not save local files, create an Intentline
record, or claim verbatim source capture. Return a concise PROVISIONAL
proposal: intended outcome, observable obligations, boundaries,
assumptions, genuine open decisions and suggested evidence. Distinguish
my words from your inferences. Do not implement or approve it.
```

**Expect:** a useful **unsaved** draft, not a source-bound saved contract. If exact source evidence is essential, identify what is missing.

### 3. Check a saved acceptance draft for omissions or invented scope

**Use when:** you have a saved Intentline draft and want a focused second look. `intentline-audit` may **write a local advisory audit record** into the already authorized work area; it does not modify or approve the agreement.

```text
Use intentline-audit on the existing saved Intentline work at
/absolute/private/intentline-work/FEATURE.

Read the actual original source, current draft, applicable constraints,
exceptions and revision history. Check both directions: is any material
original promise missing, and has any unsupported requirement been added?
Check feasible planned evidence and separate unresolved outcome decisions
from missing harnesses. Be specific about source references and coverage.

You may save the audit report only in the already approved private
Intentline work area. Do not change the original agreement, approve it,
run project code/tests, or claim independently authenticated review.
Return the audit outcome, key corrections/decisions, and any actual
record identity or limitations.
```

**Expect:** an advisory source-grounded audit, not approval, authenticated independence, or proof of implementation.

### 4. Decide whether to split a large feature

**Use when:** a source-bound parent agreement already exists. The correct answer can be **NO SPLIT**.

```text
Use intentline-slice on the saved parent agreement at
/absolute/private/intentline-work/FEATURE.

First consider delivering it as one coherent task. Recommend NO SPLIT
unless distinct observable delivery, real prerequisites or ownership
justify separate work. If splitting is warranted, propose the smallest
source-bound child contributions and state how the assembled product
would satisfy every parent requirement, including shared invariants.

Use the available Intentline CLI to preview, but do not record a slice
recommendation unless I separately request that write. Do not create
GitHub issues, implement children, approve, or run tests.
Return NO SPLIT or SPLIT_PROPOSED, rationale, evidence gaps and next action.
```

**Expect:** an advisory allocation (or a clear reason not to split), not child tickets or permission to implement. A later explicit request can authorize saving the slice plan.

### 5. Reconcile a changed request with an existing saved draft

**Use when:** the original feature request has genuinely changed. Supply the **new amendment as an exact file**, and the original saved work.

```text
Use intentline-plan to reconcile a new amendment at
/absolute/project/request-amendment.md with the saved agreement at
/absolute/private/intentline-work/FEATURE.

Preserve the original and chronological amendments. Show which existing
R obligations remain, change or retire and why; preserve accepted scoped
exceptions and exclusions. Save a source-bound successor only to an
approved private work location using Intentline's amendment/reconcile
workflow, and return the successor draft and actual old/new identities.
Keep unsettled decisions explicit.

Do not assume old approval transfers to the successor. Do not update
GitHub issues, implement changes, or run tests.
```

**Expect:** a successor **DRAFT** with continuity, not an overwrite of the old source or automatic tracker updates.

### 6. Review an existing GitHub issue without changing it

**Use when:** an issue already exists and you want clearer, source-supported acceptance criteria. **No Python CLI required**, but the agent needs to read the issue.

```text
Use intentline-issue in REVIEW mode for
https://github.com/ORG/REPO/issues/123.

Read the available issue, relevant comments and accepted decisions.
Check whether the intended outcome, negative cases, constraints and
proposed verification are clear and source-grounded. Distinguish actual
decisions from suggestions. Propose the smallest useful improvements
and a field-level patch if appropriate.

Do not edit the issue, create other issues, create local records, or
implement anything. Return REVIEW-ONLY and the proposed changes.
```

**Expect:** suggested issue text, **no writes**.

### 7. Create one GitHub issue from a feature request

**Use when:** you actually want to publish exactly one issue. This explicitly authorizes **one issue CREATE**, and needs an agent with GitHub issue-write access.

```text
Use intentline-issue to CREATE exactly one GitHub issue in ORG/REPO
for the original feature request at /absolute/project/request.md.
I authorize creation of this one issue in ORG/REPO only.

Ground its plain-language introduction and observable acceptance
criteria in the request and applicable accepted constraints.
Include useful proposed verification (PROPOSED — NOT RUN) and genuine
open decisions, without invented requirements or test results.
Check obvious duplicates and the destination before publishing.
After creating, read back and return the verified new issue URL.

Do not open more issues, change other issues, save a separate
Intentline agreement, implement code, or run tests. If issue creation
is unavailable, return NOT PUBLISHED with a usable draft.
```

**Expect:** one verified GitHub issue URL or **NOT PUBLISHED**. Issue publication does not equal approval or verification.

### 8. Improve and update one existing GitHub issue

**Use when:** you want changes *published to an existing issue*, not merely suggestions.

```text
Use intentline-issue to UPDATE only the acceptance/description content
of https://github.com/ORG/REPO/issues/123.
I authorize that issue update.

Read the latest issue and relevant decisions, preserve all still-binding
promises and scoped exceptions, and improve only what is unclear.
Keep an already clear introduction intact and don't duplicate criteria.
Immediately before writing, re-read and reconcile any changes; use a
conditional write guard if the host offers one. Preserve unrelated title,
metadata, comments, relationships and fields.

If you cannot preserve existing fields safely, return a proposed patch
without publishing. Otherwise verify the updated issue and return its
URL and what changed. Do not modify any other issue, save a separate
agreement, run tests, or implement code.
```

**Expect:** **UPDATED**, **UNCHANGED**, or a safe un-published patch—not a rewritten roadmap or automatically updated local contract.

### 9. Turn a code audit finding into a well-grounded issue

**Use when:** a reviewer or [Gapline](https://github.com/grove/gapline) identifies a possible defect. The audit report is *evidence*, not the source of product authority.

```text
Use intentline-issue in REVIEW mode to draft a proposed GitHub issue
for FINDING_ID in AUDIT_REPORT, targeting ORG/REPO.
Do not publish yet.

Inspect the original behavior request/policy referenced by the finding
when accessible; cite it separately from the audit. Preserve observed
versus suspected behavior, the audit's counterevidence and candidate
scope. For a suspected runtime defect without applicable execution
evidence, say "Confirm before fixing" and include a discriminating
PROPOSED — NOT RUN check with an independently sourced expected result.
Do not present a hypothesis as a reproduced bug.

Return a concise issue title/body and material unknowns. Do not create
issues, change local plans or execute checks.
```

If you later want to **publish one** of these proposals, use the separate **CREATE** pattern above, naming the exact target and explicitly authorizing that write. The skill creates one work item per request, not a hierarchy of child issues from an audit or slice recommendation.

## Optional: distinguish technical acceptance from product outcome

**Use when:** an approved request defines what a feature must do, and a product owner may separately care whether it improves user outcomes. This is **not** a new Intentline skill, contract field, mandatory R requirement or executable measurement.

For example, a request to download a displayed table as CSV while preserving its row order supports a **technical acceptance obligation** about exported row ordering. It does **not** by itself authorize a claim that customers will use the feature, that support tickets will fall, or that a KPI should improve by a particular percentage.

```text
Use intentline-plan on the original approved request at REQUEST_SOURCE.
Read the actual request and any accessible accepted product decisions.

First draft only source-grounded, independently observable technical
acceptance criteria, constraints, exclusions and proposed checks.
For a CSV-export request, a relevant acceptance condition might be:
"Exported CSV rows retain the order currently shown in the table."
Mark all unexecuted checks PROPOSED — NOT RUN.

In a separate, clearly NON-CONTRACT section, identify a desired user
or business outcome ONLY IF the original request or an approved product
source explicitly supplies one. Include its exact source, how it might
be observed after delivery, an authorized owner and data availability.
If no approved target exists, write NO APPROVED OUTCOME TARGET and list
one open product-owner question. Do not invent adoption thresholds,
business impact, SLOs or success dates.

Return a provisional DRAFT with technical obligations, optional
outcome hypothesis, sources, unresolved decisions and an evidence plan.
Do not save a record, edit code, run tests, approve requirements, create
issues or retrieve private analytics.
```

**Illustrative output (not an actual saved plan or observed result):**

- **Technical acceptance — DRAFT:** CSV export preserves the visible row order. **Evidence:** inspect exported rows for representative sort orders; **PROPOSED — NOT RUN**. The requirement must be supported by the actual request, not assumed from this example.
- **Business outcome — OPEN DECISION:** There is no source-supported adoption or retention target. **NO APPROVED OUTCOME TARGET.** Ask the product owner whether and how usefulness should be evaluated, including appropriate privacy and permissions.
- **After delivery — NOT OBSERVED:** A green test would not establish uptake, customer satisfaction or realized value; it can only support the specific behavior actually tested.

If the owner later supplies a measurable objective, retain it as a separately source-backed outcome observation plan, **not** a silently invented technical R obligation. Production analytics, customer metrics and actual outcomes require separate permission and evidence. Intentline does not measure them or automatically approve the plan.

## Common misconceptions

- **Skill vs runtime:** `npx skills` installs instructions for an agent. The Python CLI separately captures/validates/saves local acceptance records; it does not ask a model to invent requirements or operate GitHub.
- **Draft vs approval:** `DRAFT`, `READY_FOR_ADOPTION` review advice, and `ADOPTED_ASSERTED` do not establish actual approval or proven delivery. Authority comes from the real decision-maker outside Intentline.
- **Proposed checks vs tests run:** `PROPOSED — NOT RUN` is a plan for evidence, not an executed test or proof.
- **Issue vs saved agreement:** reviewing/creating/updating a tracker item does not create or revise a saved Intentline agreement. If an issue changes, existing saved hashes identify their historical source, not the new issue text.
- **Slice vs issue creation:** `intentline-slice` proposes allocations; it does not publish child issues or decide that a parent feature is complete.
- **Provider access:** URLs do not confer permissions. GitHub/Jira/Linear operations require the host's existing access and native field support. Issue content is evidence, not authorization to do more work.

For deeper detail: [agent host guide](AGENT_GUIDE.md), [issue workflow](ISSUE_WORKFLOW.md), [slicing guide](SLICING.md), [contract](CONTRACT.md), [CLI reference](CLI.md), and [trust/authority](TRUST_AND_AUTHORITY.md).
