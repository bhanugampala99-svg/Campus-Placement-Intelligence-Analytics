-- Campus Placement Intelligence Analytics
-- SQL queries for key business questions
-- Assumes table name: placement_data
-- Columns: student_id, name, gender, category, branch, college_tier,
--          cgpa, internships, certifications, skills, placement_status,
--          company_type, ctc_lakhs, location

-- 1. Overall placement rate
SELECT
    COUNT(*) AS total_students,
    SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_students,
    CAST(SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS FLOAT) * 100 / COUNT(*) AS placement_rate_pct
FROM placement_data;

-- 2. Placement rate by branch
SELECT
    branch,
    COUNT(*) AS total_students,
    SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_students,
    CAST(SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS FLOAT) * 100 / COUNT(*) AS placement_rate_pct
FROM placement_data
GROUP BY branch
ORDER BY placement_rate_pct DESC;

-- 3. Placement rate by college tier
SELECT
    college_tier,
    COUNT(*) AS total_students,
    SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_students,
    CAST(SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS FLOAT) * 100 / COUNT(*) AS placement_rate_pct
FROM placement_data
GROUP BY college_tier
ORDER BY placement_rate_pct DESC;

-- 4. Average CTC by branch (placed students only)
SELECT
    branch,
    COUNT(*) AS placed_students,
    AVG(ctc_lakhs) AS avg_ctc_lakhs
FROM placement_data
WHERE placement_status = 'Placed'
GROUP BY branch
ORDER BY avg_ctc_lakhs DESC;

-- 5. Average CTC by college tier and CGPA band (placed students)
SELECT
    college_tier,
    CASE
        WHEN cgpa >= 8.0 THEN '8.0+'
        WHEN cgpa >= 7.0 THEN '7.0-7.9'
        WHEN cgpa >= 6.0 THEN '6.0-6.9'
        ELSE '<6.0'
    END AS cgpa_band,
    COUNT(*) AS placed_students,
    AVG(ctc_lakhs) AS avg_ctc_lakhs
FROM placement_data
WHERE placement_status = 'Placed'
GROUP BY college_tier, cgpa_band
ORDER BY college_tier, avg_ctc_lakhs DESC;

-- 6. Placement rate and avg CTC by gender
SELECT
    gender,
    COUNT(*) AS total_students,
    SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_students,
    CAST(SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) AS FLOAT) * 100 / COUNT(*) AS placement_rate_pct,
    AVG(CASE WHEN placement_status = 'Placed' THEN ctc_lakhs ELSE NULL END) AS avg_ctc_lakhs
FROM placement_data
GROUP BY gender;

-- 7. Company type-wise average CTC (placed students)
SELECT
    company_type,
    COUNT(*) AS placed_students,
    AVG(ctc_lakhs) AS avg_ctc_lakhs,
    MIN(ctc_lakhs) AS min_ctc_lakhs,
    MAX(ctc_lakhs) AS max_ctc_lakhs
FROM placement_data
WHERE placement_status = 'Placed'
GROUP BY company_type
ORDER BY avg_ctc_lakhs DESC;