# Intentline 0.3

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
`review`, `approval-request`, `amend-source`, `reconcile`, `inspect-native`,
`audit-record`, `adopt`, `export`. Each has `--help` and `--json`.

Secure record storage supports POSIX hosts with descriptor-relative no-follow
operations. Windows installation/help and safe filesystem refusal are supported;
Windows record storage is not yet qualified and returns exit 3.

See [trust boundaries](docs/TRUST_AND_AUTHORITY.md),
[development](docs/DEVELOPMENT.md), and the committed implementation plan.

Private work belongs in an ignored `.intentline/work/<slug>/`. Intentline never
edits project ignore files; explicitly ignore your work directory before use
in another repository. Captured sources can contain sensitive information.

[The 0.3 scorecard](docs/SCORECARD_0.3.md) separates offline engineering results
from unmeasured planning quality. Version 0.3.0 is an engineering release
candidate in open dependent PRs; merge and release publication remain pending.
The [0.2 evidence](docs/SCORECARD_0.2.md) remains unchanged.

Review shows the current full agreement, exact source identities, gaps, disputes
and mechanical revision/lineage differences. Viewing and `approval-request`
never adopt. A conversational amendment creates a distinct successor with frozen
original request and chronological exact amendments, freshly selected context,
explicit per-obligation continuity and a new exact adoption boundary. Context
refresh needs no invented user amendment. Old approval assertions stay historical.

`proofline-native` exports a portable, versioned full contract/source/lineage
bundle with standalone inspection. The separately owned experimental Proofline
adapter requires its own caller adoption for exact contract/source-chain/bundle
hashes before dispatch. Native export is not execution permission. Direct brief
export remains supported for original work; successors require native/JSON/
Markdown rather than a misleading concatenated direct request.

Optional: [advisory Lore reports](docs/LORE_CONTEXT.md),
[direct Proofline handoff](docs/INTEGRATIONS.md), and the source-distribution
[evaluation protocol](evaluation/README.md). All peers remain optional. The
acceptance/result schema 1 and existing CLI behavior remain compatible.
