# Blinded semantic rubric, revision 1

Score source truth rather than schema style, verbosity or a checker's preferred
implementation. Map each material source promise to output IDs; map each binding
output obligation/exclusion back to original sources. Retain disagreements and
citation corrections. Record nonnegative adverse finding counts for every field:

| Field | Count |
|---|---|
| material_omissions | Original material promises omitted or narrowed |
| invented_obligations | Unsupported requirements or exclusions |
| constraint_losses | Applicable constraints, lifecycle or scoped exceptions lost |
| decision_errors | Wrong authority, scope or settled/ambiguous interpretation |
| weak_oracles | Expected answer mirrors candidate; no credible falsifier/negative case |
| missing_gap_disclosures | Material unavailable evidence silently presented as planned |
| unnecessary_blockers | Settled outcomes blocked for missing harness or routine detail |

Each score also includes citations for coverage and findings, original-source
digests/lines and substantive output IDs. Empty output_ids can describe an omitted
promise. All dimensions are mandatory, even when zero. Review task provenance
before scoring; do not tune reference answers after observing results.

Record agent/user actions, elapsed wall time, model calls, reported tokens/cost
when available (null otherwise). Include failed attempts, installation/preparation,
audit and correction effort. No token/cost percentage claim from unknown bills.
A pilot diagnoses failures; separately registered untouched held-out tasks and
appropriate paired uncertainty estimates are needed for efficacy claims.
