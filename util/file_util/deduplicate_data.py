import csv
import json
from collections import defaultdict
# 去除网站二级tag里的重复数据(category_name,tags)
def extract_categories_and_tags(input_file, output_file):
    unique_rows = set()
    original_count = 0

    # 读取输入CSV文件
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            original_count += 1
            category = row['category_name']
            tags = row['tags']
            
            # 将行转换为可哈希的元组并添加到集合中
            unique_rows.add((category, tags))

    # 将unique categories和tags写入CSV文件
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['category_name', 'tags'])
        for row in unique_rows:
            writer.writerow(row)

    print(f"提取完成。原始数据条数：{original_count}")
    print(f"去重后数据条数：{len(unique_rows)}")

# 去重网站标准csv数据(category_name,tags,site,name)里的重复数据
def deduplicate_csv(input_file, output_file):
    # 使用defaultdict来存储唯一的数据
    unique_data = defaultdict(dict)
    original_count = 0

    # 读取输入CSV文件
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            original_count += 1
            # 使用category_name和site作为键
            key = (row['category_name'], row['site'])
            # 如果这个键还不存在，就添加整行数据
            if key not in unique_data:
                unique_data[key] = row

    # 将去重后的数据写入新的CSV文件
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['category_name', 'tags', 'site', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in unique_data.values():
            writer.writerow(row)

    print(f"去重完成。原始数据条数：{original_count}, 去重后数据条数：{len(unique_data)}")

import pandas as pd

def merge_categories(input_file, output_file):
    """
    根据指定规则合并标签。

    :param input_file: 原始 CSV 文件路径
    :param output_file: 合并后的 CSV 文件路径
    """
    # 读取原始 CSV 文件
    df = pd.read_csv(input_file)

    # 定义合并规则
    merge_dict = {
        '广告工具': '营销工具',
        '引流工具': '营销工具',
        
        '全球接码': '接码服务',
        '虚拟邮箱': '接码服务'
    }

    # 更新一级标签
    df['category_name'] = df['category_name'].replace(merge_dict)

    # 保存结果到新的 CSV 文件
    df.to_csv(output_file, index=False)

    print("标签合并成功！文件已保存到：", output_file)

if __name__ == "__main__":
    input_file = '../../Data/error.csv'  # 输入文件路径
    output_file = '../../Data/error_dep.csv'  # 输出文件路径
    # extract_categories_and_tags(input_file, output_file)
    # deduplicate_csv(input_file, output_file)
    merge_categories('./categories_and_tags.csv', './new_category.csv')