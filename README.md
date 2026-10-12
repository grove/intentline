# Intentline 0.1

Turn an original request into a source-grounded acceptance agreement using an
existing coding assistant or manual JSON authoring. The offline Python CLI
preserves sources, validates structure and identity, and manages records.
It does not write semantic requirements, implement code, run proof, or approve work.

Python 3.11+; runtime dependencies: none. Install with `python -m pip install .`.
Use `intentline --help` or `python -B -m intentline --help`.

See [trust boundaries](docs/TRUST_AND_AUTHORITY.md),
[development](docs/DEVELOPMENT.md), and the committed implementation plan.

Private work belongs in an ignored `.intentline/work/<slug>/`. Intentline never
edits project ignore files; explicitly ignore your work directory before use
in another repository. Captured sources can contain sensitive information.
