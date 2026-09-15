# User Stories

Each story maps to a requirement in [requirements.md](requirements.md). Not every requirement
gets a fully detailed story yet: US-007 is written at "needs discovery" maturity, on purpose —
a real backlog contains stories at different levels of readiness, and pretending otherwise would
misrepresent how this analysis actually concluded.

---

### US-001 — Clear document format guidance

En tant que **client en cours d'ouverture de compte**,
je veux **connaître les formats et la taille de fichier acceptés avant de téléverser un
document**,
afin de **ne pas perdre de temps à soumettre un fichier qui sera rejeté**.

**Priority:** High
**Dependencies:** None
**Maps to:** REQ-001

**Acceptance criteria:**
- Given I am on the `document_upload` step, When the page loads, Then I see the accepted file
  formats (e.g. PDF, JPG, PNG) and the maximum file size displayed before selecting a file.
- Given I select a file that doesn't meet the format or size requirements, When I attempt to
  upload it, Then I see a specific error message naming the exact problem (e.g. "File too
  large — max 5MB") rather than a generic error.

---

### US-002 — Clear status during credit verification

En tant que **client en cours de demande de crédit**,
je veux **voir un message clair pendant la vérification de mon dossier**,
afin de **savoir que je n'ai rien à faire et que je n'ai pas été refusé**.

**Priority:** High
**Dependencies:** None
**Maps to:** REQ-002

**Acceptance criteria:**
- Given I have submitted my information for `credit_check_verification`, When the verification
  is still processing, Then I see a message such as "We're verifying your information — no
  action needed" instead of a blank or ambiguous loading state.
- Given the verification fails, When the result is returned, Then the message distinguishes a
  technical error (retry available) from a decision outcome (see next steps / contact support).

---

### US-003 — Proactive assisted channel for older customers

En tant que **client de 60 ans ou plus**,
je veux **qu'on me propose une assistance en agence pour ma démarche digitale**,
afin de **pouvoir terminer ma démarche avec de l'aide si l'application en libre-service me
semble difficile**.

**Priority:** Medium
**Dependencies:** Requires `age_group` to be known for the logged-in customer.
**Maps to:** REQ-003

**Acceptance criteria:**
- Given I am logged in and my profile's age group is `60+`, When I start a digital journey,
  Then I see a visible, dismissible suggestion to use branch-assisted digital support.
- Given I dismiss the suggestion, When I continue the journey, Then I am not shown the same
  suggestion again during that session.

---

### US-004 — In-app document capture

En tant que **client en cours d'ouverture de compte**,
je veux **photographier mon document directement dans l'application**,
afin de **ne pas avoir besoin d'un scanner ou d'une application séparée**.

**Priority:** Medium
**Dependencies:** Requires camera permission handling. Should ship after US-001, so accepted
formats are already communicated before the capture tool is introduced.
**Maps to:** REQ-005

**Acceptance criteria:**
- Given I am on the `document_upload` step, When I choose "use camera," Then the app opens a
  guided capture view with real-time framing and quality feedback.
- Given the captured image is blurry or a corner is cut off, When I confirm the capture, Then
  I am prompted to retake it before proceeding.

---

### US-005 — Guided first journey for new customers

En tant que **nouveau client effectuant ma première démarche digitale**,
je veux **voir ma progression et des conseils adaptés à chaque étape**,
afin de **savoir à quoi m'attendre et ne pas me sentir perdu en cours de route**.

**Priority:** Medium
**Dependencies:** Requires a reliable "first digital journey" flag on the customer profile.
Should be built as an A/B-testable component, per the recommendation in
[docs/final-report.md](../docs/final-report.md).
**Maps to:** REQ-006

**Acceptance criteria:**
- Given I am a `new_customer` starting my first digital journey, When I reach any step, Then I
  see a progress indicator showing my current step out of the total.
- Given I am a `new_customer`, When I reach a step with a historically higher error rate (e.g.
  `document_upload`, `identity_verification`), Then I see an additional contextual tip specific
  to that step.

---

### US-006 — Save and resume credit verification

En tant que **client en cours de demande de crédit**,
je veux **pouvoir quitter la vérification en cours et être notifié une fois le résultat prêt**,
afin de **ne pas devoir attendre à l'écran pendant une durée incertaine**.

**Priority:** Low–Medium
**Dependencies:** Requires a notification system (push or email) integration.
**Maps to:** REQ-004

**Acceptance criteria:**
- Given I am on `credit_check_verification` and the result is not immediate, When I choose
  "notify me instead," Then I can leave the app and receive a notification once the result is
  ready.
- Given I return via that notification, When I reopen the app, Then I am taken directly to my
  application's current status.

---

### US-007 — Reduce steps in the credit application (needs discovery)

En tant que **Product Manager**,
je veux **savoir quelles étapes de `credit_application` peuvent être fusionnées ou reportées**,
afin de **réduire l'abandon sur le parcours le plus problématique du dataset**.

**Priority:** Needs discovery — not yet ready for development.
**Dependencies:** Compliance/legal review to confirm which fields are truly mandatory upfront;
UX research on candidate steps to merge or defer.
**Maps to:** REQ-007

**Acceptance criteria:** *Not yet defined.* This story is at the discovery stage: writing
acceptance criteria before compliance confirms which requirements are flexible would risk
specifying a solution that isn't actually implementable.
