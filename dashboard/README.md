# Power BI Dashboard — Specification

## Status

This is a **specification only** — no `.pbix` file exists in this repository. That is a
deliberate scope decision (see [Why a spec, not a build](#why-a-spec-not-a-build) below), not an
oversight: a Business Analyst is frequently asked to *specify* what a dashboard must show and why
— pages, measures, audience, and the KPI definitions behind them — and to hand that spec to a BI
developer, rather than to build the report personally. This document is written as that
handoff artifact would be.

## Audience and purpose

Three stakeholders were identified in [business-analysis/stakeholders.md](../business-analysis/stakeholders.md)
who would use this dashboard differently:

| Stakeholder | What they need from this dashboard |
|---|---|
| Product Manager | Which journey/step to prioritize next — rate vs. absolute volume (Insight 2), sequenced against the roadmap in [docs/final-report.md](../docs/final-report.md). |
| Customer Experience Manager | Segment-level gaps (new vs. existing customer, age 60+) to brief CX initiatives. |
| IT / Engineering lead | Confirmation that a shipped fix (e.g. Action A on `document_upload`) actually moved the KPI it targeted, not just a general health check. |

A single dashboard cannot equally serve "what should we build next" and "did what we built
work" — so the spec below splits those into separate pages rather than cramming both into one
crowded view.

## Data source

Single source of truth: `data/processed/banking_customer_journeys_clean.csv` (the same file
`python/analysis.py` and the `sql/` queries read). In a real deployment this would be a scheduled
extract from the production event store; for this portfolio project, Power BI would connect
directly to the CSV (or to `sql/novabank.db` via an ODBC/SQLite connector) and refresh manually,
since there is no live pipeline behind it.

**Grain:** the source file is one row per step-event (a customer's visit to one step within one
session) — the same grain `python/analysis.py`'s `df` operates on before it gets collapsed by
`build_session_table()`. The data model below reconstructs that same session-level collapse
inside Power BI, so a KPI means the same thing in the dashboard as it does in the Python and SQL
analysis — this project treats "three tools, one definition" as a requirement, not a nice-to-have.

## Data model

Recommended approach: import the flat CSV into Power Query and split it into a lightweight star
schema, rather than building every visual directly off one wide table. This keeps DAX measures
simpler and matches how `build_session_table()` already separates "one row per session" facts
from "one row per step-event" facts in the Python code.

```text
        Dim_Journey                    Dim_Customer
      (journey_type)                (customer_segment,
            │                         age_group)
            │                              │
            └──────────┐        ┌──────────┘
                        ▼        ▼
                  Fact_StepEvents
        (session_id, step_name, step_order, timestamp,
         step_duration_seconds, error_count, support_contact,
         completed, abandoned, abandonment_reason,
         device_type, channel)
                        │
                        ▼
                Fact_Sessions (calculated table)
        one row per session_id — mirrors build_session_table()
```

`Fact_Sessions` would be built with a Power Query grouped transformation (or a calculated DAX
table using `SUMMARIZE`) that reproduces exactly what `build_session_table()` does in Python:
one row per `session_id`, `journey_duration_seconds` = sum of `step_duration_seconds`,
`total_errors` = sum of `error_count`, `contacted_support` = max of `support_contact`. Keeping
this transformation documented here (rather than only inside a `.pbix`) means a BI developer
without Python experience can still reproduce the same session-level numbers a stakeholder might
cross-check against `docs/final-report.md`.

## Core DAX measures

Each measure below is written to match one function in `python/analysis.py` exactly, so a number
never silently drifts between the Python analysis, the SQL queries, and the dashboard.

```dax
Completion Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Fact_Sessions), Fact_Sessions[completed] = TRUE),
    COUNTROWS(Fact_Sessions)
)
-- mirrors completion_rate() in python/analysis.py

Abandonment Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Fact_Sessions), Fact_Sessions[abandoned] = TRUE),
    COUNTROWS(Fact_Sessions)
)
-- mirrors abandonment_rate()

Avg Journey Duration (sec) =
AVERAGE(Fact_Sessions[journey_duration_seconds])
-- mirrors average_journey_duration()

Support Contact Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Fact_Sessions), Fact_Sessions[contacted_support] = TRUE),
    COUNTROWS(Fact_Sessions)
)
-- mirrors support_contact_rate()

Error Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Fact_StepEvents), Fact_StepEvents[error_count] > 0),
    COUNTROWS(Fact_StepEvents)
)
-- mirrors error_rate(), grain: step visits, not sessions

Customers Lost at Step =
VAR SessionsAtStep = COUNTROWS(Fact_StepEvents)
VAR SessionsAtNextStep =
    CALCULATE(
        COUNTROWS(Fact_StepEvents),
        FILTER(
            ALL(Fact_StepEvents[step_order]),
            Fact_StepEvents[step_order] = MAX(Fact_StepEvents[step_order]) + 1
        )
    )
RETURN SessionsAtStep - SessionsAtNextStep
-- mirrors the LEAD()-based logic in build_funnel_table() / 02_funnel_analysis.sql;
-- the last step of a journey should show BLANK(), not a misleading 100%, matching the
-- same COALESCE bug that was found and fixed in Phase 6 (see project memory / git history)
```

## Report pages

### Page 1 — Executive Overview

- KPI cards: Completion Rate, Abandonment Rate, Avg Journey Duration, Support Contact Rate
  (overall, with a journey_type slicer).
- Bar chart: Abandonment Rate by `journey_type`, sorted descending — surfaces Insight 1
  (`credit_application` at ~3x `bank_transfer`) at a glance.
- Trend placeholder: this project's dataset is a single synthetic snapshot (no real time series),
  so the spec calls for a line chart *once real data with a date range exists* — noted here so a
  BI developer doesn't wonder why it's missing from the current build.

### Page 2 — Funnel & Drop-off

- Funnel visual per `journey_type`: `sessions_reaching_step` at each `step_order`.
- Table: `Customers Lost at Step` (absolute) side-by-side with drop-off rate %, sortable by
  either — this directly operationalizes Insight 2 (rate vs. volume give different priorities)
  as an interactive toggle instead of a static report choice.
- Matrix: error rate by step — flags `document_upload` (32.3%) and `otp_verification`/
  `credit_check_verification` (~25%) without requiring the reader to already know the numbers.

### Page 3 — Segment Deep-Dive

- Abandonment rate by `customer_segment`, `age_group`, `device_type`, `channel` — small multiples
  or a matrix, filterable by `journey_type` and `step_name` to reproduce
  `segment_breakdown_for_step()` interactively (e.g. drill into `credit_check_verification` x
  `customer_segment` as done in Phase 7).
- Callout visuals for the two largest segment effects found in this project: age 60+ (26.3% vs.
  10-13%) and new vs. existing customer (16.0% vs. 11.7%) — pinned rather than left to be found,
  since Insight 5 was flagged as the single strongest effect in the whole analysis.

### Page 4 — Recommendations Tracker

- A table mirroring the roadmap in `docs/final-report.md` (Actions A-G): action, insight,
  impact/effort tier, status (Not started / In progress / Shipped / Needs discovery).
- This page has no data behind it yet in the synthetic dataset — it exists as a **spec for how
  Chevron Constantine Banking would track roadmap execution** once actions A-C actually ship, at which point the KPI
  cards from Page 1/2 would be filtered to a before/after date range per action.

## Refresh and access

- **Refresh cadence (spec):** daily incremental refresh in production; manual refresh for this
  portfolio project since the dataset is static and synthetic.
- **Row-level security (spec):** not applicable to this synthetic, non-customer-identifying
  dataset, but a production version would need RLS by business unit (e.g. Credit team sees
  `credit_application` detail only) — noted here because a reviewer with BI experience would
  otherwise expect to see it addressed.

## Why a spec, not a build

Three reasons this stays a specification rather than a `.pbix` file:

1. **Tool availability.** This project was built without a licensed Power BI Desktop environment
   readily available for the portfolio timeline.
2. **What the spec demonstrates.** Writing measure definitions that trace 1:1 back to
   `python/analysis.py` and `sql/` demonstrates the same "one KPI, one definition, everywhere"
   discipline a BA needs whether or not they personally build the report — arguably more clearly
   than a screenshot of a finished dashboard would, since the reasoning behind each visual is
   visible here rather than implicit.
3. **Honesty over completeness.** Claiming a dashboard was "built" without a way for a reviewer
   to open and interact with it would misrepresent the work, the same principle already applied
   to REQ-007 and Action G elsewhere in this project (documented as not-yet-scoped rather than
   forced into a fake level of completeness).
