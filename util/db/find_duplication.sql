
-- 查找 web_navigation 中是否有重复元素
SELECT name, COUNT(*) AS count
FROM web_navigation
GROUP BY name
HAVING COUNT(*) > 1;