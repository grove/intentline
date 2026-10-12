# Agent-neutral planning

Give the host the original request and `skills/intentline-plan/SKILL.md` as task
instructions. Codex and Claude Code can read the same document and call the same
CLI. Slash-command installation and fresh-context isolation depend on the host;
Intentline does not install hooks, modify AGENTS.md/CLAUDE.md, or orchestrate agents.
Manual authoring uses the identical contract schema and commands. The CLI has
zero model calls and does not automatically generate semantic requirements.

Start with one source and one planning pass. Return one concise agreement,
provenance, unresolved material decisions, and next action. An audit is optional;
if used, the host should supply a fresh context with the frozen exact revision
and original source. Same-context review must be labeled self_check. A different
actor name/process/hash alone cannot establish independent review.

Fixtures under examples are public illustrative inputs, not private user
captures or authenticated adoption. `good.template.json` and
`bad.template.json` use `SOURCE_BUNDLE_AT_PREPARE`; replace it with the real
prepare result before proposing. The example replay tests create actual byte-valid
records. Expected semantic findings are authored expectations, not model scores.
