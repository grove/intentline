# Frozen control and scoring types, version 1

These extend AI_DEVELOPMENT_06.md, using the unchanged seven-dimensional
rubric_02.md (SHA-256
`6f18178d3eec040e7072c98ed8c6875cc73055c84b369a44d31460c26461ecdd`).
All objects have exactly the listed fields; no arbitrary metadata reaches a judge.
The adapter reads already-produced artifacts. It never prepares a prompt or answer.

## Authored controls and qualification

`cases/ai_06/control-source.txt` and `authored-controls.json` are original public
authored fixtures, not historical requests, model outputs or calibrated judges.
They contain two equivalent positive representations and eight mutants: omission,
exclusion loss, wrong accepted/proposed authority, lost exception, candidate-derived
oracle, invention, missing gap disclosure and unnecessary harness blocker. The
second positive uses different order, wording and observations; format earns no
points. These examples qualify deterministic engineering only. Real calibration
requires source-grounded controls for **each selected historical task**, frozen
before any judge call or arm output. Never mount expected fields for a model.

Protocol keys: `record` (intentline.ai-judge-protocol), `schema_version` (1),
`control_version` (opaque revision), `registered_at`, `rubric_sha256`, `rules`
(instructions ref), `judge_config` (`model_id, version, reasoning`), `controls`.
Protocol is a private ref in the externally pinned registration. Rules and every
control must have a new identity/registration when changed; original failures stay.

Control keys: `id, task, category, inputs, plan, expected_dimensions, critical,
anchors`. Inputs equal the task's ordered corpus. Plan is a neutral ref; expected
dimensions are all seven bounded adverse integers, critical is bool, anchors are
exact source citations. Categories are positive_a, positive_b, omission, exclusion,
authority, exception, oracle, invention, gap, blocker. Each task needs all ten;
omission, exclusion, authority and exception must include critical seeds. Positive
expected counts are zero. Negative categories must seed their named dimension.
Blank or incomplete controls cannot qualify, even if declared status is observed.

Calibration keys: `status` (not_run/observed/failed), `protocol` (nullable ref),
`judges` (0..2 AI-role receipts), `receipts` (0..2 calibration refs), `metrics`,
`judging_metrics`. Each judge's context contains only original sources, neutral
control plans and rules. Protocol/expected answers, mapping, gold and other judge
responses are forbidden. Judges need distinct observed session/environment IDs.
Receipts parse to `judge_session_id, protocol_sha256, timestamp, predictions`.
Each prediction is `control_id, dimensions, critical, citations`. Missing/failed
predictions remain recorded and prevent qualification; unknown usage stays null.

Calibration gates require both complete fixed populations before planning, no
critical seeded miss, no positive alternative rejection, and correct source/row
citations. Counts per control, secondary dimension errors and cross-judge dissent
are computed from predictions, never inferred from authored expected fields.
This strict small smoke gate is not statistical calibration or AI independence.

## Lossless neutral representation

Raw imported plan keys: `branding` (arm label), `content`, `rows`, `exclusions`,
`uncertainty`. This is an evaluation transport representation, not a production
acceptance schema. Preserve the verbatim model response separately in transcript;
the operator's import must be auditable against it. Content cannot be hand-repaired.
Every row has `id, text, binding` (bool), `sources` (exact source anchors).
Unparseable model output remains an adverse/unfinished attempt with raw artifacts;
it cannot be made completed/clean by silently authoring missing acceptance rows.

Neutral plan has `blind_id, content, rows, exclusions, uncertainty`, exactly equal
to raw except for replacing the top-level branding with an opaque 32-hex ID.
No semantic text, exclusion or uncertainty can change. Visible approach branding
or unexpected fields refuses scoring; retain raw output as unqualified evidence.
Mapping is private: `blind_id, task, arm, raw_sha256, neutral_sha256,
removed_fields` (exactly `["branding"]`). Judges receive only neutral plans and
original sources. No filename/history/redaction metadata or hidden label map.
This strict import supports material-preserving records, not arbitrary automatic
prose parsing. Manual import fidelity and semantic answer leakage remain external
inspection responsibilities; byte comparison cannot authenticate that fidelity.

## Scores and bidirectional citations

Score keys: `blind_id, neutral_sha256, judge_session_id, timestamp, dimensions,
critical, adjudication, citations, coverage, row_support, context`.
Judge_session_id binds the calibrated judge profile. The context ref records the
actual fresh scoring session and environment separately: `session_id,
environment_id, judge_session_id, model_config, inputs, fresh_context, started_at`.
Inputs equal ordered originals + neutral plan + frozen rules. No other plans,
calibration answers, private gold, labels or previous scoring context. Sessions
cannot equal planners/calibrators or be reused for another output.

Citation keys: `source, output_ids, dimension, finding, severity, counterexample`.
Source is `{sha256, line_start, line_end, quote}`; source identity, exact quote
and output IDs must exist. Severity is coverage/material/critical. Coverage has
null counterexample; every adverse finding has a nonempty plausible counterexample.
The dimension count equals its adverse citations; every dimension has citations.
Critical bool must agree with critical citations. Adjudication is `state, reason`:
clear only with no critical citation; otherwise source_certain or contested.

Coverage entries: `obligation_id, output_ids, status, source`. Every ledger
obligation appears once with its exact anchor. Covered needs existing rows;
omitted needs empty rows and an omission/constraint-loss citation. A critical
ledger omission requires a critical finding; it cannot be downgraded to material.
Contested gold
must remain contested. Binding row support entries: `output_id, status, source`.
Every binding row appears once. Supported needs an anchor from that row; unsupported
needs null source and an invention finding; contested remains unresolved.

Two scores are retained independently. Worst dimension counts are descriptive;
different dimensions/coverage/support or critical states remain disagreement.
Contested gold, critic dissent and unresolved critical findings never count clean.
Only source-, host- and calibration-qualified records expose comparative adverse
counts/clean fractions; full assignment denominators include stopped/not_run runs.
No ranking, significance test or broad effectiveness percentage is produced.

## External grants, role and host records

Study adds `authorization` (null or grant ref) to the externally sealed registration.
Grant keys: `provider, models, max_cost_usd, subscription_limit, max_calls,
max_seconds, host_ids, source_sha256s, issued_at, authority`. Models contain exact
`model_id, version, reasoning`. Cost is nullable only with a declared subscription
bound. Calls/seconds are positive integers; all sources/environments/models must
be covered. Every known usage subtotal must fit the cap even when other usage is
unknown. This imports a declared grant; it neither authenticates operator consent
nor authorizes any dispatch. The trusted host must enforce real caps during runs. Attempted arms need a
positive frozen seconds horizon. Known execution timestamp durations and the
recorded first-role-start to last-role-finish span must fit the respective time
bounds even when reported elapsed usage is null.

AI role receipts add `output` (nullable artifact ref). Oracle context equals
originals only and output equals its ledger. Critic context equals originals plus
that ledger and output equals its critique. Role sessions must be distinct for
source qualification; no actor-declared independence/authenticated human field.
AI role records have nullable `version` and `reasoning` alongside `model_id`;
unknown or unapproved preparation configurations cannot qualify. Outstanding
critique findings prevent source qualification; retain prior challenges and actual
source-grounded resolution as distinct artifacts, never erase a dissent.
Each role also has `started_at`, preceding its `timestamp`; host checks precede
that start. Preparation/planner/calibration/scoring sessions and environments stay
distinct, with preparation roles included in access gates.

Host receipt keys: `environment_id, tested_at, canaries, permissions, witness`.
Canaries has exactly gold, other_arm, operator_answers, network, connected_apps;
each is denied/accessible/untested. Permissions is a host_policy ref; witness is
the exact host_witness artifact ref, not a loose digest or prose PASS.
Policy keys: `environment_id, read_sha256s, write_scope, tools, egress,
session_visibility, operator_separated`. Qualification needs own_scratch write
scope, denied egress, own_only sessions, true operator separation, all denied
canaries, and read/tool sets exactly matching that role's inputs. No duplicate
environment receipts can erase a failed canary. Tests must precede the role call;
judging mounts are established after the corresponding immutable output exists.
Grant, policy and witness are externally supplied, unauthenticated assertions.
The evaluator cannot certify a fake host witness or provider result as genuine.

All measurement fields are nullable nonnegative values bounded to 10^12; counts
are integers, cached input ⊆ input, reasoning ⊆ output, tokens=input+output when
all known. Preparation/calibration/scoring/all-attempt totals remain null until
every applicable component is known; known cap violations still refuse.
