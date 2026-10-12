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

`tests/compatibility/proofline_checkout.py` extracts exact `git_bytes`,
`capture_base` and `validate_links` from the same pinned Apache-2.0 Proofline file.
Function/file digests are in `tests/compatibility/checkout-identity.json`; its
OfflineGit shim is test scaffolding, never a runtime peer or host/model emulator.

The test-only tests/compatibility/proofline_native_input.py byte snapshot comes
from grove/proofline 2285a434c1c33e73f8d89a6c3267abcaa37e9b95, checks/intentline_input.py,
Apache-2.0 (Copyright 2026 Proofline contributors). Its pinned identity records
shared producer-validator ancestry; no independent review is claimed. The snapshot
is not installed/imported by the Intentline runtime and performs no inference.

0.4 selectively adapts NO SPLIT, outcome sizing, bidirectional allocation, credible
merges, observable prerequisites and assembled-parent ownership from Promise to
Proof `skills/productivity/slice-contract/SKILL.md`, Apache-2.0, copyright its
contributors, at `17f3deb982a8224f71b12bda74be6b24d86571e4`. Adapted files:
`skills/intentline-slice/SKILL.md`, the optional slicing audit section in
`skills/intentline-audit/SKILL.md`, `docs/SLICING.md`, `docs/SLICING_INTEGRATIONS.md`
and the advisory allocation design. No issue topology, delivery orchestration,
tracker controller or runtime code is imported. The referenced public skill SHA-256
is `de3c8238c0f19f462853876ec0d8577aeb9f0a8b79ef9df76420f94020014976`.

Proofline main `5ab3ff193f3d5d665645d704d9d6d7e410865b91` was rechecked for 0.4. Its
`checks/intentline_input.py` bytes match the retained 0.3 test snapshot exactly;
that snapshot remains test-only. This byte comparison and offline negative
consumer tests do not qualify child delivery or constitute independent review.
