# Project Brief — Banking Customer Journey Analysis

## Context

Chevron Constantine Banking is a fictional digital bank. Like most digital-first banks, it lets customers complete
key operations entirely through its mobile and web app: opening an account, applying for credit,
transferring money, or updating personal information.

Product and Customer Experience teams have noticed, anecdotally, that a meaningful share of
customers **start** these digital journeys but never **finish** them. So far this has not been
studied systematically — nobody can say with confidence which journeys are most affected, at
which step customers give up, or why.

## Business Problem

Chevron Constantine Banking does not have a clear, data-backed view of **where and why customers abandon digital
journeys**. Without this view, the bank cannot prioritize product fixes, cannot brief IT on what
to build first, and cannot measure whether future changes actually help.

## Objective

Produce a data-driven diagnosis of digital journey abandonment at Chevron Constantine Banking, and turn it into
concrete, prioritized recommendations that Product, CX, and IT can act on.

Concretely, this project aims to answer:

- Where in each journey do customers abandon?
- Which journeys are the most problematic?
- Which steps generate the most errors?
- Does time spent on a step influence abandonment?
- Are some customer segments more affected than others?
- What should Chevron Constantine Banking change first?

## Scope

**In scope:**

- Four digital journeys: `account_opening`, `credit_application`, `bank_transfer`,
  `personal_data_update`.
- Step-by-step funnel analysis (completion, drop-off, duration, errors).
- Segment-level analysis (customer segment, age group, device, channel).
- KPI design and calculation (Python + SQL).
- Business recommendations and functional requirements derived from the analysis.
- A dashboard specification (Power BI) built on the same data and KPIs.

**Out of scope:**

- Any real Chevron Constantine Banking/Belfius data — the dataset is entirely synthetic.
- Implementation of the recommended product changes (this project stops at the
  recommendation/requirement stage, not the build).
- Statistical causal inference (A/B testing, experiments). Findings are described as
  associations ("associated with", "may indicate"), not proven causes.
- Financial risk, credit scoring, or fraud analysis — the focus is the digital *experience*,
  not the underlying financial decision.

## Stakeholders

See [stakeholders.md](stakeholders.md) for the full breakdown (Product Manager, Business
Analyst, Customer Experience Manager, IT, Data Analyst, Customer Support).

## Business Questions

See [business-questions.md](business-questions.md) for the full list.

## Assumptions

Because this is a portfolio project and not a live engagement, some inputs are assumed rather
than confirmed with real stakeholders:

- Each customer interaction is captured as an event with a timestamp, a step name, a duration,
  and an error count — this is a realistic minimum for any modern digital banking platform.
- A journey is considered **abandoned** if it was started but not completed within the observed
  session (no explicit "cancel" action is required — silence counts as abandonment, which is
  itself a finding worth flagging to Product).
- The four journeys chosen are representative of common digital banking operations, not an
  exhaustive list of everything Chevron Constantine Banking offers.
- "Support contact" is treated as a signal of friction, not necessarily of a good or bad outcome.

## KPIs (initial list — refined once data is available)

- Completion rate (overall and per journey)
- Abandonment rate (overall, per journey, per step)
- Average journey duration
- Average step duration
- Error rate (per step, per journey)
- Support contact rate
- Abandonment rate by device, channel, customer segment, age group

## Deliverables

- Synthetic dataset (raw + processed)
- Python data generation, cleaning, and analysis scripts
- Exploratory analysis notebook
- SQL KPI, funnel, and segmentation queries
- Business analysis documentation (this brief, stakeholders, requirements, user stories,
  as-is/to-be process)
- Final business report with insights and recommendations
- Power BI dashboard specification
- Interview preparation notes
