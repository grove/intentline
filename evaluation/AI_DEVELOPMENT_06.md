# AI-only development record, version 1

This separate, read-only lane is **AI-only development, unverified human
independence**. It never creates `human_independent` or formal `eligible` records.
The seven adverse dimensions retain `rubric_02.md` semantics. The production CLI,
schemas, formal evaluators and historical evidence are unchanged.

The operator supplies a private root and a separately retained registration hash:

```
python -B -m evaluation.ai_development_06 report /private/study/study.json \
  --private-root /private/study --registration-sha256 <sealed-registration-digest>
```

`validate`, `assess`, `report` only read. They never dispatch, install, execute Git,
write, or contact a network/model. The CLI emits fixed aggregates or a fixed error,
never caller text/IDs/paths. Use `-B` to disable Python import-cache writes. POSIX
descriptor-relative storage is required; Windows returns exit 3 before record I/O.
Nonempty packets must have an owner-only root. This does not isolate same-user
agents. Canonical UTF-8 JSON, exact fields, bounded lists, 2 MiB single-link regular
files, no symlink components, absolute/traversing/Windows-style paths are required.

## Exact types

All objects below have exactly the listed keys. `ref` is `{path, sha256, size,
kind}`; size is an integer 1..2097152. Each ref binds bytes relative to the secure
root. Kinds and compartments are in `KINDS` in the adapter. Null is explicit;
missing or unknown measurements cannot become zero. IDs are opaque ASCII tokens,
not participant names, arm labels or paths. Arrays are bounded by the adapter.

The study keys are `record` (`intentline.ai-development-study`), `schema_version`
(integer 1), `mode` (`ai_only_development`), `phase` (`development`), `registered_at`
(offset-aware ISO timestamp), `registration` (ref), `arms`, `tasks`, `population`,
`assignments`, `judge_calibration`, `isolation`, `preparation`, `blockers`, `decision`,
`authorization` (null or externally supplied bounded grant ref).
`blockers` contains fixed codes only: budget, host, isolation, sources, calibration.
`decision` is insufficient_or_unqualified_evidence, fix_specific_defect,
simplify_overhead or expand_new_tasks; it is a declared development choice.

Registration bytes contain exactly `registered_at, arms, tasks, population,
judge_protocol, isolation_policy, authorization`. These equal the calibration
protocol ref, isolation mode and grant ref. Registration SHA equals the operator pin;
changing reference bytes and rehashing the study cannot bypass that pin. Changing
the pin is a new registration, never an amendment to observed results.

`arms` has ordinary, intentline, p2p_plan_only. Each arm has `model_id, version,
reasoning, seconds, tools, differences, instructions`. Model strings/seconds may
be null only for unattempted offline work. Tools/differences are bounded strings;
all configuration except instruction tree/differences must be identical.
Instructions are one canonical ref to the entire frozen package, with linked
files captured in the external operator manifest; never a convenient excerpt.

Each task has `id, kind` (historical/authored_control), `repository` (owner/repo),
`commit` (40 lowercase hex), `license, provenance, request, context, reference,
critique, agents, source_decision, contamination`. License/provenance/request are
refs; context is an ordered array of refs. Request/context are the single identical
corpus for every arm. Reference/critique may be null before preparation finishes.
Source decision is checked/unreviewed. Contamination is retained as bounded private
text. Agents are AI role receipts, never formal author/checker/reviewer identities.

An agent receipt has `agent_role, model_id, run_or_session_id, environment_id,
context_access, timestamp, output, record`. Output is a nullable ref. Environment
may be null if unobserved; record
is a byte-bound receipt. Roles are researcher, drafter, oracle, critic, judge.
Context_access lists exact refs. It is declared provenance, not authentication.

A reference ledger has `record` (intentline.ai-obligation-ledger), `schema_version`
(1), `task, input_sha256s, obligations`. Each obligation has `id, source, scope,
severity` (material/critical), `observable, counterexample, uncertainty`
(resolved/contested), `binding` (bool). Source is `{sha256, line_start, line_end,
quote}` with exact UTF-8 logical lines. A critique has `task, reference_sha256,
input_sha256s, findings`; findings are private nonempty strings (empty list allowed).
Gold is AI-derived. Byte and quote validation cannot settle historical authority.

Population is the frozen ordered list of `{task, arm, blind_id}`. It must contain
every task×arm exactly once, opaque 32-hex blind IDs, no omitted adverse attempt.
An assignment has `task, arm, blind_id, state, inputs, output, neutral, mapping,
prompt, transcript, execution, scores, metrics`. State reuses planning_02.STATES.
Inputs equal the task corpus exactly. Non-not_run attempts need structured execution
receipts and prompt/transcript refs; failed/partial outputs are retained. Completed
needs output. Not_run has no artifacts/scores and all-null metrics plus blockers.

Execution ref parses to `{task, arm, blind_id, state, input_sha256s,
output_sha256, prompt_sha256, transcript_sha256, model_id, version, reasoning,
session_id, environment_id, started_at, finished_at, transport}`. Transport is
native_host/operator_import; times follow registration, and output null is explicit.
No opaque string, provider request count inferred from sessions, or fake native PASS
is execution provenance. Structured receipts remain externally unauthenticated.

Metrics have planning_02.METRICS plus `input_tokens, cached_input_tokens,
output_tokens, reasoning_tokens, manual_interventions`. Cached input is a subset
of input, reasoning a subset of output; total tokens = input+output when known.
Integer counts and finite nonnegative elapsed/USD are nullable. Cost has no guessed
pricing. Preparation, calibration and judging usage are separate from arm attempts;
all-in totals stay null unless every applicable component is known.

Isolation has `mode` (host-enforced/shared/unverified), `receipts` (refs). Effective
permissions/canaries must be captured before attempts. Receipt schema, judge/control,
neutral-output and score types are specified in JUDGE_CONTROLS_06.md. Shared or
unverified isolation always prevents qualification. Host-enforced declarations
alone do not pass; the external host must supply contextual negative canaries.

## Reports and limits

No attempts yields not_run with blockers or offline_prepared for registered offline
preparation. Actual attempts without passing source/host/calibration gates yield
ai_development_unqualified. Observed requires at least three historical tasks from
three repositories, checked source/AI gold/challenge, complete gates, and two blind
critics per scored output. Contested obligations/dissent remain unresolved.
Authored controls never meet historical cohort qualification.

The report keeps full denominators, per-task opaque numbered paired counts,
per-arm adverse counts, disagreements, all-attempt/success-only costs, calibration
errors and source-citation observations. It supplies no ranking or superiority test.
The Wilson helper is descriptive only. Evidence remains AI-derived and host
declarations are not authenticated by this validator. Partial/semantic/encoded gold
leakage, pretrained source knowledge and correlated critics remain limitations.
