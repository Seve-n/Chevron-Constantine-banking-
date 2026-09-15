# Interview Preparation

This document turns the project into interview-ready talking points: likely questions, the
answer grounded in what this project actually did (not a generic textbook answer), and the exact
file to point to if asked to show it live.

## "Walk me through this project."

30-second version: "I built a portfolio case study simulating digital journey abandonment at a
fictional bank, because I'm applying for a Business Analyst role at Belfius and wanted to show
the full BA workflow, not just a chart. I started from a business problem — the bank doesn't
know where or why customers give up mid-journey — worked through business questions, generated a
synthetic dataset with realistic patterns, analyzed it in Python and SQL, and turned five
findings into a prioritized recommendations roadmap and IT-ready requirements. I also specified
(but didn't build) a Power BI dashboard, and mapped the current process against a redesigned
to-be process."

Where to point if asked to show it: [../README.md](../README.md) → [final-report.md](final-report.md).

## "Why synthetic data instead of a real/public dataset?"

Two reasons, in order: no real banking dataset would let me simulate abandonment *reasons* and
*step-level* granularity the way I needed for a funnel analysis — public datasets rarely have
that. And using anything resembling real Belfius data would be inappropriate and against data
protection practice for an unsolicited portfolio project. Generating the data myself also let me
document explicit hypotheses upfront (`credit_application` should be harder than
`bank_transfer`) and then test whether the analysis actually confirmed them — which is closer to
how a real BA engagement starts (from stakeholder hypotheses), not further from it.

See: [methodology.md](methodology.md#why-a-synthetic-dataset).

## "What was the single most interesting finding?"

Insight 2 — the "worst" step depends entirely on whether you rank by rate or by absolute
customers lost. `credit_check_verification` has the highest drop-off *rate* (7.0%), but
`document_upload` and `identity_verification` each cost the bank more real customers because far
more sessions reach them. I'd use this to challenge a stakeholder who wants to fix "the worst
step" as if there's one universal answer — the right answer depends on the question you're
actually asking (which fix saves the most customers vs. which experience is scariest for the
people who hit it).

See: [final-report.md](final-report.md#insight-2--the-worst-step-depends-on-whether-you-measure-by-rate-or-by-volume).

## "How do you know these findings are real and not just noise or bias in how you generated the data?"

I don't claim they're proven causes — every insight in the final report is phrased as an
association ("is associated with", "may indicate"), not a causal claim, and the report has an
explicit section ("What this report does not claim") saying so. Several recommendations are
framed as A/B tests or pilots specifically because that's the next step to move from correlation
to a confirmed effect. I'd rather show I understand that distinction than overclaim what a single
synthetic snapshot can prove.

See: [final-report.md](final-report.md#what-this-report-does-not-claim).

## "Tell me about a mistake or bug you caught during this project."

Three real ones, useful because they show a QA/verification habit, not just "I ran a script once
and trusted the output":

1. **A SQL bug that would have shipped a wrong number to a stakeholder.** My funnel drop-off
   query used `COALESCE(LEAD(...), 0)`, which made the *last* step of every journey show a
   misleading 100% drop-off (there's no next step to drop into — that's not abandonment, that's
   the journey ending). I caught it by cross-checking the SQL output against the Python
   analysis, which didn't have the same bug, and removed the COALESCE so it correctly shows NULL.
2. **A data modeling inconsistency I introduced myself.** I'd injected missing `device_type`
   values per-row instead of per-session, which let a handful of sessions show two different
   devices in the same journey — not realistic. I fixed the injection logic to be per-session and
   re-ran the full pipeline; verified zero inconsistent sessions afterward.
3. **A duplicate-detection ordering bug.** Normalizing channel casing (e.g. "Mobile" → "mobile")
   during cleaning created one *new* duplicate row that hadn't been a duplicate before
   normalization. I learned to re-check for duplicates *after* normalization, not only before.

Lesson I'd state out loud: verification isn't a one-time checklist item, it's something you do
after every transformation, because a fix in one place can silently break an assumption
somewhere else.

## "How did you decide what to prioritize?"

I built an impact/effort table (roadmap in [final-report.md](final-report.md)) and explicitly
split bundled recommendations into their actual component actions first — one of my own
insights (Insight 2) mixed a one-line copy change with a full in-app camera feature, and scoring
that as one "medium effort" item would have hidden that the copy change alone is nearly free.
Three actions came out as genuine quick wins (low effort, meaningful impact) and could ship in
parallel without waiting on the larger initiatives.

## "What would you do differently, or what's the biggest limitation?"

The dataset is a single point-in-time synthetic snapshot — there's no real before/after or trend
data, so I can't show whether abandonment is improving or worsening over time, only what it looks
like right now. If I extended this project, I'd add a second synthetic period to simulate a
"post-fix" state and show the KPI actually moving — which is exactly the kind of before/after
view the dashboard specification's Recommendations Tracker page is designed to hold once real
data exists.

## "Why didn't you actually build the Power BI dashboard?"

I didn't have a reliable Power BI Desktop environment for this project's timeline, and I decided
a detailed specification — pages, audience per page, and DAX measures written to match my Python
KPI functions field-for-field — demonstrates the same design discipline a BA needs whether or not
they personally build the report. I'd rather hand over an honest, usable spec than a rushed
dashboard I couldn't fully stand behind.

See: [../dashboard/README.md](../dashboard/README.md#why-a-spec-not-a-build).

## Questions to ask the interviewer

- How does Belfius currently decide which digital-experience fix to prioritize when a "quick fix"
  and a "root-cause fix" target the same problem (my Insight 2 finding)?
- How mature is the A/B testing capability for customer-facing digital changes — is that
  something the BA function is involved in scoping?
- For a segment-level finding like the age 60+ effect I found here, who owns the decision to
  invest in accessibility work versus a proactive assisted-channel offer?
