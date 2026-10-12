# Intentline: username\-validation

Status: **STRUCTURALLY\_VALID**. Preview / advisory; not authenticated approval or proof.

Contract SHA-256: `797c1eb6f35b4ebdc906be35ada59b05d2c39253fa6c2bf483704bc4762b71e0`

Source bundle SHA-256: `8e9119d2927e2e5114e9d1a9c1196b2b8cdad6b36a38fe7153f96112a3a1ecdb`

Revision: 1

Reject empty and whitespace\-only usernames

| ID | Required outcome | Basis / source | Boundaries | Seam | Oracle | Planned evidence | Plan state |
|---|---|---|---|---|---|---|---|
| R1 | Reject empty and whitespace\-only usernames | request: S1:1\-1 — Reject empty and whitespace\-only usernames | empty; spaces; tabs | public validation interface | validation error for empty/whitespace\-only usernames | call interface with empty, spaces, and tabs | planned |

## Constraints

None.

## Out of scope

None.

## Open decisions

None.

## Evidence gaps

None.

## Change notes

- \{&quot;kind&quot;: &quot;initial&quot;, &quot;revision&quot;: 1\}

## Selected sources

- S1 request: request\.md; SHA\-256 54962ec5ec269555068401d68869d652bbb6545333250593b07424bc6ba6241d; authority: user\_request
