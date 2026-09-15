# Stakeholder Analysis

This project simulates a typical Business Analyst engagement inside a digital bank.
Understanding who cares about digital journey abandonment, and why, shapes which questions
matter and how recommendations should be framed later on.

## Product Manager

- **Role:** Owns the roadmap for the digital banking app; decides what gets built and when.
- **Interest:** Wants to know which journeys to fix first to maximize business impact
  (conversion, customer satisfaction) for the least development effort.
- **Needs:** A prioritized list of problems backed by data, not opinions, ideally ranked by
  volume of customers affected and ease of fix.
- **Influence:** High. Controls the backlog. Recommendations that don't speak the PM's language
  (impact, effort, priority) won't get scheduled.

## Business Analyst (this role)

- **Role:** Bridges the gap between business problems and technical/data work. Frames the
  problem, defines requirements, and translates data findings into actionable recommendations.
- **Interest:** Deliver a clear, defensible analysis that stakeholders can act on without
  needing to interpret raw data themselves.
- **Needs:** Access to data, alignment with stakeholders on what "success" looks like, and a
  structured way to turn insights into requirements and user stories.
- **Influence:** Medium-high. Shapes how the problem is framed and what gets prioritized, but
  doesn't own final build decisions.

## Customer Experience Manager

- **Role:** Responsible for the quality of the customer journey and overall satisfaction with
  digital channels.
- **Interest:** Wants to understand where customers get frustrated, confused, or blocked, and
  whether abandonment reflects a UX problem, a trust problem, or something else.
- **Needs:** Journey-level detail, not just aggregate numbers: which step, which error, which
  segment. Evidence to justify UX investment to leadership.
- **Influence:** High on UX/process decisions, lower on technical implementation timing.

## IT

- **Role:** Builds and maintains the digital platform; implements whatever changes are approved.
- **Interest:** Wants precise, technically translatable requirements, not vague complaints. Also
  cares about technical root causes (e.g., is a high error rate a UX issue or a system
  reliability issue?).
- **Needs:** Clear functional requirements with acceptance criteria, and enough context to
  estimate effort and flag technical constraints early.
- **Influence:** High on feasibility and timeline; low on what problem gets prioritized.

## Data Analyst

- **Role:** Owns data quality, instrumentation, and the technical analysis pipeline (in this
  project, this responsibility overlaps with the Business Analyst / project author).
- **Interest:** Wants clean, reliable, well-documented data and KPI definitions that don't get
  reinterpreted differently by each team.
- **Needs:** Agreement on KPI definitions (e.g., what exactly counts as "abandoned") before
  numbers are shared widely, to avoid conflicting reports.
- **Influence:** Medium. Shapes what can be measured and how confidently conclusions can be
  stated, but doesn't set business priorities.

## Customer Support

- **Role:** Handles customers who contact the bank when they get stuck during a digital journey.
- **Interest:** Wants fewer avoidable support contacts (lower volume, lower frustration) and, for
  the contacts that do happen, better context on what the customer was doing when they reached
  out.
- **Needs:** Visibility into which steps generate the most support contacts, so staffing and
  scripts/FAQs can be adjusted proactively.
- **Influence:** Medium. Often the first to notice a problem (via contact volume) but has
  limited power to change the product itself; escalates findings to Product/CX.

## Summary: power/interest view

| Stakeholder | Interest in this project | Influence on outcomes |
|---|---|---|
| Product Manager | High | High |
| Business Analyst | High | Medium-High |
| Customer Experience Manager | High | High |
| IT | Medium | High (on feasibility) |
| Data Analyst | High | Medium |
| Customer Support | Medium | Medium |

**Why this matters for the project:** Product Manager and CX Manager are the primary audience
for the final recommendations. They have both high interest and high influence. IT is the
audience for the functional requirements and user stories. This shapes how the final report and
requirements documents are written later in the project.
