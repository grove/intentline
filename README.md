# Intentline

**Turn a feature request into a clear checklist of what “done” means.**

Intentline helps your AI coding assistant explain what a feature should do, what matters most, and how someone could check the result—**before** anyone starts changing code.

It provides four skills. Pick the one that matches your task.

## 1. Install the skills

Open a terminal in your project and run:

```sh
npx skills@latest add grove/intentline
```

Follow the prompts to choose your coding assistant and the skills to install. The installer uses [Node.js and Git](docs/FAQ.md#what-do-i-need-to-install).

## 2. Tell your coding assistant what you need

| Skill | Ask it to… |
| --- | --- |
| **`intentline-plan`** | Turn a feature request into clear acceptance criteria (a checklist of what should work) |
| **`intentline-audit`** | Check a **saved Intentline plan** against the original request |
| **`intentline-slice`** | Decide whether a **saved plan** should stay as one task or be split into smaller ones |
| **`intentline-issue`** | Review, create, or improve an issue in GitHub or another issue tracker your assistant can access |

**Try planning a feature:**

```text
Use intentline-plan to suggest a simple checklist of what
must work for this feature:

"Let people download the table they're viewing as a CSV file,
keeping the same row order."

For now, show me a provisional plan. Don't save files,
change code, or approve anything.
```

**Or improve an existing GitHub issue:**

```text
Use intentline-issue to review this GitHub issue:
https://github.com/ORG/REPO/issues/123

Suggest clearer acceptance criteria. Don't edit the issue.
```

Replace the example link with yours. **Creating or updating** a GitHub issue is a separate request: say exactly which issue or repository to change. Your assistant must already have permission to access it.

To **save** an Intentline plan, or work with saved plans using `intentline-audit` and `intentline-slice`, you also need the [Intentline Python setup](docs/FAQ.md#what-if-i-want-to-save-a-plan). You can try an unsaved plan without it.

## 3. What happens next?

You'll get a draft checklist, suggestions, or a proposed breakdown of work. You can discuss and revise it with your assistant.

**Intentline does not implement features, run tests, or approve work for you.** A suggested check is not proof that the software works.

## More help

- **[Try a complete first plan](docs/FIRST_USE.md)** — an original request, sample checklist, and what to do next.
- **[Which tool should I use?](docs/WHICH_TOOL.md)** — choose between Intentline, Gapline, Proofline, and Faultline.
- **[Copy-and-paste prompts](docs/AGENT_PROMPTS.md)** — real requests for each skill, including creating GitHub issues.
- **[Common questions and setup help](docs/FAQ.md)** — choosing a skill, saving plans, permissions, and troubleshooting.
- **[Detailed setup and technical background](docs/ADVANCED.md)** — command-line tools, record formats, and advanced workflows.

[Agent guide](docs/AGENT_GUIDE.md) · [Skill documentation](docs/AGENT_PROMPTS.md) · [License](LICENSE)
