import csv
import json

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

if __name__ == "__main__":
    input_file = '../../Data/website_data.csv'  # 输入文件路径
    output_file = '../../Data/unique_categories_and_tags.csv'  # 输出文件路径
    extract_categories_and_tags(input_file, output_file)