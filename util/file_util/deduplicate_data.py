import csv
import json
import pandas as pd
from collections import defaultdict

def extract_categories_and_tags(input_file, output_file):
    """
        去除网站二级tag里的重复数据(category_name,tags)
    """
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

def deduplicate_csv(input_file, output_file):
    """
        去重网站标准csv数据(category_name,tags,site,name)里的重复数据
    """
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

def merge_categories_by_code(input_file, output_file, code1, code2, new_code):
    """
    合并两个指定 code 的类别为一个新的类别，只更改 code。
    如果新 code 与原有 code 之一相同，则保留该行的所有数据
    :param input_file: 输入CSV文件的路径
    :param output_file: 输出CSV文件的路径
    :param code1: 要合并的第一个类别的 code
    :param code2: 要合并的第二个类别的 code
    :param new_code: 新类别的 code
    """
    # 读取CSV文件
    df = pd.read_csv(input_file,dtype={'sort': 'Int64','create_by': 'Int64', 'del_flag': 'Int64'})
    
    # 找到需要合并的行的索引
    index1 = df[df['code'] == code1].index[0]
    index2 = df[df['code'] == code2].index[0]
    new_code_index = df[df['code'] == new_code].index
    if not new_code_index.empty:
        # 如果新 code 已存在，保留该行数据
        df = df.drop(index1)
        df = df.drop(index2)
    elif new_code in [code1, code2]:
        # 如果新 code 与 code1 或 code2 相同，保留对应的行
        keep_index = index1 if new_code == code1 else index2
        drop_index = index2 if new_code == code1 else index1
        df.loc[keep_index, 'code'] = new_code
        df = df.drop(drop_index)
    else:
        # 如果新 code 与两个原有 code 都不同，创建新行
        new_row = pd.Series(dtype='object')
        new_row['code'] = new_code
        new_row['name_cn'] = new_code
        new_row['categoryId'] = df['categoryId'].max() + 1
        df = df.drop([index1, index2])
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    

    df = df.sort_values('categoryId')
    
    df['categoryId'] = range(1, len(df) + 1)
    
    # 保存修改后的CSV文件
    df.to_csv(output_file, index=False)
    
    print(f"Categories merged successfully. Output saved to {output_file}")


# 使用示例
if __name__ == "__main__":
    # input_file = '../../Data/navigation_category_rows.csv'  
    # output_file = '../../Data/merge_category.csv' 
    # input_file = './navigation_category_rows.csv'  
    # output_file = './merge_category.csv'  
    input_file = '../../Data/hulian.csv'
    output_file = '../../Data/hulian1.csv'
    # extract_categories_and_tags(input_file, output_file)
    deduplicate_csv(input_file, output_file)
    # merge_categories_by_code(
    #     input_file,
    #     output_file,
    #     '全球网络',  # code1
    #     '全球接码',  # code2
    #     '跨境服务'  # new_code
    # )