-- 查看有多少条数据
SELECT COUNT(*) FROM category WHERE category_name = '';

-- 更改category_name
UPDATE category
SET category_name = ' '
WHERE category_name = '';
