"""
Synthetic data generator for the Banking Customer Journey Analysis project.

Generates a fully synthetic dataset of Chevron Constantine Banking digital journey attempts, following the
schema and business-logic hypotheses documented in `data/README.md`. No real customer,
account, or transaction data is used anywhere in this script.

Reproducibility: a fixed SEED drives a single numpy random Generator, so re-running this
script always produces an identical dataset.
"""

import os

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 42
N_SESSIONS = 5_000
# Not every session is a different customer: some customers attempt more than one
# journey. A pool smaller than N_SESSIONS naturally creates repeat customers.
N_CUSTOMERS = int(N_SESSIONS * 0.82)

OUTPUT_PATH = os.path.join("data", "raw", "banking_customer_journeys.csv")

# Journey definitions: ordered list of steps per journey type (see data/README.md).
JOURNEYS = {
    "account_opening": [
        "login", "service_selection", "personal_information",
        "document_upload", "identity_verification", "confirmation",
    ],
    "credit_application": [
        "login", "service_selection", "personal_information", "income_details",
        "loan_terms_selection", "credit_check_verification", "confirmation",
    ],
    "bank_transfer": [
        "login", "service_selection", "recipient_details",
        "amount_entry", "otp_verification", "confirmation",
    ],
    "personal_data_update": [
        "login", "service_selection", "update_information",
        "identity_verification", "confirmation",
    ],
}

# How often each journey is attempted (reflects that transfers are routine,
# credit applications are rarer but not negligible).
JOURNEY_WEIGHTS = {
    "bank_transfer": 0.42,
    "personal_data_update": 0.23,
    "account_opening": 0.20,
    "credit_application": 0.15,
}

# Step duration in seconds: (mean, std) of a normal distribution, floored at 3s.
STEP_DURATION_PARAMS = {
    "login": (8, 3),
    "service_selection": (10, 4),
    "personal_information": (45, 15),
    "update_information": (35, 12),
    "recipient_details": (30, 10),
    "amount_entry": (20, 8),
    "loan_terms_selection": (40, 15),
    "document_upload": (70, 25),
    "income_details": (55, 20),
    "identity_verification": (50, 18),
    "credit_check_verification": (45, 25),
    "otp_verification": (25, 10),
    "confirmation": (8, 3),
}

# Average number of errors per step visit (Poisson lambda).
STEP_ERROR_LAMBDA = {
    "login": 0.05,
    "service_selection": 0.03,
    "personal_information": 0.15,
    "update_information": 0.10,
    "recipient_details": 0.08,
    "amount_entry": 0.06,
    "loan_terms_selection": 0.12,
    "document_upload": 0.35,
    "income_details": 0.30,
    "identity_verification": 0.30,
    "credit_check_verification": 0.28,
    "otp_verification": 0.30,
    "confirmation": 0.02,
}

# How much each *additional error* on a step raises the abandonment probability.
# This is the key "recoverability" lever: otp_verification has a high error rate
# (STEP_ERROR_LAMBDA) but a LOW penalty here, because a mistyped code is trivial
# to fix. credit_check_verification has a similar error rate but a much HIGHER
# penalty, because the customer has no control over an external credit decision.
STEP_ABANDON_PER_ERROR = {
    "login": 0.03,
    "service_selection": 0.02,
    "personal_information": 0.05,
    "update_information": 0.04,
    "recipient_details": 0.04,
    "amount_entry": 0.03,
    "loan_terms_selection": 0.06,
    "document_upload": 0.09,
    "income_details": 0.08,
    "identity_verification": 0.08,
    "credit_check_verification": 0.13,
    "otp_verification": 0.025,
    "confirmation": 0.02,
}

# Steps considered complex enough that device friction (typing/uploading on a
# small screen) plausibly matters.
COMPLEX_STEPS = {
    "document_upload", "income_details", "identity_verification",
    "credit_check_verification", "loan_terms_selection",
}

# Small per-step baseline abandonment probability, reflecting overall journey
# friction independent of any single step's errors.
JOURNEY_BASE_ABANDON = {
    "account_opening": 0.015,
    "credit_application": 0.025,
    "bank_transfer": 0.008,
    "personal_data_update": 0.010,
}

CUSTOMER_SEGMENTS = ["new_customer", "existing_customer", "premium_customer"]
CUSTOMER_SEGMENT_WEIGHTS = [0.30, 0.55, 0.15]
SEGMENT_ABANDON_ADJUSTMENT = {
    "new_customer": 0.015,
    "existing_customer": 0.0,
    "premium_customer": -0.005,
}

AGE_GROUPS = ["18-25", "26-35", "36-45", "46-60", "60+"]
AGE_GROUP_WEIGHTS = [0.15, 0.30, 0.25, 0.20, 0.10]
AGE_ABANDON_ADJUSTMENT = {
    "18-25": 0.0, "26-35": 0.0, "36-45": 0.0, "46-60": 0.005, "60+": 0.02,
}

CHANNELS = ["mobile_app", "web_browser", "branch_assisted_digital"]
CHANNEL_WEIGHTS = [0.55, 0.35, 0.10]

# Device type depends on the channel (e.g. mobile_app sessions are mostly, but
# not exclusively, on a phone).
CHANNEL_DEVICE_WEIGHTS = {
    "mobile_app": {"mobile": 0.85, "desktop": 0.05, "tablet": 0.10},
    "web_browser": {"mobile": 0.15, "desktop": 0.65, "tablet": 0.20},
    "branch_assisted_digital": {"mobile": 0.05, "desktop": 0.90, "tablet": 0.05},
}
DEVICE_ABANDON_ADJUSTMENT = {"mobile": 0.01, "desktop": 0.0, "tablet": 0.005}

SUPPORT_MITIGATION_FACTOR = 0.45  # abandon probability is multiplied by this if
                                   # the customer contacted support on this step.

ABANDONMENT_REASONS = [
    "too_long_or_complex", "technical_error", "changed_mind", "missing_information",
]

SESSION_PERIOD_DAYS = 90
REFERENCE_END_DATE = pd.Timestamp("2026-06-01")

# Deliberate, documented data-quality issues (see data/README.md "Known data quality issues").
# A real event-logging pipeline is never perfectly clean; without at least a little mess here,
# Phase 4 (data_cleaning.py) would have nothing genuine to detect and fix.
DUPLICATE_ROW_FRACTION = 0.003    # retried network calls double-logging the same event
MISSING_DEVICE_FRACTION = 0.006   # device-detection failures on the client
CHANNEL_CASING_FRACTION = 0.004   # inconsistent casing from an older app version


# ---------------------------------------------------------------------------
# Customer pool
# ---------------------------------------------------------------------------

def generate_customer_pool(rng):
    """Create a fixed pool of customers with stable segment/age attributes."""
    segments = rng.choice(CUSTOMER_SEGMENTS, size=N_CUSTOMERS, p=CUSTOMER_SEGMENT_WEIGHTS)
    age_groups = rng.choice(AGE_GROUPS, size=N_CUSTOMERS, p=AGE_GROUP_WEIGHTS)
    customer_ids = [f"CUST{i + 1:06d}" for i in range(N_CUSTOMERS)]
    return pd.DataFrame({
        "customer_id": customer_ids,
        "customer_segment": segments,
        "age_group": age_groups,
    })


# ---------------------------------------------------------------------------
# Session planning (who, which journey, which channel/device, when)
# ---------------------------------------------------------------------------

def plan_sessions(customer_pool, rng):
    """Assign each of N_SESSIONS a customer, a journey, a channel/device, and a start time."""
    customer_rows = customer_pool.sample(
        n=N_SESSIONS, replace=True, random_state=rng.integers(0, 2**32 - 1)
    ).reset_index(drop=True)

    journey_types = rng.choice(
        list(JOURNEY_WEIGHTS.keys()), size=N_SESSIONS, p=list(JOURNEY_WEIGHTS.values())
    )
    channels = rng.choice(CHANNELS, size=N_SESSIONS, p=CHANNEL_WEIGHTS)

    device_types = []
    for channel in channels:
        weights = CHANNEL_DEVICE_WEIGHTS[channel]
        device_types.append(rng.choice(list(weights.keys()), p=list(weights.values())))

    offsets_seconds = rng.uniform(0, SESSION_PERIOD_DAYS * 24 * 3600, size=N_SESSIONS)
    start_times = REFERENCE_END_DATE - pd.to_timedelta(offsets_seconds, unit="s")

    plan = customer_rows.copy()
    plan["journey_type"] = journey_types
    plan["channel"] = channels
    plan["device_type"] = device_types
    plan["start_time"] = start_times

    # Chronological order makes sequential IDs meaningful (earliest session = ID 1).
    plan = plan.sort_values("start_time").reset_index(drop=True)
    plan["session_id"] = [f"SESS{i + 1:06d}" for i in range(N_SESSIONS)]
    plan["journey_id"] = [f"JRNY{i + 1:06d}" for i in range(N_SESSIONS)]
    return plan


# ---------------------------------------------------------------------------
# Abandonment reason (only assigned on the last row of an abandoned session)
# ---------------------------------------------------------------------------

def pick_abandonment_reason(step_name, error_count, duration, mean_duration, rng):
    """Pick a plausible reason, weighted by what actually happened on this step."""
    weights = {reason: 1.0 for reason in ABANDONMENT_REASONS}

    if error_count >= 2:
        weights["technical_error"] += 4.0
    elif error_count == 1:
        weights["technical_error"] += 1.5

    if duration > mean_duration * 1.5 and error_count == 0:
        weights["too_long_or_complex"] += 3.0

    if step_name in {"document_upload", "income_details"} and error_count >= 1:
        weights["missing_information"] += 3.0

    reasons = list(weights.keys())
    probs = np.array(list(weights.values()))
    probs = probs / probs.sum()
    return rng.choice(reasons, p=probs)


# ---------------------------------------------------------------------------
# Core simulation: walk one session through its journey, step by step
# ---------------------------------------------------------------------------

def simulate_session(session, rng):
    """Return the list of step-event rows produced by one journey attempt."""
    steps = JOURNEYS[session["journey_type"]]
    rows = []
    current_time = session["start_time"]
    completed = False
    abandoned = False
    abandonment_reason = None

    for step_order, step_name in enumerate(steps, start=1):
        mean_duration, std_duration = STEP_DURATION_PARAMS[step_name]
        duration = max(3.0, rng.normal(mean_duration, std_duration))
        if session["device_type"] == "mobile" and step_name in COMPLEX_STEPS:
            duration *= 1.15

        error_count = int(rng.poisson(STEP_ERROR_LAMBDA[step_name]))

        support_prob = min(0.6, 0.05 + error_count * 0.15)
        support_contact = bool(rng.random() < support_prob)
        if support_contact:
            duration += rng.uniform(60, 180)

        current_time = current_time + pd.Timedelta(seconds=duration + rng.uniform(1, 4))

        is_last_step = step_order == len(steps)
        abandon_prob = JOURNEY_BASE_ABANDON[session["journey_type"]]
        abandon_prob += error_count * STEP_ABANDON_PER_ERROR[step_name]
        abandon_prob += SEGMENT_ABANDON_ADJUSTMENT[session["customer_segment"]]
        abandon_prob += AGE_ABANDON_ADJUSTMENT[session["age_group"]]
        if step_name in COMPLEX_STEPS:
            abandon_prob += DEVICE_ABANDON_ADJUSTMENT[session["device_type"]]
        if support_contact:
            abandon_prob *= SUPPORT_MITIGATION_FACTOR
        abandon_prob = max(0.0, min(abandon_prob, 0.85))

        # The final confirmation step cannot itself be "abandoned" into nothing:
        # reaching it means the journey is complete.
        if not is_last_step and rng.random() < abandon_prob:
            abandoned = True
            abandonment_reason = pick_abandonment_reason(
                step_name, error_count, duration, mean_duration, rng
            )
        elif is_last_step:
            completed = True

        rows.append({
            "customer_id": session["customer_id"],
            "session_id": session["session_id"],
            "journey_id": session["journey_id"],
            "journey_type": session["journey_type"],
            "customer_segment": session["customer_segment"],
            "age_group": session["age_group"],
            "channel": session["channel"],
            "device_type": session["device_type"],
            "step_name": step_name,
            "step_order": step_order,
            "step_duration_seconds": round(duration, 1),
            "error_count": error_count,
            "support_contact": support_contact,
            "timestamp": current_time,
        })

        if abandoned:
            break

    for row in rows:
        row["completed"] = completed
        row["abandoned"] = abandoned
        row["abandonment_reason"] = abandonment_reason if abandoned else None

    return rows


# ---------------------------------------------------------------------------
# Realistic data-quality noise
# ---------------------------------------------------------------------------

def inject_realistic_noise(dataset, rng):
    """Add the small, documented data-quality issues listed in data/README.md.

    Every issue introduced here is checked for explicitly in python/data_cleaning.py, so
    this function exists purely to give that later step genuine work to do.
    """
    dataset = dataset.copy()

    n_duplicates = int(len(dataset) * DUPLICATE_ROW_FRACTION)
    duplicate_rows = dataset.sample(n=n_duplicates, random_state=rng.integers(0, 2**32 - 1))
    dataset = pd.concat([dataset, duplicate_rows], ignore_index=True)

    # Device detection fails for a whole session, not for one random step in the middle of
    # it — so the affected rows are chosen by session_id, not by row index. Nulling
    # individual rows independently would let the same session show two different devices,
    # which can't happen in reality.
    session_ids = dataset["session_id"].unique()
    n_missing_sessions = max(1, int(len(session_ids) * MISSING_DEVICE_FRACTION))
    missing_sessions = rng.choice(session_ids, size=n_missing_sessions, replace=False)
    dataset.loc[dataset["session_id"].isin(missing_sessions), "device_type"] = None

    n_casing_noise = int(len(dataset) * CHANNEL_CASING_FRACTION)
    casing_idx = rng.choice(dataset.index, size=n_casing_noise, replace=False)
    dataset.loc[casing_idx, "channel"] = dataset.loc[casing_idx, "channel"].str.title()

    # Shuffle so injected rows aren't neatly appended at the end (a raw export wouldn't be).
    shuffled = dataset.sample(frac=1, random_state=rng.integers(0, 2**32 - 1))
    return shuffled.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    rng = np.random.default_rng(SEED)

    customer_pool = generate_customer_pool(rng)
    session_plan = plan_sessions(customer_pool, rng)

    all_rows = []
    for _, session in session_plan.iterrows():
        all_rows.extend(simulate_session(session, rng))

    dataset = pd.DataFrame(all_rows)
    clean_session_count = dataset["session_id"].nunique()
    completion_rate = dataset.groupby("session_id")["completed"].first().mean()
    outcomes = dataset.groupby(["journey_type", "session_id"])["abandoned"].first()
    abandonment_by_journey = outcomes.groupby("journey_type").mean().sort_values(ascending=False)

    dataset = inject_realistic_noise(dataset, rng)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    dataset.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(dataset):,} raw step-event rows across {clean_session_count:,} sessions.")
    print(f"Overall completion rate: {completion_rate:.1%}")
    print("Abandonment rate by journey_type:")
    print(abandonment_by_journey.to_string())
    print(
        f"Injected noise: {dataset.duplicated().sum()} duplicate rows, "
        f"{dataset['device_type'].isna().sum()} missing device_type, "
        f"casing issues in 'channel' (see data_cleaning.py for detection)."
    )
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
