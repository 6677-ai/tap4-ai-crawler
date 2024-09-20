import pandas as pd
import ast  # 用于处理字符串格式的列表

# 读取原始 CSV 文件
df = pd.read_csv('../../Data/website_data_flag.csv')

# 新增 name 列
df['name'] = df['site']

# 新增 category_name 列并设置为 'proxy'
df['category_name'] = 'proxy'

# 调整列的顺序
df = df[['category_name', 'tags', 'site', 'name']]

# 保存到一个新的 CSV 文件
df.to_csv('../../Data/website_data_flag.csv', index=False)