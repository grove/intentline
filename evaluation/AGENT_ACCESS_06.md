# Effective access for the AI-only development workflow

Trusted host controls construct role-specific read-only views before models see
inputs. Codex subagents in one environment share files/tools; different names,
threads, prompts, owner-only sibling folders or Git worktrees are not security
domains. See [preparation](CODEX_PREPARATION_06.md) for exact role artifacts.

Use a private packet outside Git:

```text
sources/<task>/                 retained originals, license, chronology, retrievals
visible/<task>/                 exact common ordered arm corpus and digest manifest
restricted/gold/<task>/         AI-derived ledgers and every retained revision
restricted/critiques/<task>/    challenges and source-based reconciliation
runs/<arm>/<task>/              prompts, raw plans, failures, transcripts, usage
judging/<blind-id>/             blinded sources/plans and separate judge responses
receipts/                      grants, registrations, host capability and canaries
```

That layout aids retention only. Do not mount the whole packet in any model
environment. The trusted operator seals manifests and hashes after capture;
hashes bind bytes, not authenticity or isolation. Model output goes into a new
stage artifact; it cannot overwrite visible sources, old responses or registration.

## Access matrix

`R` means host-enforced exact enumerated input mount, `W` exclusively owned response
scratch, and `—` denied. A role's named subset never means recursive access.

| Role | Originals | Common corpus | Gold | Critiques | Arm outputs | Blind inputs | Output |
|---|---|---|---|---|---|---|---|
| Operator (nonmodel) | R | R | R | R | R | R | W sealed artifacts |
| Coordinator | metadata only | digest only | — | receipt digest | counts only | receipt digest | W coordinator response |
| Source researcher | R named historical subset | — | — | — | — | — | W source suitability |
| Task author | R named approved subset | — | — | — | — | — | W presentation description |
| AI obligation drafter | R same task originals | R sources only | — prior answers | — | — | — | W new ledger response |
| Adversarial challenger | R same task originals | R sources only | R ledger only | — prior critics | — | — | W challenge response |
| Planning arm | — retained/private originals | R identical task corpus | — | — | — other/previous arms | — | W own scratch/plan |
| Blind judge A/B | — retained/private originals | R identical task corpus | — | — | — raw/other judges | R one anonymized plan | W own response |

All model roles deny operator answer storage, another run's session/history/cache,
calibration expected answers, blind-to-arm mapping, repository/private history,
credential stores and unauthorized apps/MCP/network. Disable ambient skills,
AGENTS/config/hooks, history caches and inherited credentials that could expose
answers. Mount only the assigned complete skill tree for each planning arm.
Keep provider transport credentials outside model-visible compute where possible;
required model transport is not permission for model-command egress.

The trusted host retains effective user/container/environment identity, read/write
mount inventory, effective sandbox policy, tool inventory/config, credential
broker boundary, network policy and dispatcher policy. Record actual origins and
capture timestamps privately. An agent-declared path list or `isolated:true` is
not evidence of actual mounts. Unknown identity/config remains unverified.

## Executable sample canaries

The [operator-only probe module](cases/ai_06/access_canaries.py) is authored code,
not a host receipt. It never launches models or qualifies a host. Its network/app
functions belong in a separately permitted host preflight; the evaluation adapter
never invokes them. Ordinary CI tests exercise logic with mocks and nonsecret
files; those tests do not establish actual tool or network isolation.

Before probes, the trusted operator creates unique **nonsecret** sentinels and
seals a private inventory proving each negative sentinel exists in the real
restricted locations. Retain the positive sentinel's exact bytes/digest, negative
sentinel identities, container mount evidence, probe code hash and session/host
identity. Do not probe real gold, tokens or private outputs. The path list is a
probe target list, not an asserted mount inventory.

Run the following Python in the exact command surface available to that role,
with only these synthetic sentinel parameters supplied by the trusted host:

```python
from access_canaries import visible_canary, forbidden_canary, network_canary, summary

positive = visible_canary("/input/canaries/visible.txt", b"intentline-access-06\n")
forbidden = [
    forbidden_canary("/operator-private/canaries/gold.txt"),
    forbidden_canary("/operator-private/canaries/answers.txt"),
    forbidden_canary("/other-run/canaries/session.txt"),
    forbidden_canary("/judge-private/canaries/labels.txt"),
]
# host_ip/host_port are operator-owned endpoints, permitted only for this preflight.
network = network_canary(host_ip, host_port)
print(summary(positive, forbidden, network, connected_app))
```

Here `host_ip`, `host_port` and `connected_app` must come from the concrete
operator preflight, not guessed defaults. A private file successfully opened means
the access gate fails even without reading its contents. Only explicit permission
denial (`EACCES`/`EPERM`) passes that sample. `ENOENT`, symlink loop, timeout, refused
TCP connection or unavailable surface is **unresolved**, never a passed denial.
Masked mount views can therefore need additional trusted host mount evidence;
missing paths alone do not prove that an answer was inaccessible.

Probe outbound TCP from the model-command surface to a single controlled listener
that the operator independently confirms is reachable outside that boundary.
Send no payload. Never target public provider endpoints, real apps or arbitrary
external hosts. Host-only environment/provider transport remains separate. Sampled
denial must be supported by complete egress/firewall policy; one endpoint cannot
prove every destination or channel is denied.

For connected apps/MCP, run `connected_app_canary(real_host_dispatch)` through the
**actual same role tool dispatcher**, bound to a dedicated read-only synthetic
canary resource. The module invokes that callback with this exact request:

```json
{"resource":"intentline-access-06-nonsecret-sentinel","read_only":true}
```

The operator must bind the callback to the actual tool name/transport and record
its invocation, native denial, effective tool inventory and dispatcher policy.
Only a native policy refusal represented as `PermissionError` counts as that
sample. A callback returning success/data, missing callback/tool, disconnected
server, auth failure, not-found result, exception or operator-authored denial is
unresolved/failed. Do not construct a callback that merely raises PermissionError.
When all connected apps are absent by host policy, the trusted host supplies its
complete effective tool inventory and dispatcher denial witness; no absent-tool
unit test may substitute. If this host exposes no such pre-inference dispatch
surface, connected-app qualification is blocked.

Do these probes without model inference before a budgeted run. Then confirm the
role's shell, file tool, search, apps/MCP, remote dispatcher and session/history
surfaces have the same effective boundary. Shell-only probes cannot qualify other
surfaces. Probe every role's actual environment instance, retaining denials and
unexpected successes. If even one surface/instance remains unresolved, preserve
the receipt and stop qualified comparison; do not quietly broaden its access.

`sample_probes_passed:true` is sample evidence only, and `host_qualified` is always
false in this helper. A trusted operator must additionally substantiate effective
mount/tool/network/session restrictions. A host qualification receipt is still an
external assertion unless actually established; the offline evaluator cannot
authenticate it. A mock dispatch or caller-declared path inventory cannot promote
an unverified/shared host to observed isolated evidence.

## Current preparation boundary

CLI help/version inspection establishes interface facts only. Shared local
engineering subagents have shared filesystem/tools and no demonstrated restricted
mount or connected-app denial. No actual experiment host canary result is claimed
by these instructions or their unit tests. If actual separation cannot be shown,
mark model observations `ai_development_unqualified`; with no authorized inference
mark `not_run` and keep unknown usage null.
