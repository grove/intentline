# Optional Proofline handoff and retained research

Current guidance is [the integration guide](../docs/INTEGRATIONS.md): Intentline
is an optional producer of structured promise data, using the existing versioned
`export --format json`. Ordinary coding and Proofline `check`/`status` need no
Intentline contract, second model, independent reviewer/prover or planning audit.
The optional consumer proposed in [Proofline #23](https://github.com/grove/proofline/issues/23)
was merged as [PR #27](https://github.com/grove/proofline/pull/27) at
`32b08893b71eed64e73199d1314f09d56a8a895d` on 13 October 2026.
Its generic evidence mapping comes from [#13](https://github.com/grove/proofline/issues/13).

## Current offline producer check

```sh
python -B -m unittest tests.test_export tests.test_export_json -v
python -B -m intentline --help
```

Focused authored fixtures check the existing single-original schema-1 JSON shape:
exact mixed-newline/Unicode source bytes and provenance, canonical contract/source
SHA-256 identities, stable R IDs and citations, boundaries, proposed oracle and
planned evidence, constraints/exclusions, explicit evidence gaps, authority labels,
secure storage and completion-marker-last recovery. CLI export is checked with
peer imports, subprocess execution and network access forbidden. No Proofline
runtime is installed, imported or executed by Intentline.

This is producer compatibility evidence, not a live check/candidate round trip.
Consumer tests and supported-host receipts are separately owned. The narrow
consumer rejects revised/multi-source/amended/native/child exports; producer
lineage must never be silently flattened. Neither an offline pass nor export
labels/hashes establish external authority or requirement satisfaction.

## Historical controller recipes and findings

The former `deliver`/`inspect-intentline` controller and mandatory reviewer/prover
acceptance path are retired. The following original instructions and evidence are
retained **as historical research only**, not commands to run against current
Proofline. No historical S0–S6 gate is reinstated for check-only use.

- [Original Intentline handoff guide at db6ab4f](https://github.com/grove/intentline/blob/db6ab4faf35accfb116eee3a4463d83e082f4b10/evaluation/PROOFLINE_HANDOFF.md)
  preserves the complete 0.2 direct and 0.5 native operator recipes and limitations.
- [0.2 consumer at c4d28e4](https://github.com/grove/proofline/blob/c4d28e4e743adbb261552323e694946f1360a129/README.md)
  pins the old direct parser/clean-tracked-checkout observation.
- [0.5 consumer at 023a3d5](https://github.com/grove/proofline/blob/023a3d5a380f4659b4459e585f1910604374d2a7/README.md)
  pins the old native caller-adoption path;
  [its S6 report](https://github.com/grove/proofline/blob/023a3d5a380f4659b4459e585f1910604374d2a7/docs/S6-RESULTS.md)
  reported 69/120 assigned runs executed, 51 unexecuted and one false acceptance.
- [0.6 follow-up at 46c503a](https://github.com/grove/proofline/blob/46c503ae23bef70ae410eac67f1b9e62bd1c62e3/docs/S6-FOLLOWUP.md)
  retains subsequent adverse trust findings. Consumer CI did not resolve them.

Existing `results/proofline-not-run.json`, `results/proofline-consumer-05.json`,
`results/proofline-native-05-not-run.json`, pinned test snapshots and frozen
baselines remain unchanged. They establish neither live native delivery nor
planning usefulness. `evaluation.handoff_02` retains historical input inspection
and opaque externally supplied evidence **unverified**; it does not execute a
consumer, authenticate receipts or replace current Proofline status.
