# Intentline 0.4

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
`audit-record`, `adopt`, `export`, and optional `slice` commands. Each has `--help` and `--json`.

Secure record storage supports POSIX hosts with descriptor-relative no-follow
operations. Windows installation/help and safe filesystem refusal are supported;
Windows record storage is not yet qualified and returns exit 3.

See [trust boundaries](docs/TRUST_AND_AUTHORITY.md),
[development](docs/DEVELOPMENT.md), and the committed implementation plan.

Private work belongs in an ignored `.intentline/work/<slug>/`. Intentline never
edits project ignore files; explicitly ignore your work directory before use
in another repository. Captured sources can contain sensitive information.

[The 0.4 scorecard](docs/SCORECARD_0.4.md) separates tested engineering from
unmeasured usefulness. Version 0.4.0 is an engineering candidate in five stacked
PRs; merge and release publication require separate authorization.
The [0.3](docs/SCORECARD_0.3.md) and [0.2](docs/SCORECARD_0.2.md) evidence remains retained.

For optional sizing, ask your existing assistant to use
[the slicing skill](skills/intentline-slice/SKILL.md): “Decide whether this parent
needs slicing; preserve its full promise and return the smallest useful result.”
A correct **NO SPLIT** keeps the coherent agreement whole, explains direct delivery
and gives one next action, with no child files or mandatory extra audit/model.
When a concrete observable boundary earns another delivery cycle, **SPLIT_PROPOSED**
allocates every parent R to source-bound children and named parent integration
checks. Every child inherits constraints/exclusions; child success never proves
the parent. Explicitly request local recording or a child export when needed.
See [slicing/manual commands](docs/SLICING.md) and
[portable advisory handoff](docs/SLICING_INTEGRATIONS.md).


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
