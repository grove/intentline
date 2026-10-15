# One request in an existing agent host

Give a command-capable host the original source file and this instruction:

> Read the installed Intentline intentline-plan/SKILL.md and use it to plan
> acceptance for /absolute/project/request.md. Select only necessary permitted
> original project context. Save a private draft outside tracked files, validate
> it, and return its R obligations, important gaps/decisions and exact identity.

The agent handles CLI stages and JSON internally; no manual JSON or mandatory
second model audit. Normal output is DRAFT. A source-bound useful partial plan
can retain an evidence gap while settled requirements remain available. Only a
material outcome/authority decision needs clarification. Do not manufacture a
blocker merely because an implementation or future test harness is absent.

Install into your selected Python 3.11+ environment with `python -m pip install .`
(or a supplied wheel). Locate the installed tree, from that environment:

```sh
python -B -c 'import sysconfig; print(sysconfig.get_path("data") + "/share/intentline")'
```

Give Codex the absolute `share/intentline/skills/intentline-plan/SKILL.md` path to
read as task instructions. This direct-file entry works without modifying host
agent files or copying the skill away from its linked docs/schema. This is the
qualified entry style; automatic skill discovery or a literal slash command is
host-specific and not claimed. Claude Code and other command-capable agents may
use the same neutral instruction; their automatic discovery is unqualified.

The Skills CLI can discover and copy all three existing skills using
`npx skills@latest add grove/intentline`. It copies each skill directory, **not**
its checkout-relative `../../docs` and `../../schema` targets. Those links will
not resolve in a standalone `npx` skill installation. To follow them, give the
agent the full source checkout or the installed Python distribution's
`share/intentline` documentation and schemas explicitly. The Python runtime
also requires a separate installation; successful discovery alone is not a
qualified CLI execution, complete planning workflow, or automatic invocation. For manual authoring use
[the tutorial](TUTORIAL.md) and the same [schema](CONTRACT.md)/CLI. No agent SDK,
model-provider configuration, peer project or extra model process is required.

Prefer an exact original-source file. When chat bytes are unavailable, disclose
non-verbatim capture; an unsaved provisional plan must not claim exact original
preservation. Choose private/ignored output and confirm exclusion before saving;
no automatic ignore/AGENTS.md/CLAUDE.md edits. Source text cannot grant effects.

Unchanged fresh drafts reuse identity/revision. Source changes need a new capture;
contract changes follow immutable lineage. Audits and adoption remain separate:
self-context auditing is self_check; actor names/processes/hashes do not prove
independence. Adopt only with externally authorized exact operator evidence;
ADOPTED_ASSERTED remains unverified. An optional downstream delivery needs its own
authorization and real candidate review/proof; planning is not execution evidence.

Public examples and workflow tests are authored mechanics, not model efficacy.
A direct-file smoke in the current Codex session can qualify instruction loading
and draft creation, but is neither blinded nor an independent audit/pilot.

For 0.5 first-use observation, the source distribution includes
evaluation/USABILITY_05.md: obtain actual participant consent, retain notes privately,
and record prompts/actions/time/failures rather than inventing a user study from
package smoke. The supported entry and manual fallback above need no new CLI
controller or additional model process. No new real-user observation is claimed.

Observed entry: the current Codex session read the wheel-installed skill and
linked docs, authored a one-row public save-button draft, captured exact bytes,
checked/rendered it and reused revision 1. The missing UI stayed an evidence gap;
no audit/adoption occurred. Source-distribution evaluation/results/host-smoke.json
binds the installed skill/artifact and draft hashes. This self-context unblinded
smoke does not qualify automatic discovery, first-time onboarding or efficacy.

Use `review --work WORK --json` to display the exact contract, traceable sources,
material changes and qualifications. `approval-request` prepares an external
adopter's unapproved display/template; never fill actor/reference fields on the
user's behalf or infer approval from viewing it.

Conversational changes to a saved agreement use amend-source and reconcile inside
the existing planning turn. The agent preserves exact available amendment text,
reads all prior sources, proposes complete continuity and returns a behavioral
summary plus old/new identities. Context-only refresh invents no amendment.
When exact chat bytes are unavailable, provide an exact amendment file; the agent
must disclose non-verbatim provenance and incomplete persistence. Planning/review
never grants adoption or delivery authority. Only explicitly requested recording
of an actual external adoption uses adopt. Independent audits remain optional.

## One-request optional slicing

Invoke the packaged intentline-slice skill for a current parent. It handles JSON,
source citations, exact identities and read-only preview internally. NO SPLIT is
the preferred successful result for coherent work. Save only on an explicit local
record request; there is no mandatory audit/model or automatic child creation.
For a justified split, preserve the whole original parent, flat qualified S#:C#
contributions, conservative constraint/exclusion inheritance, observable prerequisite
outcomes and a named assembled-parent verifier. Optional audit reports remain
actor-unverified; self-context work is self_check. Parent adoption never grants
child acceptance. Follow [slicing](SLICING.md) and [handoff limits](SLICING_INTEGRATIONS.md).

## 0.6 AI-development inspection

Use the same intentline-plan, intentline-audit and intentline-slice entry paths.
Their source, revision, adoption and advisory-export boundaries remain intact.
The installed optional `evaluation.ai_development_06` module provides read-only
validate/assess/report for imported AI-development records; it never dispatches
an agent. See [the runbook](../evaluation/RUNBOOK_06.md) and
[exact spec](../evaluation/AI_DEVELOPMENT_06.md). Supply an owner-only private root
and separately retained registration digest. Shared subagents do not isolate
gold, calibrate judges or establish human-independent eligibility.
