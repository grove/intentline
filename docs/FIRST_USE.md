# Your first useful task

Start with a request you would normally give your coding assistant. Intentline
helps you decide what should happen before you start building it.

## 1. Install

In your project's terminal:

```sh
npx skills@latest add grove/intentline --skill intentline-plan --skill intentline-issue
```

Choose your coding assistant when prompted. You'll need Node.js 22.20+ and Git.
Then switch to your assistant's chat. You don't need Python for this walkthrough.

## 2. Ask in ordinary language

```text
Use intentline-plan to clarify this:
Let people download the table as CSV, keeping its current row order.
```

Here is an **illustrative response**, rather than a captured agent run:

> **CSV download**
>
> Add a CSV download of the displayed table, preserving its current row order.
>
> **What should work**
> - Downloading a sorted table keeps the displayed order.
>
> **One question to settle**
> Should the download include only rows matching the current filter, or every row?
>
> **Suggested check — not run**
> Sort a small table, download it, and compare the downloaded order with the screen.

The question matters because the answer changes which rows the feature exports.
Intentline can still describe the settled behavior while that choice is open.
It shouldn't turn every unspecified implementation detail into a question.

## 3. Refine it

Reply:

```text
Only rows matching the current filter. Keep it small.
```

The revised draft should keep the ordering requirement and add the filtering
decision. Its suggested check can use a table with a hidden row, sort the visible
rows, and compare the downloaded rows with exactly those displayed.

For a small request such as “Reject empty and whitespace-only usernames,” one
criterion and examples using an empty string and spaces may be enough. There
is no minimum number of questions, requirements, or test scenarios.

## 4. Use the result

You now have a draft you can discuss with a developer or use in your normal
coding workflow. The suggested checks haven't been run.

If you want a ticket, say:

```text
Use intentline-issue to create one issue from this draft in ORG/REPO.
```

That request authorizes creation of one issue in the named repository, if your
assistant has access. Replace `ORG/REPO` with your destination.

Already have an issue? Start directly with:

```text
Use intentline-issue to suggest improvements to this issue: ISSUE_URL
```

Suggestions stay in chat. Say “Update that issue with these changes” when you
want them applied. A clear issue can be left unchanged.

## Need to keep a formal record?

Chat drafts need no storage setup. If you want a saved plan with original-source
references and revision history, ask to save it. Your assistant will explain any
needed [Python and storage setup](FAQ.md#what-if-i-want-to-save-a-plan).

[More examples](AGENT_PROMPTS.md) · [Common questions](FAQ.md) · [Back to Intentline](../README.md)
