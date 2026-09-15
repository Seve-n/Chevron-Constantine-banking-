# To-Be Process — Digital Journey (Post-Recommendations)

## Purpose

[as-is-process.md](as-is-process.md) modeled the *generic* digital journey as a hypothesis,
before any data existed. This document revisits that same 5-step process **after** the analysis
(Phases 5-9) and the resulting requirements (Phase 10) — showing exactly where the process
changes, why, and which requirement/insight justifies each change.

Two design rules were applied throughout:

- **No invented fixes.** Every change below traces back to a specific insight in
  [docs/final-report.md](../docs/final-report.md) and a specific requirement in
  [requirements.md](requirements.md). If a step has no change listed, it means the data did not
  surface a problem there — not that it was ignored.
- **Discovery-stage items stay out of the process map.** REQ-007 (reducing
  `credit_application` steps) and Action G (accessibility audit) are called out separately at
  the end, not drawn into the diagram, because neither is scoped enough yet to describe as a
  concrete process change (see the notes on each below).

## Process Steps (To-Be)

```text
Customer
   ↓
1. Authentication (Login)                              [unchanged]
   ↓
2. Service Selection  ──▶  [NEW] Proactive assisted-channel offer for 60+ customers (US-003)
   ↓
3. Information Input  ──▶  [CHANGED] Upfront file format/size guidance (US-001)
                       ──▶  [NEW] In-app camera capture with quality feedback (US-004)
                       ──▶  [NEW] Progress indicator + contextual tips for new customers (US-005)
   ↓
4. Verification       ──▶  [CHANGED] Reassuring status messaging during credit checks (US-002)
                       ──▶  [NEW] Leave-and-be-notified option during credit checks (US-006)
   ↓
5. Confirmation / Submission                            [unchanged]
```

### 1. Authentication (Login) — unchanged

No insight in this project points to the login step as a source of abandonment or error. The
as-is assumption ("customers who forgot their password may abandon here") was never
contradicted, but it also never surfaced as a measurable problem in the data. **To-be decision:**
leave as-is; revisit only if future data (outside this project's scope) shows otherwise.

### 2. Service Selection — new proactive channel offer

**Change:** When a logged-in customer aged 60+ starts any journey, the app now surfaces a
visible, dismissible suggestion to use branch-assisted digital support, instead of leaving that
channel undiscoverable.

**Why here, and why now (at selection, not later):** Insight 5 found the 60+ age group abandons
at 26.3% — roughly double every other segment, and the largest single gap found in the whole
analysis. Offering the alternative channel *before* the customer invests time in a journey they
may abandon avoids wasted effort on both sides.

**Traceability:** Insight 5 → REQ-003 → US-003.

**Decision point added:** Does the customer dismiss the suggestion or accept it? If accepted,
the customer is routed to branch-assisted support instead of continuing the self-service flow
(routing itself is out of scope for this project — see [dashboard/README.md](../dashboard/README.md)
for how adoption of this channel would be measured going forward).

### 3. Information Input — three changes, all targeting the same step

This step absorbs the most changes because it is where the two highest-volume problem findings
(Insight 2) and the persistent new-customer gap (Insight 4) both live.

**Change A — upfront format guidance (quick win):** Before the customer selects a file for
`document_upload`, the accepted formats and maximum size are shown, and a rejected file now
produces a specific error ("File too large — max 5MB") instead of a generic one.

**Why:** `document_upload` costs Chevron Constantine Banking more customers in absolute terms (54) than any other
single step, and has the highest error rate in the dataset (32.3%). This is the cheapest possible
intervention on the biggest volume problem.

**Traceability:** Insight 2 → REQ-001 → US-001.

**Change B — in-app document capture (strategic initiative):** Ships *after* Change A, so
customers already know what's expected before the capture tool guides them to it. Real-time
framing/quality feedback catches a blurry or cropped photo before submission instead of after.

**Why:** Change A fixes the *communication* of the problem; this fixes the underlying *cause* of
many of the errors (customers photographing/scanning documents with no guidance).

**Traceability:** Insight 2 → REQ-005 → US-004.

**Change C — progress indicator + contextual tips for new customers:** A `new_customer` on their
first digital journey now sees a step-count progress indicator throughout, plus an extra tip at
steps with a historically higher error rate (`document_upload`, `identity_verification`).

**Why:** Insight 4 showed the new-vs-existing customer abandonment gap (16.0% vs. 11.7%) holds
even *within* a single step in isolation — meaning it isn't one confusing step, but a broader
unfamiliarity that guidance embedded across the whole Information Input step can address.

**Traceability:** Insight 4 → REQ-006 → US-005.

**Decision point added:** Is this session's customer flagged `new_customer` and on their first
journey? → show progress/tips overlay. Is the current step `document_upload`? → show format
guidance and offer camera capture.

### 4. Verification — reframing a forced wait into an informed, resumable one

**Change A — reassuring status message (quick win):** While `credit_check_verification` is
pending, the customer now sees "we're verifying your information — no action needed" instead of
an ambiguous or blank loading state. If verification fails, the message explicitly distinguishes
a technical/retryable error from a decision outcome.

**Why:** Insight 3 found `credit_check_verification` and `otp_verification` have almost
identical error rates (~25%), yet customers abandon 4x more often after a
`credit_check_verification` error (7.0% vs. 1.8%). The data suggests the *ambiguity and perceived
lack of control* during this specific wait — not the error frequency itself — drives the extra
abandonment.

**Traceability:** Insight 3 → REQ-002 → US-002.

**Change B — leave-and-be-notified option (strategic initiative):** From the same screen, the
customer can choose "notify me instead," leave the app, and return later via a notification that
takes them straight back to their application's current status.

**Why:** Converts a forced on-screen wait into an asynchronous one, directly targeting the same
7.0% drop-off without requiring the verification itself to get any faster.

**Traceability:** Insight 3 → REQ-004 → US-006 (dependency: requires a notification system —
flagged as Medium/Low priority in requirements.md until that integration is scoped).

**Decision point added:** Does verification return instantly? → proceed to Confirmation. Is it
still pending after N seconds? → offer "wait" or "notify me instead."

### 5. Confirmation / Submission — unchanged

No insight in this project isolates a problem specific to the confirmation step itself. The
as-is assumption about unclear confirmation feedback was a reasonable hypothesis going in, but
the data did not produce a finding that would justify a specific change here. **To-be decision:**
leave as-is; this step remains a candidate for future investigation, not a current
recommendation.

## Requirements traceability (summary)

| Step | Change | Insight | Requirement | User Story | Roadmap tier |
|---|---|---|---|---|---|
| 2. Service Selection | Proactive 60+ channel offer | 5 | REQ-003 | US-003 | Quick win (C) |
| 3. Information Input | Upfront format/size guidance | 2 | REQ-001 | US-001 | Quick win (A) |
| 3. Information Input | In-app document capture | 2 | REQ-005 | US-004 | Strategic (D) |
| 3. Information Input | Progress indicator + tips | 4 | REQ-006 | US-005 | Strategic (E) |
| 4. Verification | Reassuring status message | 3 | REQ-002 | US-002 | Quick win (B) |
| 4. Verification | Leave-and-be-notified | 3 | REQ-004 | US-006 | Strategic (deferred) |

## Changes intentionally left out of this process map

- **`credit_application` step reduction/merging (REQ-007, Action F).** Insight 1 is the
  strongest journey-level finding in the project (24.8% abandonment, ~3x `bank_transfer`), but
  *which* steps could be merged or deferred is a compliance question, not a process-design one
  (see the note in [requirements.md](requirements.md)). Drawing a specific "merged" flow here,
  before that review happens, would specify a solution the business hasn't actually validated as
  implementable — so this process map deliberately stops at "Insight 1 exists and is unresolved,"
  the same honesty already modeled in Phase 10's user stories (US-007).
- **Accessibility audit for 60+ customers (Action G).** Insight 5 is addressed above at the
  *channel-offering* level (Change: Service Selection), but the roadmap's Action G (text size,
  button size, plain language across steps) is explicitly an "investigate further" item, not a
  committed change — a short UX research pass needs to happen first so effort isn't spent fixing
  the wrong accessibility barrier. Nothing is drawn into the process map for it yet.

## What this to-be process does not claim

Like the final report, this document does not assert that these changes *will* fix abandonment —
it proposes them because the data is *consistent with* each targeted problem, and each
recommendation in [docs/final-report.md](../docs/final-report.md) is explicitly framed as a pilot
or A/B test where that distinction matters (Change C, in particular, is designed to be A/B
tested against the current experience before being rolled out to all new customers).
