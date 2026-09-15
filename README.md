# Banking Customer Journey Analysis

**Status:** ✅ Complete. All 15 phases delivered, from business framing to interview
preparation.

A Business Analyst case study simulating a digital journey abandonment investigation for
**Chevron Constantine Banking**, a fictional digital bank, built as a portfolio project for a Business Analyst
alternance application. The project follows a full BA workflow, from business problem to data
analysis to actionable recommendations, using a synthetic dataset (no real banking data of any
kind).

## Business Problem

Chevron Constantine Banking does not have a clear, data-backed view of where and why customers abandon digital
journeys (account opening, credit application, bank transfer, personal data update). This
project investigates the problem end-to-end and produces concrete recommendations.

Full framing: [business-analysis/project-brief.md](business-analysis/project-brief.md)

## Start here

- **Full findings:** [docs/final-report.md](docs/final-report.md), with 5 insights, each with
  evidence, interpretation, a recommendation, and a KPI to monitor, plus the prioritized
  recommendations roadmap.
- **How this was built:** [docs/methodology.md](docs/methodology.md), covering workflow, tool
  choices, and the consistency/honesty principles enforced throughout.
- **Skills demonstrated, with evidence:** [docs/skills.md](docs/skills.md).

## Methodology

This project follows a Business Analyst workflow, not a straight-to-code approach:

```text
Business Problem → Business Questions → Data Requirements → Data Analysis
    → Business Insights → Recommendations → Functional Requirements
    → User Stories → Target (To-Be) Process → Dashboard Specification
```

Work was done in phases, each producing a reviewable, standalone deliverable. See
[docs/methodology.md](docs/methodology.md) for the full approach.

## Project Structure

```text
banking-customer-journey-analysis/
│
├── business-analysis/    # Business framing: brief, stakeholders, questions, requirements,
│                          # as-is/to-be process, user stories
├── data/                  # raw/ and processed/ synthetic datasets
├── python/                # Data generation, cleaning, and analysis scripts
├── sql/                    # SQLite KPI, funnel, and segmentation queries
├── dashboard/              # Power BI dashboard specification
└── docs/                   # Methodology, final business report, and skills summary
```

> **Note on `notebooks/`:** an exploratory notebook was planned in the original project brief as
> a pedagogical extra, but was not part of the 15 numbered phases actually executed and was not
> built. `python/analysis.py` and the `sql/` queries cover the same analysis. The empty folder
> is called out here rather than silently dropped or left as an unexplained gap.

## Current Progress

| Phase | Deliverable | Status |
|---|---|---|
| 1 | Business Analysis framing (brief, stakeholders, questions, data requirements, as-is process) | ✅ Done |
| 2 | Dataset design | ✅ Done |
| 3 | Synthetic data generation | ✅ Done |
| 4 | Data quality & cleaning | ✅ Done |
| 5 | Python analysis | ✅ Done |
| 6 | SQL analysis | ✅ Done |
| 7 | Funnel & segmentation analysis | ✅ Done |
| 8 | Business insights | ✅ Done |
| 9 | Recommendations | ✅ Done |
| 10 | Requirements & user stories | ✅ Done |
| 11 | To-be process | ✅ Done |
| 12 | Dashboard specification | ✅ Done |
| 13 | Final report | ✅ Done |
| 14 | README & portfolio polish | ✅ Done |
| 15 | Interview preparation | ✅ Done |

## Technologies

Python (pandas), SQL (SQLite), Power BI (specification only; see
[dashboard/README.md](dashboard/README.md) for why), Git/GitHub.

## Business Analyst Skills Demonstrated

- **Stakeholder analysis:** [business-analysis/stakeholders.md](business-analysis/stakeholders.md)
- **Requirements engineering:** [business-analysis/requirements.md](business-analysis/requirements.md),
  including a requirement (REQ-007) deliberately left at discovery stage rather than forced
- **Process mapping (As-Is / To-Be):** [as-is-process.md](business-analysis/as-is-process.md) /
  [to-be-process.md](business-analysis/to-be-process.md), with every to-be change traced back to
  a specific insight and requirement
- **Business questions → data requirements mapping:**
  [business-analysis/business-questions.md](business-analysis/business-questions.md)
- **Data analysis (Python, SQL):** funnel analysis, segmentation, rate-vs-volume prioritization
- **KPI design:** one set of KPI definitions reused consistently across Python, SQL, and the
  dashboard spec (see [docs/methodology.md](docs/methodology.md))
- **User stories & acceptance criteria:** [business-analysis/user-stories.md](business-analysis/user-stories.md),
  including a story (US-007) intentionally left without acceptance criteria pending discovery
- **Business recommendations & prioritization:** impact/effort roadmap in
  [docs/final-report.md](docs/final-report.md)
- **Dashboard specification:** [dashboard/README.md](dashboard/README.md)

## Disclaimer

This is a fictional, educational portfolio project. **Chevron Constantine Banking** is not a real company. All data
is synthetically generated. This project is not affiliated with, and does not use any data from,
Belfius or any real financial institution.

## License

[MIT](LICENSE)
