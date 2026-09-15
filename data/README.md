# Data Dictionary: Banking Customer Journey Dataset

This document is the design contract for the synthetic dataset used throughout this project. It
is written **before** any data is generated (Phase 3), so that the data generation script has a
clear, deliberate schema to implement rather than improvised columns.

The dataset is entirely synthetic. No real customer, account, or transaction data is used.

## Row granularity

**One row = one step event within one journey attempt.**

If a customer starts `credit_application` and abandons after completing step 3 of 7, that
session produces exactly **3 rows**: steps 4 to 7 simply do not exist for that session. This is
intentional. The absence of later steps is what signals abandonment and is what makes the funnel
analysis in Phase 7 possible (count of customers reaching each step, and where they stop).

## Design decisions (and alternatives considered)

| Decision | Chosen approach | Alternative considered | Why chosen |
|---|---|---|---|
| Table structure | One flat, denormalized table | Two normalized tables (`sessions` + `steps`) joined by a key | A single table answers every business question in `data-requirements.md` without extra joins; keeps the project simple (KISS) while SQL can still demonstrate `GROUP BY`, window functions, and self-joins between consecutive steps |
| `session_id` vs `journey_id` | Kept as two columns, but always equal | Model multiple journey attempts per session | In this dataset, one session = one journey attempt. Modeling anything more complex isn't needed by any business question (YAGNI) |
| Abandoned rows | No placeholder rows for unreached steps | Fill all steps, mark unreached ones as `NULL`/`not_reached` | Missing rows are a cleaner, more realistic signal and simplify funnel counting (`COUNT` per step_order) |

## Columns

| Column | Type | Description | Example values |
|---|---|---|---|
| `customer_id` | string | Unique customer identifier, stable across sessions | `CUST00001` |
| `session_id` | string | Unique identifier for this app session | `SESS000001` |
| `journey_id` | string | Unique identifier for this journey attempt (1:1 with `session_id`; see decision table above) | `JRNY000001` |
| `journey_type` | categorical | Which digital journey this is | `account_opening`, `credit_application`, `bank_transfer`, `personal_data_update` |
| `customer_segment` | categorical | Customer relationship segment | `new_customer`, `existing_customer`, `premium_customer` |
| `age_group` | categorical | Age bracket | `18-25`, `26-35`, `36-45`, `46-60`, `60+` |
| `channel` | categorical | Access channel | `mobile_app`, `web_browser`, `branch_assisted_digital` |
| `device_type` | categorical | Device used | `mobile`, `desktop`, `tablet` |
| `step_name` | categorical | Name of this step (depends on `journey_type`, see below) | `login`, `personal_information`, `identity_verification`, ... |
| `step_order` | integer | Position of this step within its journey's sequence (1 = first) | `1`, `2`, `3`, ... |
| `step_duration_seconds` | float | Time spent on this step | `18.4` |
| `error_count` | integer | Number of validation/system errors on this step | `0`, `1`, `2` |
| `support_contact` | boolean | Whether the customer contacted support during this step | `True` / `False` |
| `completed` | boolean | Whether the overall journey (session) was completed | `True` / `False` |
| `abandoned` | boolean | Whether the overall journey was abandoned | `True` / `False` |
| `abandonment_reason` | categorical, nullable | Reason for abandonment; only set on the last row of an abandoned session | `too_long_or_complex`, `technical_error`, `changed_mind`, `missing_information`, `null` if completed |
| `timestamp` | datetime | When this step event occurred | `2026-03-14 10:22:31` |

`completed`, `abandoned`, and `abandonment_reason` are repeated on every row of a given session
(denormalized) so that step-level rows can be filtered/grouped without a join back to a
session-level table, consistent with the "one flat table" decision above.

## Journeys and their step sequences

Step sequences differ by journey to reflect realistic complexity. This directly encodes the
hypothesis from [as-is-process.md](../business-analysis/as-is-process.md) that more complex
journeys (more steps, more required information) are more prone to abandonment.

| `journey_type` | Steps (`step_order`: `step_name`) | Step count |
|---|---|---|
| `account_opening` | 1: `login`, 2: `service_selection`, 3: `personal_information`, 4: `document_upload`, 5: `identity_verification`, 6: `confirmation` | 6 |
| `credit_application` | 1: `login`, 2: `service_selection`, 3: `personal_information`, 4: `income_details`, 5: `loan_terms_selection`, 6: `credit_check_verification`, 7: `confirmation` | 7 (most complex) |
| `bank_transfer` | 1: `login`, 2: `service_selection`, 3: `recipient_details`, 4: `amount_entry`, 5: `otp_verification`, 6: `confirmation` | 6 |
| `personal_data_update` | 1: `login`, 2: `service_selection`, 3: `update_information`, 4: `identity_verification`, 5: `confirmation` | 5 (simplest) |

## Business logic to encode in data generation (Phase 3)

These are the hypotheses from [as-is-process.md](../business-analysis/as-is-process.md),
translated into rules the generation script will implement. They are assumptions, not proven
facts. The analysis phases will test them against the generated data.

1. **Step complexity → duration:** steps that require more input or external checks
   (`income_details`, `document_upload`, `identity_verification`, `credit_check_verification`,
   `otp_verification`) take longer on average than simple steps (`login`, `confirmation`).
2. **Step complexity → errors:** the same complex steps have a higher error rate than simple
   steps.
3. **Errors → abandonment:** a step with more errors has a higher chance of being the last step
   before abandonment.
4. **Journey complexity → abandonment:** `credit_application` (7 steps, external checks) is
   expected to show the highest abandonment rate; `bank_transfer` and `personal_data_update`
   the lowest.
5. **Segment/age → abandonment:** `new_customer` and older age groups (`60+`) are modeled with a
   somewhat higher abandonment tendency (less digital familiarity assumption), but with enough
   randomness that this is a tendency, not a rule. Real variation must remain visible in the
   data.
6. **Device → abandonment:** `mobile` sessions are modeled with a slightly higher abandonment
   rate than `desktop` on the longer, more complex steps (small-screen friction assumption).
7. **Support contact:** more likely to occur on high-error steps; sessions with a support
   contact are modeled with a higher completion rate than similarly error-prone sessions without
   one (support helps recovery), even though they take longer overall.

## Known data quality issues (deliberately injected)

To make the data-cleaning phase (Phase 4) meaningful, the raw dataset intentionally contains a
small number of realistic imperfections, comparable to what a real digital event pipeline would
produce. Each is small (well under 1% of rows) and clearly implemented in
`python/data_generation.py`:

- **Duplicate rows (about 0.3%):** simulates a client retry double-logging the same step event.
- **Missing `device_type` (about 0.6%):** simulates a device-detection failure on the client
  side.
- **Inconsistent casing in `channel` (about 0.4%):** e.g. `Mobile_App` instead of `mobile_app`,
  simulating logs from an older app version.

`python/data_cleaning.py` (Phase 4) is responsible for detecting and resolving these.

## Target volume

About 5,000 journey attempts (sessions), with abandoned sessions contributing fewer rows than
completed ones. This is expected to produce roughly **22,000-25,000 step-event rows**, within
the 10,000-30,000 interaction range requested for the project: enough to make segment and funnel
differences statistically visible without being unwieldy to explore in pandas, Excel, or Power
BI.
