# Final Report: Banking Customer Journey Analysis

## Executive Summary

Chevron Constantine Banking customers abandon digital journeys at very different rates depending on which journey
they're in (`credit_application` 24.8% vs. `bank_transfer` 8.3%) and who they are (age 60+ at
26.3%, more than double every other age group). Two steps, `document_upload` and
`credit_check_verification`, account for a disproportionate share of lost customers, but for
different reasons: one has the highest *volume* of customers lost, the other the highest
*rate*. Five insights are developed below; each converts into a concrete, IT-estimable
requirement in [business-analysis/requirements.md](../business-analysis/requirements.md), and
three of the seven resulting actions are low-effort "quick wins" that could ship without waiting
for the larger initiatives. See [Methodology](methodology.md) for how this analysis was produced,
end to end.

This report answers the business problem defined in
[business-analysis/project-brief.md](../business-analysis/project-brief.md): where and why
Chevron Constantine Banking customers abandon digital journeys, and what the bank should do about it. Every figure
below comes directly from [python/analysis.py](../python/analysis.py) and the queries in
[sql/](../sql/), run against the cleaned dataset (5,000 sessions, 27,788 step-event rows).

Each insight follows the same structure: what we found, the evidence behind it, a careful
(non-causal) interpretation, a concrete recommendation, and the KPI that would tell Chevron Constantine Banking
whether the recommendation worked.

---

## Insight 1: Journey complexity is the strongest driver of abandonment

### Insight
`credit_application` abandons at nearly 3x the rate of `bank_transfer`, and the other two
journeys fall in between, in order of how many steps and external checks they require.

### Evidence
Abandonment rate by journey_type: `credit_application` 24.8%, `account_opening` 16.1%,
`personal_data_update` 10.3%, `bank_transfer` 8.3%.

### Interpretation
This ordering matches journey complexity exactly (7 steps with an external credit check, down
to 6, 6, and 5 simpler steps). This *suggests* that the number of steps and the presence of an
external verification are associated with abandonment. That's plausible, but not proven by this
data alone; a controlled test would be needed to isolate complexity from other differences
between these journeys (e.g. what's financially at stake for the customer).

### Recommendation
Treat `bank_transfer`'s structure (fewest steps, no ambiguous external wait) as the internal
benchmark for "how short can a journey realistically be." For `credit_application`, evaluate
which of its 7 steps could be merged, deferred, or made optional at first submission.

### KPI to monitor
`abandonment_rate` for `credit_application`, tracked monthly against the other three journeys.

---

## Insight 2: The "worst" step depends on whether you measure by rate or by volume

### Insight
By drop-off **rate**, `credit_check_verification` is the single worst step in the dataset
(7.0%). But by **absolute customers lost**, `document_upload` (account_opening) and
`identity_verification` (personal_data_update) each cost Chevron Constantine Banking more real customers, simply
because far more sessions reach them.

### Evidence
`rank_problem_steps()` (customers actually lost at each step): `document_upload` 54,
`identity_verification` (personal_data_update) 49, `login` (bank_transfer) 44,
`income_details` 42, `credit_check_verification` 40, despite `credit_check_verification`
having the highest *rate* (7.0% vs. 5.6% for `document_upload`).

### Interpretation
Rate answers "how dangerous is this step for someone who reaches it?" Absolute volume answers
"which single fix saves the most customers?" Both are legitimate, but they point to different
priorities. The answer also depends on what a lost customer is worth at that stage: a lost
`account_opening` customer never becomes a customer at all, while a lost `credit_application`
customer may already hold other Chevron Constantine Banking products.

### Recommendation
Run two parallel workstreams rather than picking one "winner": a quick UX fix on
`document_upload` (clearer accepted file formats, in-app document capture) given its high
volume, and a targeted messaging fix on `credit_check_verification` given its high rate and
the likely anxiety around an external decision (see Insight 3).

### KPI to monitor
`customers_lost_at_step` (absolute) for both steps, tracked after each change, not just the
rate, since the rate can improve while the absolute number barely moves if volume grows.

---

## Insight 3: A high error rate does not automatically mean a high abandonment impact

### Insight
`otp_verification` and `credit_check_verification` have almost identical error rates (25.7%
vs. 24.7%), but customers abandon at `credit_check_verification` about **4x more often**
(7.0% vs. 1.8%) once they hit an error there.

### Evidence
`error_rate()` by step (analysis.py) and per-step drop-off rate (`build_funnel_table()`).

### Interpretation
The *frequency* of errors is similar, but the *nature* of the error is not. A mistyped OTP
code is trivial and fully within the customer's control to fix immediately. A credit-check
error offers no such recourse. It may be read as a looming rejection, decided by a system the
customer cannot influence. This *may indicate* that perceived control over recovering from an
error matters more to abandonment than the raw error count.

### Recommendation
On `credit_check_verification`, add a clear, reassuring intermediate status (e.g. "we're
verifying your information, no action needed") to distinguish "still processing" from "likely
rejected," and offer a way to save progress and be notified rather than forcing the customer
to wait on-screen.

### KPI to monitor
`abandonment_rate_at_step` for `credit_check_verification` specifically, and its
`support_contact_rate`, before and after the messaging change.

---

## Insight 4: New customers abandon more than existing or premium customers, consistently

### Insight
`new_customer` abandons at 16.0% overall, vs. 11.7% for `existing_customer` and 10.3% for
`premium_customer`, and the same ordering holds even on a single step in isolation.

### Evidence
`abandonment_rate(sessions, by="customer_segment")`; confirmed at the step level with
`segment_breakdown_for_step()` on `credit_check_verification`: `new_customer` 9.4% vs.
`existing_customer` 5.7%.

### Interpretation
The gap holding at both the journey level and a single step level *suggests* something about
the `new_customer` segment itself (e.g. lower familiarity with Chevron Constantine Banking's digital app, lower
trust built up yet) rather than one specific confusing step. If it were just one bad step, we
would not expect the gap to persist elsewhere too.

### Recommendation
Pilot a lightweight guided-onboarding overlay (contextual tips, a visible progress indicator)
shown only to `new_customer` segment on their first digital journey, and A/B test it against
the current experience.

### KPI to monitor
The gap in `abandonment_rate` between `new_customer` and `existing_customer` is the number to
watch. The goal is to narrow it, not just move the absolute figure.

---

## Insight 5: Age 60+ shows the largest segment effect in the dataset

### Insight
Customers aged 60+ abandon at 26.3%, roughly double every other age group (10.3%-12.7%). This
is a larger gap than any other segmentation dimension in this analysis (segment, device, or
channel).

### Evidence
SQL: `sql/03_customer_segments.sql`, abandonment rate by `age_group`.

### Interpretation
Of everything measured in this project, this is the largest single disparity, larger than the
new-vs-existing customer gap (Insight 4) or any device/channel difference. It *may indicate*
a digital literacy or accessibility barrier specific to this age group, distinct from the
"new to the bank" effect, since it appears within all customer segments, not just new
customers.

### Recommendation
Investigate accessibility (text size, button size, jargon-free language) across the highest
error-rate steps for 60+ customers specifically, and proactively surface the
`branch_assisted_digital` channel as an option for this age group rather than leaving it
undiscoverable.

### KPI to monitor
`abandonment_rate` for the `60+` age group, and adoption rate of `branch_assisted_digital`
among that group.

---

## What this report does not claim

None of these insights are proven causes. They are associations observed in one synthetic
dataset, consistent with the reasoning documented throughout this project (see
[business-analysis/business-questions.md](../business-analysis/business-questions.md)). Several
recommendations above are framed as tests (A/B, pilot) precisely because the next step to move
from "association" to "confirmed effect" is a controlled experiment, not a bigger dashboard.

## Recommendations roadmap (impact vs. effort)

Some recommendations above bundle actions of very different sizes (e.g. Insight 2 mixes a
one-line copy change with a new in-app feature). Splitting them out before prioritizing avoids
the trap of treating a whole recommendation as a single unit of effort.

| # | Action | From | Impact | Effort | Tier |
|---|---|---|---|---|---|
| A | Clarify accepted file formats & instructions on `document_upload` | Insight 2 | High (54 customers) | Low | **Quick win** |
| B | Add a reassuring intermediate status message on `credit_check_verification` | Insight 3 | High (targeted, 7.0% rate) | Low | **Quick win** |
| C | Proactively surface `branch_assisted_digital` as an option for 60+ customers | Insight 5 | Medium | Low | **Quick win** |
| D | In-app document capture/scanner for `document_upload` | Insight 2 | High | Medium-High | Strategic initiative |
| E | Guided onboarding overlay + A/B test for the `new_customer` segment | Insight 4 | Medium (closes a persistent gap) | Medium-High | Strategic initiative |
| F | Reduce/merge steps in `credit_application` (likely needs compliance review) | Insight 1 | High | High | Strategic initiative |
| G | Accessibility audit (text/button size, plain language) across steps, for 60+ | Insight 5 | High | Medium | **Investigate further** |

The sequencing logic: start A, B, and C in parallel, all low-effort with no dependencies, and
together they already touch the two highest-volume problem steps (Insight 2) and the largest
segment effect (Insight 5). Scope D, E, and F as resourced initiatives once A-C are shipped. G
is deliberately not scheduled yet: committing design/engineering effort before a short UX
research pass would risk fixing the wrong accessibility barrier.

## Next steps in this project

- **Phase 10** will turn the highest-priority items above (A, B, C first) into functional
  requirements and user stories that IT could actually estimate and build.
