# Intentline

**Turn a rough request into a clear task someone can build and check.**

Intentline works inside your AI coding assistant. It helps you catch missing
requirements, avoid accidental scope changes, and explain what “done” means.

## Install once

Run this in your project's terminal, then choose your coding assistant:

```sh
npx skills@latest add grove/intentline --skill intentline-plan --skill intentline-issue
```

You'll need Node.js 22.20+ and Git for the installer. Then use Intentline in your
**assistant's chat**. No Python setup is needed for the two tasks below.

## Clarify a request

```text
Use intentline-plan to clarify this:
Let people download the table as CSV, keeping its current row order.
```

You get a draft in chat. For example:

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

This is an illustrative response. Intentline keeps unanswered questions separate
from requirements, so it doesn't silently decide the feature's scope for you.
Reply naturally: “Only the filtered rows,” or “Keep this as one small task.”

## Improve an issue

```text
Use intentline-issue to suggest improvements to this issue:
https://github.com/ORG/REPO/issues/123
```

Replace the link with your issue. Your assistant reads the issue and relevant
discussion, then suggests clearer wording, completion criteria, and useful checks.
Suggestions stay in chat.

To apply them, say **“Update that issue with these changes.”** To create a new
issue from a draft, say **“Create one issue from this draft in ORG/REPO.”**
Your assistant needs access to that tracker. GitHub, Jira, and Linear access
depends on the tools already connected to your assistant.

Intentline plans work; it doesn't implement features or run the suggested checks.

## When you need more

Most tasks can stay in chat or your issue tracker. For longer-lived work,
Intentline also supports saved plans with source references and revision history,
reviews of those plans, and suggestions for splitting larger tasks.

- [First-use walkthrough](docs/FIRST_USE.md) — see a request clarified and refined.
- [More examples](docs/AGENT_PROMPTS.md) — issues, saved plans, and larger tasks.
- [Setup and common questions](docs/FAQ.md) — installation and troubleshooting.
- [Advanced workflows](docs/ADVANCED.md) — optional Python runtime, saved records, and integrations.

[Agent setup](docs/AGENT_GUIDE.md) · [Development](docs/DEVELOPMENT.md) · [License](LICENSE)
