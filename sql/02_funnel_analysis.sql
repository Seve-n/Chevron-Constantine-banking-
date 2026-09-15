-- =============================================================================
-- 02_funnel_analysis.sql
-- Step-by-step funnel: where customers drop off within each journey.
-- Answers business-questions.md #3-5. Table: journeys (one row per step event).
-- =============================================================================

-- Per-step summary: how many sessions reach each step, their average duration and
-- error rate. Run per journey_type because step sequences differ between journeys
-- (see data/README.md).
SELECT
    journey_type,
    step_order,
    step_name,
    COUNT(DISTINCT session_id)                                           AS sessions_reaching_step,
    ROUND(AVG(step_duration_seconds), 1)                                 AS avg_duration_seconds,
    ROUND(100.0 * SUM(CASE WHEN error_count > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS error_rate_pct
FROM journeys
GROUP BY journey_type, step_order, step_name
ORDER BY journey_type, step_order;

-- Drop-off rate: the percentage of sessions that reached a step but never reached the
-- next one. Uses LEAD() to compare each step's session count with the following step's,
-- within the same journey_type.
--
-- NOTE: the last step of each journey (e.g. "confirmation") has no next step to compare
-- against, so LEAD() is NULL there and drop_off_rate_pct is correctly left NULL too —
-- do NOT coalesce that NULL to 0, or the last step would misleadingly show 100% drop-off
-- (there's nothing to "drop off" into once the journey is already finished).
WITH step_counts AS (
    SELECT
        journey_type,
        step_order,
        step_name,
        COUNT(DISTINCT session_id) AS sessions_reaching_step
    FROM journeys
    GROUP BY journey_type, step_order, step_name
)
SELECT
    journey_type,
    step_order,
    step_name,
    sessions_reaching_step,
    LEAD(sessions_reaching_step) OVER (PARTITION BY journey_type ORDER BY step_order)
        AS sessions_reaching_next_step,
    ROUND(
        100.0 * (
            sessions_reaching_step
            - LEAD(sessions_reaching_step) OVER (PARTITION BY journey_type ORDER BY step_order)
        ) / sessions_reaching_step,
        1
    ) AS drop_off_rate_pct
FROM step_counts
ORDER BY journey_type, step_order;

-- The 5 single (journey_type, step) combinations with the highest drop-off rate —
-- a direct answer to "which step should Chevron Constantine Banking fix first?" (business-questions.md #13).
WITH step_counts AS (
    SELECT
        journey_type,
        step_order,
        step_name,
        COUNT(DISTINCT session_id) AS sessions_reaching_step
    FROM journeys
    GROUP BY journey_type, step_order, step_name
),
drop_off AS (
    SELECT
        journey_type,
        step_order,
        step_name,
        sessions_reaching_step,
        ROUND(
            100.0 * (
                sessions_reaching_step
                - COALESCE(
                    LEAD(sessions_reaching_step) OVER (PARTITION BY journey_type ORDER BY step_order),
                    0
                )
            ) / sessions_reaching_step,
            1
        ) AS drop_off_rate_pct
    FROM step_counts
)
SELECT *
FROM drop_off
WHERE step_order < (SELECT MAX(step_order) FROM drop_off d2 WHERE d2.journey_type = drop_off.journey_type)
ORDER BY drop_off_rate_pct DESC
LIMIT 5;
