# Status

[Version 1.0.0](https://github.com/DannyExperiments/projective-plane-flags-no-common-opposite/releases/tag/v1.0.0) · 27 November 2026 · [Version DOI](https://doi.org/10.5281/zenodo.24567310)

The classification uses the classical Blokhuis–Wilbrink nucleus bound. Classification in arbitrary non-Desarguesian planes remains outside this result.

Internal mathematical review covered the stated result and its scope. External peer review has not been conducted. The replay checks the small-order construction, exhaustively checks orders 2 and 3, and checks order 4 through flag transitivity.

The repository verification, replay and PDF build workflows succeeded on the [reviewed commit](https://github.com/DannyExperiments/projective-plane-flags-no-common-opposite/commit/086978973a336faf1788c4300dd6aab7f2b6b1c3). See the [literature and priority audit](audits/public_safe_reports/LITERATURE.md).

The current main branch adds [a scoped Lean certificate](formalization/README.md). Lean proves that the constructed family has incident flags, has no common opposite, and has noncollinear point entries and nonconcurrent line entries given a third suitable point on the base line. The proof uses incidence, a chosen join with uniqueness for distinct points and a common point for each pair of lines. It works at arbitrary order. The finite cardinality of the family, the existence of the starting data at each order, the order-two analysis and the Desarguesian classification and count are in the paper.
