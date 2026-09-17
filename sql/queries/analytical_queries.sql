USE traffic_safety;

-- 1. State Fatal Crash Ranking & Fatality Rates (Window Functions)
-- Ranks states by fatal crash count and computes cumulative share of national fatalities.
WITH state_summary AS (
    SELECT 
        statename,
        COUNT(*) AS total_fatal_crashes,
        SUM(fatals) AS total_fatalities
    FROM crashes
    GROUP BY statename
)
SELECT 
    statename,
    total_fatal_crashes,
    total_fatalities,
    DENSE_RANK() OVER (ORDER BY total_fatal_crashes DESC) AS crash_rank,
    ROUND(100.0 * total_fatalities / SUM(total_fatalities) OVER (), 2) AS pct_of_national_fatalities
FROM state_summary
ORDER BY crash_rank ASC
LIMIT 15;

-- 2. Speeding & Alcohol Factor Breakdown by Vehicle Make (JOINs + Aggregation)
-- Analyzes driver behavior flags per vehicle make with at least 500 crash involvements.
SELECT 
    v.makename,
    COUNT(*) AS vehicles_involved,
    SUM(CASE WHEN v.dr_drink = 1 THEN 1 ELSE 0 END) AS alcohol_involved_count,
    ROUND(100.0 * SUM(CASE WHEN v.dr_drink = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_alcohol_involved,
    SUM(CASE WHEN v.speedrel IN (2, 3, 4, 5) THEN 1 ELSE 0 END) AS speed_related_count,
    ROUND(100.0 * SUM(CASE WHEN v.speedrel IN (2, 3, 4, 5) THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_speed_related
FROM vehicles v
WHERE v.makename IS NOT NULL AND v.makename != 'Unknown'
GROUP BY v.makename
HAVING COUNT(*) >= 500
ORDER BY vehicles_involved DESC;

-- 3. Restraint Usage vs. Injury Severity (Cross-table Person Analysis)
-- Evaluates the fatality and serious injury rate broken down by restraint systems.
SELECT 
    p.rest_usename AS restraint_system,
    COUNT(*) AS total_occupants,
    SUM(CASE WHEN p.inj_sev = 4 THEN 1 ELSE 0 END) AS total_fatalities,
    ROUND(100.0 * SUM(CASE WHEN p.inj_sev = 4 THEN 1 ELSE 0 END) / COUNT(*), 2) AS fatality_rate_pct
FROM people p
WHERE p.veh_no != 0 AND p.rest_usename IS NOT NULL
GROUP BY p.rest_usename
HAVING COUNT(*) >= 200
ORDER BY fatality_rate_pct DESC;

-- 4. Hourly Crash Distribution: Rural vs. Urban (CTEs + Pivot/Conditional Aggregation)
SELECT 
    hour,
    SUM(CASE WHEN rur_urb = 1 THEN 1 ELSE 0 END) AS rural_crashes,
    SUM(CASE WHEN rur_urb = 2 THEN 1 ELSE 0 END) AS urban_crashes,
    COUNT(*) AS total_crashes
FROM crashes
WHERE hour BETWEEN 0 AND 23
GROUP BY hour
ORDER BY hour ASC;