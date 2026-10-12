# Intentline 0.1

Turn an original request into a source-grounded acceptance agreement using an
existing coding assistant or manual JSON authoring. The offline Python CLI
preserves sources, validates structure and identity, and manages records.
It does not write semantic requirements, implement code, run proof, or approve work.

Python 3.11+; runtime dependencies: none. Install with `python -m pip install .`.
Use `intentline --help` or `python -B -m intentline --help`.

For one-request planning, give your command-capable assistant the original
request file and [the installed planning skill](skills/intentline-plan/SKILL.md):
“Use Intentline to plan acceptance for request.md; save and return a private draft.”
See [installed host entry](docs/AGENT_GUIDE.md). The agent handles JSON and CLI
stages; audit and adoption are separate. The [manual tutorial](docs/TUTORIAL.md)
works without an agent.
Optional review uses [the audit skill](skills/intentline-audit/SKILL.md).
Installed skills/docs are under your Python environment's `share/intentline/`.

Supported commands: `prepare`, `propose`, `check`, `render`, `status`,
`audit-record`, `adopt`, `export`. Each has `--help` and `--json`.

Secure record storage supports POSIX hosts with descriptor-relative no-follow
operations. Windows installation/help and safe filesystem refusal are supported;
Windows record storage is not yet qualified and returns exit 3.

See [trust boundaries](docs/TRUST_AND_AUTHORITY.md),
[development](docs/DEVELOPMENT.md), and the committed implementation plan.

Private work belongs in an ignored `.intentline/work/<slug>/`. Intentline never
edits project ignore files; explicitly ignore your work directory before use
in another repository. Captured sources can contain sensitive information.

[The scorecard](docs/SCORECARD_0.1.md) distinguishes measured offline engineering
from unmeasured model planning quality. Version 0.1.0 is an initial implementation;
no independent efficacy, authenticated review, or superiority claim is made.
