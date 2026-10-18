# Intentline: common questions

[Back to the quick start](../README.md) · [Copy-and-paste prompts](AGENT_PROMPTS.md)

## What do I need to install?

Start with an AI coding assistant that supports skills, a terminal, and **Node.js / npm** and **Git** for the skill installer. From your project:

```sh
npx skills@latest add grove/intentline
```

Select the assistant and skills you want. This installs **instructions for the assistant**, not a separate Intentline application or an issue-tracker connection. If `npx` is not found, you likely need a supported Node.js installation.

## Where do I put the prompts?

In the **chat of your coding assistant**, not the terminal. The command above installs skills; prompts like “Use intentline-issue to review this GitHub issue” ask the assistant to use them.

If your assistant cannot find a skill, check that you installed it for the right assistant and project. You can see discoverable skills with:

```sh
npx skills@latest add grove/intentline --list
```

Some assistants need a new session or a direct reference to a skill's `SKILL.md`. See the [agent setup guide](AGENT_GUIDE.md).

## What are “acceptance criteria”?

They are plain-language conditions that tell you what must be true for a request to be considered complete.

For example, a request to download a table might say: “The downloaded file must keep the row order shown on screen.” Intentline helps turn the original request into checkable statements like that, while separating questions that still need a decision. It **does not test whether the software already meets them**.

## Can I try it without Python?

Yes. For an exploratory first attempt, ask `intentline-plan` for a **provisional, unsaved** checklist. The assistant should be transparent about any missing original source or context.

For reviewing, creating, or updating tracker issues with `intentline-issue`, the separate Python package is **not required**. Your assistant instead needs access to that tracker.

## What if I want to save a plan?

A saved, source-bound Intentline plan uses a **separately installed Python 3.11+ package** and a safe local storage location. After installing the skill, a technical operator can install the package in an authorized environment:

```sh
python -m pip install git+https://github.com/grove/intentline.git
python -B -m intentline --help
```

Give the assistant the original request as a UTF-8 file when possible, and ask it to use an approved private or ignored folder. **Do not save private requests into a tracked/public repository directory.** The assistant cannot claim it preserved exact original wording if it only has a paraphrase.

The [step-by-step setup and manual example](ADVANCED.md#quick-start) and [agent guide](AGENT_GUIDE.md) explain the full workflow. Secure record storage is currently supported on POSIX systems; **Windows record storage is not supported**.


## What might the first plan look like?

Here is a **made-up illustration**, not a saved or approved plan.

**Original request:** “Let people download the table they're viewing, keeping the same row order.”

**Draft checklist:** When the table is sorted, the downloaded rows appear in that same order.

**Suggested check:** Sort a small sample table, download it, and compare the order (proposed, **NOT RUN**).

**Open question:** Does “the table they're viewing” exclude hidden rows? The request may need to settle that; the assistant should not silently invent an answer.

**Status:** **DRAFT** — no feature was implemented, tested, or approved.

## How do I check or divide an existing plan?

Use `intentline-audit` to compare a **saved acceptance plan** with its original request. The audit may record an advisory report in an authorized local work area; it does not approve the draft.

Use `intentline-slice` to consider smaller delivery tasks. A successful answer can be **NO SPLIT**. It does **not** create child GitHub issues, and recording the recommendation is a separate action.

See the [prompt cookbook](AGENT_PROMPTS.md) for exact requests.

## Can it create or update GitHub issues?

Yes, **only when you explicitly request the target and action**, and your assistant has suitable tracker tools and permissions. For example, use `intentline-issue` to review an issue without changing it, or explicitly ask to create **one** issue in a specified repository.

Reviewing never creates local files or modifies the tracker. Creating/updating a tracker issue does **not** also create or update a saved Intentline plan. Other trackers, such as Jira and Linear, depend on the host's existing tools and access; installing Intentline does not connect them.

## Does it approve a feature or write its code?

No. A plan is a **draft**, a review is **advice**, and an issue is a **work item**. None is proof that the feature works, and none grants permission to implement or deploy it.

If you want an investigation of *existing implementation code*, [Gapline](https://github.com/grove/gapline) is a separate optional skill for that purpose.

## My request changed. Should I start over?

Tell `intentline-plan` about the **actual new request** and the earlier saved plan. Its amendment workflow can keep a record of which requirements changed and which stayed. It does not silently overwrite the original or update GitHub tickets. The [amendment prompt](AGENT_PROMPTS.md#5-reconcile-a-changed-request-with-an-existing-saved-draft) shows what to ask.
