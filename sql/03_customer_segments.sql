-- =============================================================================
-- 03_customer_segments.sql
-- Compare abandonment across customer segments, age groups, devices, and channels.
-- Answers business-questions.md #9-12. Table: journeys (one row per step event).
--
-- Every query below collapses to one row per session first (session-level attributes
-- are constant across a session's rows, so MAX/first just recovers that constant value),
-- then compares groups. As noted in business-questions.md, read these as associations,
-- not proven causes.
-- =============================================================================

-- Abandonment rate by customer_segment.
SELECT
    customer_segment,
    COUNT(*)                                      AS sessions,
    ROUND(100.0 * SUM(abandoned) / COUNT(*), 1)   AS abandonment_rate_pct
FROM (
    SELECT session_id, customer_segment, MAX(abandoned) AS abandoned
    FROM journeys
    GROUP BY session_id, customer_segment
)
GROUP BY customer_segment
ORDER BY abandonment_rate_pct DESC;

-- Abandonment rate by age_group.
SELECT
    age_group,
    COUNT(*)                                      AS sessions,
    ROUND(100.0 * SUM(abandoned) / COUNT(*), 1)   AS abandonment_rate_pct
FROM (
    SELECT session_id, age_group, MAX(abandoned) AS abandoned
    FROM journeys
    GROUP BY session_id, age_group
)
GROUP BY age_group
ORDER BY abandonment_rate_pct DESC;

-- Abandonment rate by device_type.
SELECT
    device_type,
    COUNT(*)                                      AS sessions,
    ROUND(100.0 * SUM(abandoned) / COUNT(*), 1)   AS abandonment_rate_pct
FROM (
    SELECT session_id, device_type, MAX(abandoned) AS abandoned
    FROM journeys
    GROUP BY session_id, device_type
)
GROUP BY device_type
ORDER BY abandonment_rate_pct DESC;

-- Abandonment rate by channel.
SELECT
    channel,
    COUNT(*)                                      AS sessions,
    ROUND(100.0 * SUM(abandoned) / COUNT(*), 1)   AS abandonment_rate_pct
FROM (
    SELECT session_id, channel, MAX(abandoned) AS abandoned
    FROM journeys
    GROUP BY session_id, channel
)
GROUP BY channel
ORDER BY abandonment_rate_pct DESC;

-- Cross-tab: journey_type x customer_segment, to check whether the segment effect holds
-- consistently across journeys or is concentrated in just one of them.
SELECT
    journey_type,
    customer_segment,
    COUNT(*)                                      AS sessions,
    ROUND(100.0 * SUM(abandoned) / COUNT(*), 1)   AS abandonment_rate_pct
FROM (
    SELECT session_id, journey_type, customer_segment, MAX(abandoned) AS abandoned
    FROM journeys
    GROUP BY session_id, journey_type, customer_segment
)
GROUP BY journey_type, customer_segment
ORDER BY journey_type, abandonment_rate_pct DESC;
