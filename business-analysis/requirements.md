# Functional Requirements

These requirements are derived directly from the recommendations roadmap in
[docs/final-report.md](../docs/final-report.md) (actions A–G). Each requirement traces back to
a specific insight and a specific KPI — nothing here is a generic "best practice" example
disconnected from this project's actual findings.

`REQ-007` is intentionally left without a fully scoped requirement: it needs a compliance
review before IT could estimate it (see the note below the table).

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| REQ-001 | The system shall display the accepted file formats and maximum file size for `document_upload` before the customer selects a file, and show a specific (not generic) error if the file doesn't meet those requirements. | High | Targets the single step with the most customers lost in absolute terms (54) and the highest error rate (32.3%) — Insight 2 / Action A. |
| REQ-002 | The system shall display a clear, reassuring status message during `credit_check_verification` while the result is pending, distinguishing "still processing" from a final decision. | High | Targets the step with the highest drop-off rate in the dataset (7.0%) — Insight 3 / Action B. |
| REQ-003 | The system shall proactively offer the `branch_assisted_digital` channel to customers in the `60+` age group at the start of a digital journey. | Medium | Targets the strongest single segment effect found in the analysis (26.3% abandonment vs. 10-13% for other age groups) — Insight 5 / Action C. |
| REQ-004 | The system shall allow a customer to leave `credit_check_verification` while it is pending and be notified (in-app or push) once a result is available, instead of requiring them to wait on-screen. | Medium | Converts a forced wait into an asynchronous one; may recover some of the 40 customers currently lost at this step — Insight 3. |
| REQ-005 | The system shall provide an in-app camera-based document capture tool for `document_upload`, with real-time quality/format feedback before submission. | Medium | Addresses the root cause of the highest error rate (32.3%) rather than only its symptoms — Insight 2 / Action D. |
| REQ-006 | The system shall display a visible progress indicator and step-specific contextual guidance to customers in the `new_customer` segment during their first digital journey. | Medium | Targets a gap that persists across the whole journey and even within a single step (16.0% vs. 11.7% abandonment) — Insight 4 / Action E. |
| REQ-007 | *(Needs discovery)* The system should reduce the number of mandatory steps in `credit_application`, or defer some information collection to after initial submission. | Low (until scoped) | Targets the highest-abandonment journey overall (24.8%) — Insight 1 / Action F. |

## Note on REQ-007

Unlike the other requirements, REQ-007 cannot yet be estimated by IT: which fields in
`credit_application` are truly mandatory (regulatory requirement) versus merely
convenient to collect upfront is a compliance question, not a UX one. Writing a specific
requirement before that review would risk specifying the wrong solution. This is intentional —
not every finding is ready to become a requirement on day one, and a requirements document
should say so rather than force a premature specification.
