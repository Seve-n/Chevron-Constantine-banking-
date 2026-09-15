-- =============================================================================
-- 01_basic_kpis.sql
-- Overall KPIs for the Banking Customer Journey Analysis project.
-- Answers business-questions.md #1-2. Table: journeys (one row per step event).
-- Load the data first with: python sql/load_to_sqlite.py
-- =============================================================================

-- Completion rate & abandonment rate.
-- `completed`/`abandoned` are repeated on every row of a session (see data/README.md), so
-- we must first collapse to one row per session (MAX picks up the constant value) before
-- averaging — averaging over raw rows would overweight sessions with more recorded steps.
SELECT
    COUNT(*)                                          AS total_sessions,
    ROUND(100.0 * SUM(completed) / COUNT(*), 1)       AS completion_rate_pct,
    ROUND(100.0 * SUM(abandoned) / COUNT(*), 1)       AS abandonment_rate_pct
FROM (
    SELECT session_id, MAX(completed) AS completed, MAX(abandoned) AS abandoned
    FROM journeys
    GROUP BY session_id
);

-- Average journey duration (sum of step durations within a session, then averaged
-- across sessions).
SELECT
    ROUND(AVG(total_duration_seconds), 1) AS avg_journey_duration_seconds
FROM (
    SELECT session_id, SUM(step_duration_seconds) AS total_duration_seconds
    FROM journeys
    GROUP BY session_id
);

-- Average step duration, across all journeys, longest first.
SELECT
    step_name,
    ROUND(AVG(step_duration_seconds), 1) AS avg_duration_seconds
FROM journeys
GROUP BY step_name
ORDER BY avg_duration_seconds DESC;

-- Error rate per step: share of visits to that step with at least one error.
SELECT
    step_name,
    COUNT(*)                                                              AS visits,
    ROUND(100.0 * SUM(CASE WHEN error_count > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS error_rate_pct
FROM journeys
GROUP BY step_name
ORDER BY error_rate_pct DESC;

-- Support contact rate: share of sessions that contacted support at least once.
SELECT
    ROUND(100.0 * SUM(contacted_support) / COUNT(*), 1) AS support_contact_rate_pct
FROM (
    SELECT session_id, MAX(support_contact) AS contacted_support
    FROM journeys
    GROUP BY session_id
);
