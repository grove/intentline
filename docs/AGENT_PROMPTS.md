# Examples you can use in chat

Install the two main skills from your project's terminal:

```sh
npx skills@latest add grove/intentline --skill intentline-plan --skill intentline-issue
```

Then paste a request into your coding assistant's chat. Replace the example
request, issue URL, or destination with yours. No Python setup is needed for
clarification or issue work. [First time? Follow the walkthrough.](FIRST_USE.md)

## Clarify a feature

```text
Use intentline-plan to clarify this:
Let people download the table as CSV, keeping its current row order.
```

Expect a draft explaining what should work, important unanswered questions, and
suggested checks. It stays in chat. Refine it naturally: “Only filtered rows,”
or “Keep the original error wording.” You don't need to specify a mode.

## Improve an existing issue

```text
Use intentline-issue to suggest improvements to this issue:
https://github.com/ORG/REPO/issues/123
```

Expect suggested wording or a small patch, with important questions called out.
The issue stays unchanged. If it is already clear, the assistant should say so.
To apply the proposed changes, reply:

```text
Update that issue with these changes.
```

The update preserves unrelated content and metadata. Your assistant needs tracker
write access. A missing capability should result in a usable draft and an
explanation, rather than a claim that an update happened.

## Create one issue

```text
Use intentline-issue to create one issue in ORG/REPO for this:
Let people download the table as CSV, keeping its current row order.
```

Or, after clarifying a request:

```text
Use intentline-issue to create one issue from this draft in ORG/REPO.
```

That request authorizes creation in the named destination. Expect a verified
issue link, or a draft marked **NOT PUBLISHED** if creation cannot be completed.
For Jira or Linear, name the accessible project/team and use its native issue
identifier. Access depends on your assistant's existing tools.

## Turn an investigation finding into an issue draft

```text
Use intentline-issue to draft an issue from finding G1 in the report above.
```

The draft stays in chat. A suspected bug should remain qualified until supported
by runtime evidence; it should explain the smallest useful check to confirm or
refute it. Reported findings don't automatically become product requirements.
To publish the draft, use the create request above with the intended destination.

## When you need saved plans

Chat and issue workflows are enough for many tasks. The following workflows
keep a formal local record with source references and revision history. They
need the separate [Python setup and private storage](FAQ.md#what-if-i-want-to-save-a-plan).
Your assistant handles the record format and commands.

### 1. Plan one feature and save its acceptance draft

```text
Use intentline-plan to clarify /absolute/project/request.md
and save the plan under /absolute/private/intentline-work/FEATURE.
```

Expect the readable draft and its saved location. If setup or exact source
capture is missing, the assistant should still provide useful wording and
explain what prevents saving a formal record.

### 2. Explore a request before committing to a saved plan

Use the normal “clarify this” request above. Saving is optional; no special
“provisional” wording is required.

### 3. Check a saved acceptance draft for omissions or invented scope

```text
Use intentline-audit to check the saved plan at
/absolute/private/intentline-work/FEATURE against the original request.
```

Install this advanced skill with
`npx skills@latest add grove/intentline --skill intentline-audit`.
Expect a review of missing or unsupported requirements. The skill can save an
advisory report in the authorized work area; it doesn't edit or approve the plan.

### 4. Decide whether to split a large feature

```text
Use intentline-slice to suggest whether the saved plan at
/absolute/private/intentline-work/FEATURE needs smaller tasks.
```

Install with `npx skills@latest add grove/intentline --skill intentline-slice`.
Expect a reason to keep it together or the smallest useful breakdown. This doesn't
create child issues. Keeping a coherent task together is a successful result.

### 5. Reconcile a changed request with an existing saved draft

```text
Use intentline-plan to update the saved plan at
/absolute/private/intentline-work/FEATURE using the new request in
/absolute/project/request-amendment.md. Save a successor privately.
```

Expect a description of what changed and what stayed, plus a new saved draft.
The original history is preserved. Existing tracker issues are updated only if
you request that operation separately.

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

## Further reference

- [Issue workflow](ISSUE_WORKFLOW.md): tracker fields, evidence, and safe updates.
- [Saved planning procedures](PLANNING_RECORDS.md): exact source capture and revisions.
- [CLI reference](CLI.md): reading records and technical commands.
- [Integrations](INTEGRATIONS.md): optional handoffs to other tools.
