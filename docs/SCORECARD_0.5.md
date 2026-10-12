# Intentline 0.5 engineering and empirical scorecard

Observed 12 October 2026. Starting/final committed HEAD currently remains
`587ef061287f02d4d7328f7c291bf57b85892603`; local changes are on
`implement/05-engineering`, uncommitted and unpublished. No release/tag/merge,
package publication or inference was performed. The package remains 0.4.0 until
the engineering gates, including exact-head CI, pass with publication authority.

| Measurement | Status | Evidence / limitation |
|---|---|---|
| Starting 0.4 suite | passed | 120 tests on macOS/Python 3.14.8 and standalone 3.11.17; 119 pass, one actual-Windows probe skipped |
| Starting exact-head CI | passed | [38258294929](https://github.com/grove/intentline/actions/runs/38258294929), Linux/macOS/Windows × Python 3.11/3.14 |
| 0.5 full local regression | passed | 136 tests on macOS/Python 3.11.17 and 3.14.8; 135 pass, one actual-Windows probe skipped |
| Fresh wheel/sdist install | passed locally | Both supported local Python versions; whole skills/docs/schema and manual workflows; final artifact receipts retained outside the distribution |
| 0.5 exact-head six-cell CI | not_run | No authorized committed/pushed 0.5 head exists |
| Secure Windows record storage | unsupported | Existing exit 3 before I/O retained; green install/API-probe jobs do not qualify storage |
| Independent planning pilot | blocked_external | 9 private selected candidates, 0 eligible, 0 registered/executed; 2 explicitly AI-authored requests excluded and retained |
| Independent slicing pilot | blocked_external | 4 private provisional source-bound parents, 0 independently eligible; 0 registered/executed |
| First-use human observation | not_run | Consent/observer protocol prepared; no participant or measured friction |
| Real installed-agent 0.5 run | not_run | Offline package fixtures and old self-context smokes are separate |
| Native Proofline delivery | blocked_trust_gate | Current S6 false acceptance; no independently established remediation/native qualification or task-specific adoption/host/budget grant |
| Authenticated authors/reviews/adoption | unverified | No independent role captures supplied; hashes/actor declarations do not authenticate |
| Billed USD, real-model tokens and all-in human cost | unknown | No observed comparative runs; missing measures remain null |
| Untouched holdout | not_run | No holdout registration or lookup; shortlist research is development exposure |

Engineering decision: **local checks passed; release qualification pending**. Frozen
0.4 source/output/evidence bytes, existing security/authority/compatibility guards
and deterministic intake/recording repairs are maintained. Local validation
and unavailable exact-head remote CI remain distinct. Preparing source/package artifacts
does not authorize publishing or changing the release version.

Empirical decision: **unmeasured / blocked_external**. The 0.5 usefulness objective
is unmet. No improvement, superiority, savings, independent planning quality,
first-time usability or safely verified native delivery is claimed. A small genuine
matched pilot would still be diagnostic; broad claims require a separately frozen
untouched holdout and adequate independent evidence. Consumer trust defects are a
material stop independently of engineering CI.

See [implementation and validation details](IMPLEMENTATION_0.5.md), the source
distribution's evaluation/INTAKE_05.md, SLICING_05.md, USABILITY_05.md and
PROOFLINE_HANDOFF.md. Dated 0.1–0.4 scorecards and receipts remain byte-identical.
