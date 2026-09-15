"""
Data quality checks and cleaning for the Banking Customer Journey Analysis project.

Loads the raw synthetic dataset, reports on its data quality (missing values, duplicates,
categorical inconsistencies, business-rule violations), fixes what can legitimately be
fixed, and writes a cleaned dataset to data/processed/. See data/README.md for the schema
and the specific issues this script is expected to find.
"""

import os

import pandas as pd

from data_generation import JOURNEYS

RAW_PATH = os.path.join("data", "raw", "banking_customer_journeys.csv")
PROCESSED_PATH = os.path.join("data", "processed", "banking_customer_journeys_clean.csv")

# Columns that hold a fixed, small set of category labels (as opposed to free-form IDs).
CATEGORICAL_COLUMNS = [
    "journey_type", "customer_segment", "age_group",
    "channel", "device_type", "step_name", "abandonment_reason",
]


def load_raw_data(path):
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# Quality checks (report only — no mutation)
# ---------------------------------------------------------------------------

def report_missing_values(df):
    missing = df.isna().sum()
    missing = missing[missing > 0]
    print("Missing values by column:")
    if missing.empty:
        print("  none")
    else:
        for column, count in missing.items():
            print(f"  {column}: {count} ({count / len(df):.2%})")


def report_duplicates(df):
    n_duplicates = int(df.duplicated().sum())
    print(f"Exact duplicate rows: {n_duplicates} ({n_duplicates / len(df):.2%})")
    return n_duplicates


def report_categorical_inconsistencies(df):
    """Surface casing/whitespace inconsistencies by showing raw unique values per column."""
    print("Distinct raw values per categorical column (watch for casing variants):")
    for column in CATEGORICAL_COLUMNS:
        raw_values = df[column].dropna().unique()
        normalized_values = {str(v).strip().lower() for v in raw_values}
        if len(raw_values) != len(normalized_values):
            print(f"  {column}: {sorted(str(v) for v in raw_values)}  <- inconsistent casing")
        else:
            print(f"  {column}: {len(raw_values)} clean values")


def report_business_rule_violations(df):
    """Check two rules that must always hold, regardless of any generation randomness:
    (1) a session is either completed or abandoned, never both, never neither;
    (2) abandonment_reason is set exactly when abandoned is True.
    """
    outcome_conflicts = df[df["completed"] == df["abandoned"]]
    print(f"Rows where completed == abandoned (should be 0): {len(outcome_conflicts)}")

    reason_mismatch = df[df["abandoned"] != df["abandonment_reason"].notna()]
    print(f"Rows where abandonment_reason disagrees with abandoned (should be 0): {len(reason_mismatch)}")


def report_step_sequence_violations(df):
    """Check every (journey_type, step_order) pair actually matches the official journey
    definition in data_generation.py — a referential-integrity check against the schema.
    """
    expected_rows = [
        {"journey_type": journey_type, "step_order": order, "expected_step_name": name}
        for journey_type, steps in JOURNEYS.items()
        for order, name in enumerate(steps, start=1)
    ]
    expected = pd.DataFrame(expected_rows)

    merged = df.merge(expected, on=["journey_type", "step_order"], how="left")
    mismatches = merged[merged["step_name"] != merged["expected_step_name"]]
    print(f"Rows with a step_name/step_order that doesn't match the journey definition: {len(mismatches)}")


# ---------------------------------------------------------------------------
# Cleaning (mutates and returns a new, cleaned DataFrame)
# ---------------------------------------------------------------------------

def clean_data(df):
    df = df.drop_duplicates().copy()

    # Normalize casing/whitespace on category-label columns only — never on ID columns,
    # where case is meaningful (e.g. "CUST002170").
    for column in CATEGORICAL_COLUMNS:
        df[column] = df[column].astype("string").str.strip().str.lower()

    # device_type can legitimately fail to be detected client-side. Dropping those rows
    # would discard real customer interactions just because one attribute is unknown, so
    # they're kept and labeled "unknown" instead — visible in any device-level breakdown
    # rather than silently disappearing from the funnel counts.
    df["device_type"] = df["device_type"].fillna("unknown")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Casing normalization can turn two previously-distinct rows (e.g. "Mobile_App" vs
    # "mobile_app") into exact duplicates. Re-check now — dropping only before normalizing
    # would miss this.
    df = df.drop_duplicates()

    for column in CATEGORICAL_COLUMNS:
        df[column] = df[column].astype("category")
    for column in ["completed", "abandoned", "support_contact"]:
        df[column] = df[column].astype(bool)
    for column in ["step_order", "error_count"]:
        df[column] = df[column].astype(int)

    df = df.sort_values(["session_id", "step_order"]).reset_index(drop=True)
    return df


def save_processed_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    raw = load_raw_data(RAW_PATH)
    print(f"Loaded {len(raw):,} rows from {RAW_PATH}\n")

    print("=== Data quality report (raw) ===")
    report_missing_values(raw)
    report_duplicates(raw)
    report_categorical_inconsistencies(raw)
    report_business_rule_violations(raw)
    report_step_sequence_violations(raw)

    cleaned = clean_data(raw)

    print("\n=== Data quality report (cleaned) ===")
    report_missing_values(cleaned)
    report_duplicates(cleaned)
    report_categorical_inconsistencies(cleaned)

    save_processed_data(cleaned, PROCESSED_PATH)
    print(f"\nRows: {len(raw):,} raw -> {len(cleaned):,} cleaned")
    print(f"Saved to: {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
