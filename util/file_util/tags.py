import csv
import ast
from collections import defaultdict
def load_csv_data(file_path, is_all_categories=False):
    data = set()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['category_name']
            if is_all_categories:
                tags = ast.literal_eval(row['tags'])
                for tag in tags:
                    data.add((category, tag))
            else:
                code = row['code']
                data.add((category, code))
    return data

def compare_csv_files(current_file, all_file, output_file):
    current_data = load_csv_data(current_file)
    all_data = load_csv_data(all_file, is_all_categories=True)
    
    missing_data = all_data - current_data
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_csvfile:
        writer = csv.writer(out_csvfile)
        writer.writerow(['category_name', 'tags'])
        for category, tag in missing_data:
            writer.writerow([category, tag])

def group_by_category(input_file, output_file):
    # 使用 defaultdict 来存储分组数据
    grouped_data = defaultdict(list)

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['category_name']
            grouped_data[category].append(row)

    # 写入输出文件
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # 假设所有行都有相同的列
        fieldnames = list(next(iter(grouped_data.values()))[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for category, rows in grouped_data.items():
            for row in rows:
                writer.writerow(row)
            # 在每个类别之后添加一个空行，以便更容易区分
            writer.writerow({field: '' for field in fieldnames})

    print(f"分组后的数据已写入 {output_file}")

if __name__ == "__main__":
    # current_file = 'current_tags.csv'
    # all_file = 'all_categories_and_tags.csv'
    # output_file = 'missing_tags.csv'
    
    # compare_csv_files(current_file, all_file, output_file)
    # print(f"在 current_tags.csv 中缺失的内容已输出到 {output_file}")
    input_file = 'missing_tags.csv'
    output_file = 'grouped_categories_and_tags.csv'
    
    group_by_category(input_file, output_file)