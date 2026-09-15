"""
KPI calculations for the Banking Customer Journey Analysis project.

Loads the cleaned dataset and computes the KPIs defined in business-analysis/project-brief.md.
These functions are the single source of truth for KPI definitions: the notebook (Phase 11)
and the dashboard specification (Phase 12) all reuse them, so a number means the same thing
everywhere in this project.
"""

import os

import pandas as pd

PROCESSED_PATH = os.path.join("data", "processed", "banking_customer_journeys_clean.csv")


def load_processed_data(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df


# ---------------------------------------------------------------------------
# Session-level table
# ---------------------------------------------------------------------------

def build_session_table(df):
    """Collapse the step-event table to one row per session.

    Most business KPIs (completion, abandonment, journey duration) are properties of the
    whole journey attempt, not of a single step — so they need this session-level view
    rather than the raw step-event rows.
    """
    sessions = df.groupby("session_id").agg(
        customer_id=("customer_id", "first"),
        journey_type=("journey_type", "first"),
        customer_segment=("customer_segment", "first"),
        age_group=("age_group", "first"),
        channel=("channel", "first"),
        device_type=("device_type", "first"),
        completed=("completed", "first"),
        abandoned=("abandoned", "first"),
        abandonment_reason=("abandonment_reason", "first"),
        journey_duration_seconds=("step_duration_seconds", "sum"),
        steps_reached=("step_order", "max"),
        total_errors=("error_count", "sum"),
        contacted_support=("support_contact", "max"),
    ).reset_index()
    return sessions


# ---------------------------------------------------------------------------
# KPI functions
# ---------------------------------------------------------------------------

def completion_rate(sessions, by=None):
    if by:
        return sessions.groupby(by)["completed"].mean().sort_values(ascending=False)
    return sessions["completed"].mean()


def abandonment_rate(sessions, by=None):
    if by:
        return sessions.groupby(by)["abandoned"].mean().sort_values(ascending=False)
    return sessions["abandoned"].mean()


def average_journey_duration(sessions, by=None):
    if by:
        return sessions.groupby(by)["journey_duration_seconds"].mean().sort_values(ascending=False)
    return sessions["journey_duration_seconds"].mean()


def average_step_duration(df, by="step_name"):
    return df.groupby(by)["step_duration_seconds"].mean().sort_values(ascending=False)


def error_rate(df, by="step_name"):
    """Share of visits to a step that had at least one error."""
    return df.groupby(by)["error_count"].apply(lambda errors: (errors > 0).mean()).sort_values(ascending=False)


def support_contact_rate(sessions, by=None):
    """Share of sessions that contacted support at least once during the journey."""
    if by:
        return sessions.groupby(by)["contacted_support"].mean().sort_values(ascending=False)
    return sessions["contacted_support"].mean()


# ---------------------------------------------------------------------------
# Funnel analysis
# ---------------------------------------------------------------------------

def build_funnel_table(df):
    """One row per (journey_type, step): volume, drop-off, duration, and error rate.

    `sessions_reaching_next_step` is the Python equivalent of the SQL LEAD() window
    function: within each journey_type, ordered by step_order, look at the next row.
    The last step of a journey has no next step, so it's left NaN rather than treated
    as "0 sessions continued" — otherwise it would misleadingly show 100% drop-off.
    """
    funnel = df.groupby(["journey_type", "step_order", "step_name"]).agg(
        sessions_reaching_step=("session_id", "nunique"),
        avg_duration_seconds=("step_duration_seconds", "mean"),
        error_rate_pct=("error_count", lambda errors: 100 * (errors > 0).mean()),
    ).reset_index()

    funnel = funnel.sort_values(["journey_type", "step_order"])
    funnel["sessions_reaching_next_step"] = (
        funnel.groupby("journey_type")["sessions_reaching_step"].shift(-1)
    )
    funnel["customers_lost_at_step"] = (
        funnel["sessions_reaching_step"] - funnel["sessions_reaching_next_step"]
    )
    funnel["drop_off_rate_pct"] = (
        100 * funnel["customers_lost_at_step"] / funnel["sessions_reaching_step"]
    )
    return funnel.reset_index(drop=True)


def rank_problem_steps(funnel, top_n=5):
    """Rank steps by absolute customers lost — volume x severity, not severity alone.

    A step with a high drop-off *rate* but very few visits matters less than a step
    with a moderate rate but high traffic. Ranking by the raw count answers "which
    single fix would save the most customers?", which is what a Product Manager
    actually needs to prioritize a backlog (see business-analysis/stakeholders.md).
    """
    ranked = funnel.dropna(subset=["customers_lost_at_step"]).copy()
    ranked = ranked.sort_values("customers_lost_at_step", ascending=False)
    columns = [
        "journey_type", "step_name", "sessions_reaching_step",
        "customers_lost_at_step", "drop_off_rate_pct", "error_rate_pct",
    ]
    return ranked[columns].head(top_n)


def segment_breakdown_for_step(df, journey_type, step_name, dimension):
    """Drill into one funnel step: is abandonment there concentrated in one group?

    Restricted to sessions that actually reached this exact step, so the comparison
    is fair (e.g. comparing segments only among people who got this far, not among
    everyone who ever started the journey).
    """
    step_rows = df[(df["journey_type"] == journey_type) & (df["step_name"] == step_name)].copy()
    step_rows["is_last_visit"] = (
        step_rows.groupby("session_id")["step_order"].transform("max") == step_rows["step_order"]
    )

    summary = step_rows.groupby(dimension).agg(
        sessions_reaching_step=("session_id", "nunique"),
        error_rate_pct=("error_count", lambda errors: 100 * (errors > 0).mean()),
    )

    abandoned_here = step_rows[step_rows["is_last_visit"] & step_rows["abandoned"]]
    summary["abandoned_at_this_step"] = abandoned_here.groupby(dimension)["session_id"].nunique()
    summary["abandoned_at_this_step"] = summary["abandoned_at_this_step"].fillna(0).astype(int)
    summary["abandonment_rate_at_step_pct"] = (
        100 * summary["abandoned_at_this_step"] / summary["sessions_reaching_step"]
    )
    return summary.sort_values("abandonment_rate_at_step_pct", ascending=False)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_section(title):
    print(f"\n--- {title} ---")


def main():
    df = load_processed_data(PROCESSED_PATH)
    sessions = build_session_table(df)

    print(f"Loaded {len(df):,} step-event rows across {len(sessions):,} sessions.\n")

    print_section("Overall KPIs")
    print(f"Completion rate:        {completion_rate(sessions):.1%}")
    print(f"Abandonment rate:       {abandonment_rate(sessions):.1%}")
    print(f"Avg. journey duration:  {average_journey_duration(sessions):.0f} sec")
    print(f"Support contact rate:   {support_contact_rate(sessions):.1%}")

    print_section("Average step duration (seconds, all journeys)")
    print(average_step_duration(df).round(1).to_string())

    print_section("Error rate by step (share of visits with >=1 error)")
    print(error_rate(df).apply(lambda x: f"{x:.1%}").to_string())

    print_section("Abandonment rate by journey_type")
    print(abandonment_rate(sessions, by="journey_type").apply(lambda x: f"{x:.1%}").to_string())

    print_section("Abandonment rate by device_type")
    print(abandonment_rate(sessions, by="device_type").apply(lambda x: f"{x:.1%}").to_string())

    print_section("Abandonment rate by customer_segment")
    print(abandonment_rate(sessions, by="customer_segment").apply(lambda x: f"{x:.1%}").to_string())

    funnel = build_funnel_table(df)

    print_section("Top 5 steps by customers lost (volume x severity)")
    top_problems = rank_problem_steps(funnel, top_n=5)
    print(top_problems.round(1).to_string(index=False))

    print_section("Drill-down: credit_check_verification abandonment by customer_segment")
    breakdown = segment_breakdown_for_step(
        df, "credit_application", "credit_check_verification", "customer_segment"
    )
    print(breakdown.round(1).to_string())


if __name__ == "__main__":
    main()
