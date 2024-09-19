
-- 查找 web_navigation 中是否有重复元素
SELECT name, COUNT(*) AS count
FROM web_navigation
GROUP BY name
HAVING COUNT(*) > 1;

-- 修改数据库的category_name
UPDATE web_navigation
SET category_name = '["AI Tools"]'::jsonb
WHERE id BETWEEN 92 AND 177;

UPDATE web_navigation
SET tag_name = tag_name::jsonb -> 0
WHERE id BETWEEN 92 AND 177;

UPDATE web_navigation
SET tag_name = '["Common AI Tools"]'::jsonb
WHERE id BETWEEN 92 AND 105;

-- 更新原来英文为中文
UPDATE web_navigation
SET tag_name = '["AI Writing Tool"]'::jsonb
WHERE id BETWEEN 119 AND 134;

UPDATE web_navigation
SET tag_name = '["AI Video Tools"]'::jsonb
WHERE id BETWEEN 135 AND 149;


UPDATE web_navigation
SET tag_name = '["AI Design Tools"]'::jsonb
WHERE id BETWEEN 150 AND 163;

UPDATE web_navigation
SET tag_name = '["AI Programming Tools"]'::jsonb
WHERE id BETWEEN 164 AND 176;

