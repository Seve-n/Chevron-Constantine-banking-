# As-Is Process: Digital Journey (Generic Model)

## Purpose

Before designing the dataset, it helps to map out what a typical Chevron Constantine Banking
digital journey looks like today. This is a **generic model** that applies, with minor
variations, to all four journeys in scope (`account_opening`, `credit_application`,
`bank_transfer`, `personal_data_update`). It is based on reasonable assumptions about how digital
banking journeys are typically built, not on real Chevron Constantine Banking/Belfius process
documentation.

This process map will directly shape the `step_name` and `step_order` fields in the dataset
(Phase 2), and will be revisited as **as-is** once real findings are available, producing the
[to-be-process.md](to-be-process.md) later in the project.

## Process Steps

```text
Customer
   ↓
1. Authentication (Login)
   ↓
2. Service Selection
   ↓
3. Information Input
   ↓
4. Verification
   ↓
5. Confirmation / Submission
```

### 1. Authentication (Login)

- **Actor(s):** Customer, Authentication system.
- **Description:** The customer logs in with credentials (and possibly 2FA) to access the app.
- **Decision point:** Credentials valid? → proceed / invalid → retry or lock account.
- **Potential errors:** Wrong password, expired session, 2FA failure.
- **Assumed friction:** Customers who forgot their password or don't have their 2FA device handy
  may abandon here before even starting the journey they came for.

### 2. Service Selection

- **Actor(s):** Customer.
- **Description:** The customer chooses which journey to start (open an account, apply for
  credit, make a transfer, update personal data).
- **Decision point:** Is the desired service available/eligible for this customer?
- **Potential errors:** Service temporarily unavailable, customer not eligible (e.g., existing
  product conflict).
- **Assumed friction:** Low, generally, but unclear navigation/menu labeling could cause
  hesitation or wrong selections.

### 3. Information Input

- **Actor(s):** Customer.
- **Description:** The customer fills in the data required for the journey (personal details,
  loan amount, transfer details, updated address, etc.). This is typically the **longest and
  most complex step**.
- **Decision point:** Are all required fields completed and well-formatted?
- **Potential errors:** Missing fields, invalid formats (e.g., IBAN, phone number), unclear
  instructions.
- **Assumed friction:** This is the step most likely to generate errors and consume the most
  time, and therefore the step this project expects to be most associated with abandonment.

### 4. Verification

- **Actor(s):** Customer, backend verification system (identity checks, business rules, fraud
  checks).
- **Description:** The information submitted is validated, either instantly or with a short
  wait, and the customer may be asked to confirm or correct details.
- **Decision point:** Does the submitted information pass verification? → proceed / fail →
  return to step 3.
- **Potential errors:** Verification system timeout, false rejections, unclear rejection reasons.
- **Assumed friction:** A verification failure with a vague error message is a strong candidate
  for both abandonment and a support contact.

### 5. Confirmation / Submission

- **Actor(s):** Customer, system (confirmation notification).
- **Description:** The customer reviews a summary and confirms; the system processes the request
  and shows a confirmation screen/notification.
- **Decision point:** Does the customer confirm, or step away before confirming?
- **Potential errors:** Confirmation screen fails to load, submission times out with no clear
  feedback to the customer on whether it succeeded.
- **Assumed friction:** Customers who don't receive clear, immediate confirmation may believe the
  journey failed (even if it technically succeeded) and may re-attempt or contact support
  unnecessarily.

## Cross-cutting observations (assumptions to validate with data)

- **Support contact** can plausibly happen at any step, but is most expected around steps 3 and
  4 (input and verification), where errors and uncertainty are highest.
- **Abandonment reasons** likely cluster into a few categories: too complex/long, technical
  error, changed their mind, missing required document/information. This will be reflected in
  the `abandonment_reason` field in the dataset.
- Journeys differ in complexity: `credit_application` is assumed to involve more input fields and
  stricter verification than `personal_data_update`, so it is expected (not yet confirmed) to
  show higher abandonment.

These assumptions exist to guide realistic data generation in Phase 3. They are explicitly
hypotheses, not conclusions. The actual analysis (Phases 5-8) will confirm, adjust, or
contradict them.
