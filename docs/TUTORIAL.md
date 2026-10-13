# First use (POSIX, Python 3.11+)

For the shortest agent-assisted path, follow [installed host entry](AGENT_GUIDE.md)
and give one instruction: “Use Intentline to plan acceptance for request.md; save
and return a private draft.” The host authors JSON and runs capture/propose/check/
render internally. No separate audit is required. The steps below are the manual
fallback; the example template is public authored material, not model evidence.

From this checkout, install: `python -m pip install .` (prefer your own virtual
environment). No GitHub, peer projects or model API is needed. The example is
public illustrative source. For real work preserve the exact user request in
your own selected file and ensure `.intentline/` is ignored; Intentline never
changes ignore files automatically.

Capture:

```sh
python -B -m intentline prepare \
  --source examples/username-validation/request.md \
  --out .intentline/work/tutorial --json
```

Author a draft manually or give `skills/intentline-plan/SKILL.md` to your existing
assistant. This example copies an already authored template and fills only its
real source identity; the CLI never synthesizes acceptance requirements:

```sh
python -B - <<'PY'
import hashlib, json
from pathlib import Path
work = Path('.intentline/work/tutorial')
draft = json.loads(Path('examples/username-validation/good.template.json').read_text())
draft['source_bundle_sha256'] = hashlib.sha256((work / 'source-manifest.json').read_bytes()).hexdigest()
(work / 'draft.json').write_text(json.dumps(draft, indent=2) + '\n')
PY
python -B -m intentline propose --work .intentline/work/tutorial \
  --draft .intentline/work/tutorial/draft.json --json
python -B -m intentline check --work .intentline/work/tutorial
python -B -m intentline render --work .intentline/work/tutorial
python -B -m intentline status --work .intentline/work/tutorial --json
```

Read the original source and rendered draft. STRUCTURALLY_VALID does not mean
semantically complete or approved. It is useful as planning context immediately.
Different credible observation methods can establish the same outcome; named
evidence remains a suggestion unless the source mandates it.

For consequential work, optionally give the exact source, saved revision and
hashes to a fresh host context using `skills/intentline-audit/SKILL.md`.
Record its actual report using `audit-record --work ... --report audit.json`.
Without actual isolation, label self_check or unverified_independence. A ready
report is advice for adoption, not adoption. No synthetic report in the examples
is an independent review.

Only after actual external user/project-authority adoption, supply approval.json:

```json
{
  "record": "intentline.approval",
  "schema_version": 1,
  "contract_sha256": "EXACT_HASH_FROM_STATUS",
  "source_bundle_sha256": "EXACT_HASH_FROM_STATUS",
  "actor": "ACTUAL_ADOPTING_ACTOR",
  "timestamp": "ACTUAL_ISO8601_TIMESTAMP_WITH_OFFSET",
  "reference": "ACTUAL_EXTERNAL_ADOPTION_RECORD",
  "record_bytes_utf8": "ACTUAL_RECORD_BYTES_WHERE_AVAILABLE"
}
```

Placeholders are intentionally invalid. Do not generate an approval on behalf
of the actor. record_bytes_utf8 is optional when original reference bytes are
unavailable; say so externally. Intentline preserves exact approval-file bytes,
checks binding, and records only operator_asserted with authentication unverified:

```sh
python -B -m intentline adopt --work .intentline/work/tutorial \
  --expected-contract-sha256 EXACT_HASH_FROM_STATUS --approval-file approval.json
```

Export can also use the fresh unadopted draft as advisory promise data:

```sh
python -B -m intentline export --work .intentline/work/tutorial \
  --format json --out .intentline/handoff/tutorial
```

The handoff has byte-exact source-S1.txt, canonical contract.json with stable R1,
the source manifest and a final completion marker with output hashes. It does not
invoke Proofline or authorize execution. Continue ordinary coding, then optionally
pass selected executable checks to Proofline's check-only path. Intentline is
unnecessary when no contract is wanted. See [integration limits](INTEGRATIONS.md).

Try negative examples in a separate work directory: no-harness produces an
honest evidence gap; unclear-outcome remains BLOCKED; tampering's bad template
fails duplicate-ID validation. Semantic bad drafts can pass structural checks;
inspect their meaning against the full source. Changing/removing the original source makes status
STALE and adopt/export exit 2, retaining historical records. Never patch saved
snapshots or mutate an old revision to bypass freshness.

For a wheel-only install, locate share/intentline with the command in the agent
guide. Use its absolute examples/username-validation/request.md/template paths,
set --root to that installed share/intentline tree, and choose a private --out
outside it. Skills, all referenced docs/schema and this public example ship in
both wheel and source distribution; a repository checkout is not needed.

For example, “Reject empty usernames” yields a DRAFT rejection obligation. An
optional audit may advise READY_FOR_ADOPTION, and explicit externally authorized
operator evidence may yield ADOPTED_ASSERTED; neither executes the behavior.
Separately authorized executable checks can supply limited evidence against a
frozen candidate. Green checks do not prove every requirement or source coverage.

To amend an existing work item, write the exact new request in amendment.md and
ask the planning skill to preserve the existing agreement and propose a successor.
It uses amend-source, authors schema-1 JSON plus continuity-v1, and runs reconcile
and review. Your old work is immutable. Inspect the original and amendment chain,
changed/retired/new obligations and exact hash through review. approval-request
returns an unapproved display/template; supply a real external adoption reference
only after the exact successor has actually been adopted. No flag grants approval.
