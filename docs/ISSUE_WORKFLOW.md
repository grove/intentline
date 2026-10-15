# GitHub issues with intentline-issue

`intentline-issue` is an optional **agent skill** for working with GitHub
issues, not an Intentline Python CLI subcommand or a new GitHub service.
An existing GitHub-connected coding agent supplies the read/write tools.

## Use one of three modes

| Request | Result | GitHub write |
| --- | --- | --- |
| "Review grove/intentline#123 for missed acceptance criteria" | Propose a clearer body or targeted changes | No |
| "Create a GitHub issue in grove/intentline for CSV export" | Publish one source-grounded issue | Yes, if authorized |
| "Improve grove/intentline#123 and update it" | Refine only the existing issue's acceptance content | Yes, if authorized |

The request to create or update is sufficient authorization **for that
issue**, not permission to edit unrelated issues, assign maintainers,
change labels/state, create PRs, or implement code. No mandatory external
audit, second model or approval workflow.

## Example issue text

The following is illustrative, not evidence about an actual request:

```markdown
## Goal
Let users export the current table to CSV.

## Acceptance criteria (proposed)
- [ ] R1: Export contains every currently visible row in the same order.
- [ ] R2: Fields containing commas or quotes remain readable by a CSV parser.

## Verification (planned)
- R1: Export a known ordered table and independently compare its rows.
- R2: Export a field containing a comma and quote; independently parse it.
```

Only include each outcome when supported by the real issue or an
essential consequence of the promised format. Don't invent features,
preferred libraries, speculative exclusions, or an arbitrary test quota.
Planned verification is **not** proof that tests have run.

For an existing issue, read its live title/body and relevant comments;
preserve still-binding scope, decisions, constraints and useful context.
Comments may provide evidence but don't automatically authenticate
approval. If acceptance criteria already cover the promise, make no
cosmetic-only update. Avoid appending duplicate acceptance sections.

## Install and run

```sh
npx skills@latest add grove/intentline --skill intentline-issue
```

The installer only copies **agent instructions**, not GitHub credentials,
`docs/`, `schema/`, or the Intentline Python runtime. Your agent
needs GitHub read access to REVIEW and write access to CREATE/UPDATE.
If it lacks access, return the issue draft/diff and **NOT PUBLISHED**
instead of inventing an issue URL.

An optional separately installed Python 3.11+ Intentline runtime can
save a source-bound acceptance **DRAFT** by following the existing
`intentline-plan` process. Private captures must remain owner-only
and untracked. A SHA-256 hash cannot authenticate GitHub authority.
No saved contract is required merely to create or update an issue.

The portable `intentline-issue/SKILL.md` and packaged
`skills/intentline-issue/SKILL.md` should be byte-identical, enforced
by repository tests. The original three Python-package skills and
frozen evaluation baselines stay unchanged.

## Safe sequence

1. Read the exact issue/request and only relevant repo context.
2. Prepare concise, falsifiable and source-grounded acceptance outcomes.
3. REVIEW only returns a draft. CREATE checks the destination and creates
   one issue. UPDATE re-reads before writing, preserves unrelated text,
   and never assumes the check was an atomic concurrency guard.
4. Return the real GitHub URL only after a confirmed write; otherwise
   report REVIEW-ONLY, UNCHANGED, or NOT PUBLISHED.

These are **authored instructions and deterministic packaging checks**;
they do not establish an observed real-agent success rate.
