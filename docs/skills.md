# Skills Matrix

A quick-reference mapping from claimed skill to concrete evidence in this repository, useful for
tailoring a CV bullet or answering "can you give me an example of X" without having to reconstruct
the project from memory.

## Business Analysis skills

| Skill | Evidence | File |
|---|---|---|
| Stakeholder analysis | Identified 6 stakeholders with distinct needs (PM, BA, CX Manager, IT, Data Analyst, Support), used later to decide dashboard page structure | [business-analysis/stakeholders.md](../business-analysis/stakeholders.md) |
| Business problem framing | Business problem stated before any data existed, with explicit in/out-of-scope boundaries | [business-analysis/project-brief.md](../business-analysis/project-brief.md) |
| Business questions → data requirements | Each business question mapped to the specific data field(s) needed to answer it | [business-analysis/business-questions.md](../business-analysis/business-questions.md), [business-analysis/data-requirements.md](../business-analysis/data-requirements.md) |
| Process mapping (As-Is) | Generic 5-step journey modeled as a hypothesis before data generation | [business-analysis/as-is-process.md](../business-analysis/as-is-process.md) |
| Process mapping (To-Be) | Same process redesigned post-analysis, every change traced to an insight and requirement, with explicit scope boundaries (REQ-007 not drawn in) | [business-analysis/to-be-process.md](../business-analysis/to-be-process.md) |
| Requirements engineering | 7 functional requirements traced 1:1 to roadmap actions, one intentionally left at discovery stage rather than force-scoped | [business-analysis/requirements.md](../business-analysis/requirements.md) |
| User stories & acceptance criteria | Given/When/Then criteria for 6 stories; 1 story left without criteria to model realistic backlog grooming | [business-analysis/user-stories.md](../business-analysis/user-stories.md) |
| Prioritization (impact/effort) | 5 insights decomposed into 7 discrete actions, scored independently rather than as bundles | [docs/final-report.md](final-report.md#recommendations-roadmap-impact-vs-effort) |
| Non-causal, hedged interpretation | Every insight distinguishes association from proven cause; recommendations framed as pilots/A-B tests where relevant | [docs/final-report.md](final-report.md#what-this-report-does-not-claim) |
| Dashboard specification | Audience-per-page design, DAX measures traced to Python KPI functions | [dashboard/README.md](../dashboard/README.md) |

## Technical skills

| Skill | Evidence | File |
|---|---|---|
| Python / pandas | Data generation (5,000 sessions, reproducible via seed), cleaning, and 8 reusable KPI/funnel functions | [python/data_generation.py](../python/data_generation.py), [python/analysis.py](../python/analysis.py) |
| Data cleaning & quality | Found and fixed 81 exact duplicates, 1 casing-induced duplicate, 167 missing values (imputed, not dropped, to preserve segment visibility) | [python/data_cleaning.py](../python/data_cleaning.py) |
| SQL | 3 independent query sets (KPIs, funnel with `LEAD()`, segmentation) cross-verified against Python output | [sql/](../sql/) |
| Data modeling | Flat step-event table collapsed to session grain consistently across Python (`build_session_table`), SQL, and the Power BI star-schema spec | [python/analysis.py](../python/analysis.py), [dashboard/README.md](../dashboard/README.md#data-model) |
| KPI design & governance | Single KPI definitions reused (not re-derived) across 3 tools; a real SQL bug was caught specifically because of this cross-check | [docs/methodology.md](methodology.md#consistency-principle-one-kpi-one-definition) |
| Debugging / root-cause analysis | 3 documented bugs found and fixed during the project, with the reasoning for each fix | [docs/interview-preparation.md](interview-preparation.md#tell-me-about-a-mistake-or-bug-you-caught-during-this-project) |
| Version control (Git/GitHub) | Full project history, `.gitignore` decisions documented (e.g. why the CSV is committed but the SQLite DB is not) | [sql/README.md](../sql/README.md) |

## Soft skills demonstrated through project decisions

| Skill | Where it shows up |
|---|---|
| Intellectual honesty over completeness | REQ-007 and US-007 left at discovery stage; Action G marked "investigate further"; notebook gap disclosed in README rather than hidden |
| Communicating trade-offs, not just answers | Insight 2 (rate vs. volume) explicitly presented as two legitimate framings, not a single "correct" ranking |
| Self-directed prioritization under ambiguity | Recommendations roadmap built without a real stakeholder to arbitrate; impact/effort criteria stated explicitly so the reasoning is auditable |
| Learning from your own mistakes | Bug retrospectives written as lessons ("verification isn't a one-time checklist item"), not just fixes |
