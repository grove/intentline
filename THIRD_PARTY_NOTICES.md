# Adapted planning principles

Intentline is Apache-2.0. Its skills and contract design selectively adapt the
spec envelope, stable requirement identity, source preservation, independent
oracles, and authority separation described in Promise to Proof (Apache-2.0),
copyright its contributors, revisions `a26e0a9c50a7d75fc3a02feda491bf497de94cf4` (0.1) and
`17f3deb982a8224f71b12bda74be6b24d86571e4` (0.2 selective clarification).
Sources: `skills/productivity/plan-acceptance/SKILL.md`,
`skills/productivity/audit-acceptance/SKILL.md`,
`docs/acceptance-contract-protocol.md`.
Adapted Intentline files: `docs/CONTRACT.md`, `docs/TRUST_AND_AUTHORITY.md`,
`skills/intentline-plan/SKILL.md`, `skills/intentline-audit/SKILL.md`.
No P2P controller or runtime code is copied or imported.

Compatibility inspection pins (not runtime dependencies):
Proofline `c4d28e4e743adbb261552323e694946f1360a129`;
Lore `55ee9830e38fe869669376a089c9fbd4dddca43c`.
All three upstream main identities rechecked on 2026-10-12.

`tests/compatibility/proofline_direct_parser.py` extracts Proofline's exact
`criterion_ids` function from pinned `proofline.py` (Apache-2.0, copyright
Proofline contributors). Its surrounding imports/exception are offline test
scaffolding. Full upstream file and function digests are retained in
`tests/compatibility/identity.json`. This file is test-only, never a runtime import.
