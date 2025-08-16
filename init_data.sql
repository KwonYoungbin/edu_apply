-- 15,000개 시험 데이터 입력
WITH generated AS (
    SELECT
        'Test ' || gs AS title,
        NOW() + (random() * interval '40 days' - interval '20 days') AS start_at,
        NOW() AS end_at
    FROM generate_series(1, 15000) AS gs
)
INSERT INTO tests_test (title, start_at, end_at, created_at)
SELECT
    title,
    start_at,
    start_at + interval '10 days' AS end_at,
    start_at - interval '10 days' AS created_at
FROM generated;

-- 15,000개 수업 데이터 입력
WITH generated AS (
    SELECT
        'Course ' || gs AS title,
        NOW() + (random() * interval '40 days' - interval '20 days') AS start_at,
        NOW() AS end_at
    FROM generate_series(1, 15000) AS gs
)
INSERT INTO courses_course (title, start_at, end_at, created_at)
SELECT
    title,
    start_at,
    start_at + interval '10 days' AS end_at,
    start_at - interval '10 days' AS created_at
FROM generated;