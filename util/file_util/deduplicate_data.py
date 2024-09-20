import csv
from collections import defaultdict

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

if __name__ == "__main__":
    input_file = '../../Data/website_data.csv'  # 输入文件路径
    output_file = '../../Data/website_data_deduplicated.csv'  # 输出文件路径
    deduplicate_csv(input_file, output_file)