-- 시험 초기 데이터(15,000개) 입력
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


-- 수업 초기 데이터(15,000개) 입력
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


-- 수업 데이터에 태그 랜덤 매핑
WITH course_ids AS (
    SELECT id FROM courses_course
),
tag_ids AS (
    SELECT id FROM courses_tag
)
INSERT INTO courses_course_tags (course_id, tag_id)
SELECT
    c.id AS course_id,
    t.id AS tag_id
FROM course_ids c,
LATERAL (
    SELECT id
    FROM tag_ids
    ORDER BY md5(c.id::text || random()::text)  -- Course ID 기반으로 랜덤 정렬
    LIMIT (1 + floor(random()*3)::int)
) t;