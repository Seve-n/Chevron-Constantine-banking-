# Methodology

This project follows a Business Analyst workflow end to end, from a business problem statement
to shipped-ready requirements, rather than starting from a dataset and working backward to find
"interesting" charts. This document explains that workflow, the tools used at each stage, and the
principles that were enforced throughout to keep the project honest and internally consistent.

## Workflow

```text
Business Problem → Business Questions → Data Requirements → Data Generation
    → Data Cleaning → Data Analysis (Python + SQL) → Business Insights
    → Recommendations Roadmap → Functional Requirements → User Stories
    → To-Be Process → Dashboard Specification → Final Report
```

Each arrow is a phase in this project (see the table in [../README.md](../README.md)), and each
phase produced a standalone, reviewable deliverable before the next one started. That's
deliberately slower than jumping straight to "build a dashboard," because a Business Analyst's
job is the framing and the traceability between steps, not just the end artifact.

## Why a synthetic dataset

This project simulates a fictional bank (Chevron Constantine Banking) with a Python-generated dataset rather than
using a public dataset, for two reasons:

1. **Control over the narrative for teaching purposes.** The generation script
   (`python/data_generation.py`) encodes deliberate, documented hypotheses (e.g. `credit_application`
   should be harder than `bank_transfer` because it has more steps and an external check) so that
   the analysis phase has real, interpretable patterns to *discover*, mirroring how a real BA
   engagement starts from stakeholder hypotheses, not a blank slate.
2. **No real banking data risk.** Belfius data protection requirements make using any real
   financial data for a portfolio project a non-starter. A synthetic, clearly-labeled dataset
   avoids that risk entirely while still producing realistic-shaped findings, including
   deliberately injected data-quality noise (duplicates, missing values, casing inconsistencies)
   so the cleaning phase has genuine work to do, not a formality.

## Tools and why each was chosen

| Tool | Used for | Why |
|---|---|---|
| Python (pandas) | Data generation, cleaning, KPI/funnel analysis | Single source of truth for every KPI definition, reused, not re-derived, by SQL and the dashboard spec. |
| SQLite + SQL | KPI, funnel, and segmentation queries | Demonstrates SQL analysis ability without requiring a database server; results cross-checked against Python to confirm the two never silently disagree. |
| Power BI (specification only) | Dashboard design | See [dashboard/README.md](../dashboard/README.md) for why this stayed a spec rather than a built report. |
| Git/GitHub | Version control, portfolio hosting | Standard practice; commit history itself is part of what a reviewer can inspect. |

## Consistency principle: one KPI, one definition

A recurring risk in analysis projects is a KPI that means something slightly different in each
tool: the Python script rounds differently than the SQL query, or the dashboard recalculates a
rate using a different denominator. This project enforces the opposite on purpose:

- `python/analysis.py` defines every KPI function once (`completion_rate`, `abandonment_rate`,
  `error_rate`, `build_funnel_table`, etc.).
- The SQL queries in `sql/` were written independently and then **verified to match the Python
  output exactly** (see the project's Phase 6 notes). A real bug was caught this way: a
  `COALESCE` in `02_funnel_analysis.sql` that made the last step of every journey show a
  misleading 100% drop-off.
- The Power BI DAX measures in `dashboard/README.md` are written to mirror the same Python
  functions, field for field, so a number in a hypothetical dashboard would match the number in
  this report.

## Honesty principle: not everything gets forced to the same maturity

Several deliverables in this project deliberately stop short of full completion where the
underlying question genuinely isn't resolved yet:

- **REQ-007** (reducing `credit_application` steps) has no fully scoped requirement, because
  which fields are truly mandatory is a compliance question this project cannot answer.
- **US-007** has no acceptance criteria, for the same reason: writing them would mean specifying
  a solution before compliance confirms it's implementable.
- **Action G** (accessibility audit for 60+ customers) is marked "investigate further" on the
  recommendations roadmap, not scheduled as a committed initiative.
- The **to-be process** ([business-analysis/to-be-process.md](../business-analysis/to-be-process.md))
  explicitly does not draw a redesigned `credit_application` flow, for the same REQ-007 reason.

A real backlog contains items at different levels of readiness; pretending every finding is
equally actionable on day one would misrepresent how this analysis actually concluded.

## Non-causal framing

None of the insights in [final-report.md](final-report.md) are described as proven causes. Every
interpretation uses hedged language ("is associated with", "may indicate", "suggests") precisely
because a single cross-sectional dataset can show correlation, not causation. A controlled
experiment (A/B test) would be needed to confirm any of them, which is why several
recommendations are explicitly framed as pilots to run, not conclusions to act on immediately.

## Limitations

- **Single synthetic snapshot, no time dimension.** There is no real "before/after" or trend
  data: every KPI is a point-in-time measurement across 5,000 simulated sessions, not a series
  observed over time.
- **No real user research behind the segment hypotheses.** Age 60+ and new-customer effects are
  measured accurately within this dataset, but *why* those groups behave this way is inferred,
  not confirmed with actual customers (this is exactly why Action G stays "investigate further"
  rather than a committed build).
- **Small-sample flags.** At least one segment finding (the "unknown" `device_type` group, ~30
  sessions) is called out in the project's working notes as real-but-small-sample and should not
  be over-weighted relative to the larger segment effects.
