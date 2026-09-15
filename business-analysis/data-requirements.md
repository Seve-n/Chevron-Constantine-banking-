# Data Requirements

This document maps each business question from [business-questions.md](business-questions.md) to
the data needed to answer it, the KPI(s) involved, and the type of analysis required. It exists
to make sure the synthetic dataset (designed in Phase 2) is actually built to answer real
questions — not the other way around.

| # | Business Question | Data Needed | KPI | Analysis |
|---|---|---|---|---|
| 1 | Overall completion rate | `journey_id`, `completed` flag per journey | Completion rate | Aggregate count of completed vs. total journeys |
| 2 | Overall abandonment rate over time | `abandoned` flag, `timestamp` | Abandonment rate (overall, by period) | Aggregate + trend over time |
| 3 | Step where most customers abandon | `step_name`, `step_order`, `abandoned`, `journey_id` | Drop-off rate per step | Funnel analysis (step-by-step drop-off) |
| 4 | Journey with highest abandonment | `journey_type`, `completed`/`abandoned` | Abandonment rate by journey | Group-by comparison across journey types |
| 5 | Is abandonment concentrated or spread out | `step_name`, `step_order`, `abandoned` | Drop-off rate per step | Funnel shape analysis (distribution across steps) |
| 6 | Error-heavy steps vs. abandonment | `step_name`, `error_count` | Error rate per step, abandonment rate per step | Correlation between error rate and drop-off rate, per step |
| 7 | Step duration vs. abandonment | `step_duration_seconds`, `abandoned` | Average step duration (completed vs. abandoned) | Compare duration distributions for completed vs. abandoned steps |
| 8 | Support contact vs. completion | `support_contact`, `completed` | Support contact rate, completion rate after contact | Compare completion rate for sessions with vs. without support contact |
| 9 | Customer segment vs. abandonment | `customer_segment`, `abandoned` | Abandonment rate by segment | Group-by comparison across segments |
| 10 | Age group vs. abandonment | `age_group`, `abandoned` | Abandonment rate by age group | Group-by comparison across age groups |
| 11 | Device vs. completion | `device_type`, `completed` | Completion/abandonment rate by device | Group-by comparison across device types |
| 12 | Channel vs. completion | `channel`, `completed` | Completion/abandonment rate by channel | Group-by comparison across channels |
| 13 | Which journey/step to prioritize | Combination of #3, #4, #6, #9–#12 | Weighted view: abandonment rate × customer volume | Ranking of steps/journeys by (volume affected × severity) |
| 14 | What changes could reduce abandonment | Same data as #6, #7, #8 (error, duration, support signals) | Error rate, avg. duration, support contact rate | Root-cause reasoning combining funnel + segment + error findings |
| 15 | KPIs to monitor going forward | All of the above | Full KPI set defined in [project-brief.md](project-brief.md) | Defines the ongoing dashboard/monitoring scope |

## Core fields this implies for the dataset

Reading across the table, every business question can be answered as long as the dataset
captures, at minimum, one row per **step event** within a **session** within a **journey**, with:

- **Identifiers:** `customer_id`, `session_id`, `journey_id`
- **Journey context:** `journey_type`, `step_name`, `step_order`
- **Customer context:** `customer_segment`, `age_group`, `channel`, `device_type`
- **Step outcome:** `step_duration_seconds`, `error_count`, `support_contact`
- **Journey outcome:** `completed`, `abandoned`, `abandonment_reason`
- **Time:** `timestamp`

This list directly informs the dataset design in Phase 2 — nothing here is arbitrary; every
column exists because a business question in this document needs it.
