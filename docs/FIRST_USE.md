# Your first Intentline plan: a complete example

**Turn a one-sentence feature request into a useful checklist, without writing code.** This first try works with the `intentline-plan` skill in your coding assistant. You can keep the result **provisional and unsaved**—no Intentline Python setup is necessary for that exploratory step.

This walkthrough uses an [actual sample request checked into the Intentline repository](../examples/username-validation/request.md). The example response below is **written for this guide**, **not** an agent transcript or a saved, approved, or tested plan. Your assistant's wording may differ.

```text
Your original request → Your prompt → Draft checklist → Your next decision
```

## 1. Start with the original request

Here is the **complete request**:

> Reject empty and whitespace-only usernames

You might say this while planning a sign-up form. It expresses an outcome, but not every implementation detail. Intentline helps make the promise checkable without inventing extra requirements.

## 2. Install the planning skill

In your project directory, open a terminal and run:

```sh
npx skills@latest add grove/intentline --skill intentline-plan
```

Choose your coding assistant when prompted. Now switch to **the assistant's chat**, not the terminal.

## 3. Copy this prompt into your coding assistant

```text
Use intentline-plan to give me a provisional, UNSAVED
acceptance checklist for this exact request:

"Reject empty and whitespace-only usernames"

Show the intended outcome, examples that would check it,
anything important the request doesn't settle, and the
next decision I should make.

Do not save files or create an Intentline record. Don't
write implementation code, run tests, approve work, or
create GitHub issues.
```

The original request is included so you can try this without preparing a file. Since this is an **unsaved** proposal, do not expect exact original-source hashes or a permanent acceptance record.

## 4. Here's an example of what the assistant might say

**Illustrative response — not an actual Intentline run**

> **Status: PROVISIONAL / UNSAVED** — not an approved or tested plan.
>
> **What the request promises:** A username consisting of no characters, or of whitespace alone, should be rejected.
>
> **R1 — Acceptance criterion:** Reject empty and whitespace-only usernames.
>
> **Examples to check (PROPOSED — NOT RUN):**
> - An empty username (`""`) is rejected.
> - A username containing only spaces (`"   "`) is rejected.
>
> **Not specified by the request:** The exact error wording, where the error appears, or other username rules. Don't add those as requirements without more source information.
>
> **Next action:** Review the checklist and decide whether to keep a saved draft. Decide on error wording only if that matters for the feature.

Notice the distinction: **R1 repeats what was requested**; the example checks make that request observable; unknown details remain **unknown**. It does not claim that the current application rejects these inputs or that tests have been run.

## 5. What should you do next?

1. **Check the checklist.** Does it capture your request without adding features or restrictions you didn't ask for?
2. **Answer only important open questions.** If error wording matters, supply that as a new instruction. If it doesn't, there's no need to invent a rule.
3. **Decide whether to keep a formal saved draft.** Saved, source-bound plans need the **separate Python 3.11+ Intentline runtime**, the original request in a file, and a permitted private storage location. See [how to save a plan](FAQ.md#what-if-i-want-to-save-a-plan). Don't silently turn this provisional example into a saved agreement.
4. **Want a GitHub issue instead?** Ask the separate `intentline-issue` skill to review or draft one. Publishing **one issue** requires a specific repository and an explicit CREATE request with host access; it doesn't happen during planning.

The same pattern works for your own requests. Paste your real words, request a provisional plan, review it, and save only if you need a durable record.

**Next:** Explore the [prompt cookbook](AGENT_PROMPTS.md) for issue review, saved planning and more, or read [Which tool should I use?](WHICH_TOOL.md) for Intentline, Gapline, Proofline, and Faultline.
