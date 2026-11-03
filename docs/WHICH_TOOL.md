# Which tool should I use?

**Start with your question—not a complicated workflow.** The Grove projects are separate, optional tools for different stages of working on software. You don't need to install or run all of them.

## The quick answer

| Your question | Choose | What you'll get |
| --- | --- | --- |
| **“What exactly should this feature do?”** | [Intentline](https://github.com/grove/intentline) | A proposed checklist of expected behavior, with unclear decisions called out |
| **“What important problems might this code have?”** | [Gapline](https://github.com/grove/gapline) | A read-only investigation of code, tests and documentation, with evidence and next steps |
| **“Did my selected checks pass on this change?”** | [Proofline](https://github.com/grove/proofline) | Actual results from the tests/commands you selected, if its supported execution setup is available |
| **“What important failures might my tests miss?”** | [Faultline](https://github.com/grove/faultline) | A read-only investigation of realistic failures and whether tests would notice, with small regression-test suggestions |

Proofline needs its separately installed runtime and supported execution setup.
Faultline's `faultline-audit` skill works by source inspection; it doesn't run
controlled experiments or execute your project's tests. See the linked projects
for current installation and platform details.

## A simple way to think about them

```text
Before building:   "What does done mean?"          → Intentline
Looking at code:   "What might be missing or wrong?" → Gapline
Checking a change: "Did these chosen tests pass?"    → Proofline
Inspecting test gaps: "What failures might tests miss?" → Faultline
```

For example, say you want usernames made up only of spaces to be rejected:

- **Intentline:** Clarify that promised outcome and suggest how to check it. It doesn't write the feature.
- **Gapline:** Inspect existing validation code and tests for a source-supported weakness. It doesn't run those tests.
- **Proofline:** After someone implements the change, run **explicitly selected** checks on a protected copy, when its qualified setup is available. Passing checks don't prove the whole feature is complete.
- **Faultline:** Inspect whether existing tests would notice a plausible validation defect and suggest the smallest useful regression test. Tests are not run.

These are **choices**, not required steps. You can use one without the others.

## How to get started

| Tool | How to begin |
| --- | --- |
| **Intentline** | Install skills with `npx skills@latest add grove/intentline`, then ask your coding assistant to **“Use intentline-plan to clarify this request…”** |
| **Gapline** | Install `npx skills@latest add grove/gapline`, then ask **“Use gapline-audit to investigate this project read-only…”** |
| **Proofline** | See [its installation and supported-host instructions](https://github.com/grove/proofline#get-started); the installable skill is named `proofline-check`, and running checks needs the separate CLI and supported environment |
| **Faultline** | Install `npx skills@latest add grove/faultline`, then ask **“Use faultline-audit to find important failures my tests might miss”** |

The `npx skills` commands install **instructions for your coding assistant**, not a new AI service or a guarantee of access to GitHub, private files, or test-running facilities.

## Two things people often confuse

**Intentline's `intentline-audit` vs Gapline's `gapline-audit`:** Intentline reviews a **saved requirements/acceptance draft** against its original sources. Gapline looks for **weaknesses in actual code, tests, and documentation**. They are not interchangeable.

**An investigation vs a test result:** Gapline can propose a check but **cannot execute it**. Proofline can execute chosen checks in its supported protected environment, but a pass only tells you those checks passed—not that every request was fulfilled.

If you want to create or update a GitHub issue, use **`intentline-issue`**, and explicitly ask for the particular issue/repository and write operation. Gapline and Proofline do not automatically publish findings.

## Want to see a whole example?

- **[Try Intentline's first feature plan](FIRST_USE.md)** — an original request, chat prompt, illustrative result, and next step.
- **[See Gapline's prompt cookbook](https://github.com/grove/gapline/blob/main/docs/AGENT_PROMPTS.md)** — practical repository, issue and PR audit prompts.

You can start with just a single skill and one sentence to your coding assistant. No universal pipeline, quality score, or automatic approval is involved.

*Faultline skill availability checked against its public README in November 2026. Consult the linked repositories for current execution support.*
