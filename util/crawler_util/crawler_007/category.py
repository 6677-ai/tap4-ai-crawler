import csv
from collections import OrderedDict
from collections import defaultdict
def extract_unique_categories(input_file, output_file):
    unique_categories = OrderedDict()
    
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['category_name'].strip('"')
            if category not in unique_categories:
                unique_categories[category] = len(unique_categories) + 1

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'category_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for category, id in unique_categories.items():
            writer.writerow({'id': id, 'category_name': category})

    print(f"已提取 {len(unique_categories)} 个唯一类别并保存到 {output_file}")



def load_csv_data(file_path, key_column, value_column):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row[key_column].strip('"')
            value = row[value_column].strip('"')
            data[key] = value
    return data

def compare_categories(dangqian_file, categories_file):
    dangqian_data = load_csv_data(dangqian_file, 'code', 'name_cn')
    categories_data = load_csv_data(categories_file, 'category_name', 'category_name')

    matching = []
    only_in_dangqian = []
    only_in_categories = []

    for code, name in dangqian_data.items():
        if code in categories_data:
            matching.append(code)
        else:
            only_in_dangqian.append(code)

    for category in categories_data:
        if category not in dangqian_data:
            only_in_categories.append(category)

    print("匹配的类别:")
    for item in matching:
        print(f"  - {item}")

    print("\n仅在 dangqian.csv 中出现的类别:")
    for item in only_in_dangqian:
        print(f"  - {item}")

    print("\n仅在 categories.csv 中出现的类别:")
    for item in only_in_categories:
        print(f"  - {item}")

    print(f"\n总结:")
    print(f"  匹配的类别数: {len(matching)}")
    print(f"  仅在 dangqian.csv 中的类别数: {len(only_in_dangqian)}")
    print(f"  仅在 categories.csv 中的类别数: {len(only_in_categories)}")

# # 使用脚本
dangqian_file = './database.csv'
categories_file = './categories.csv'
compare_categories(dangqian_file, categories_file)



# input_file = './tag_data.csv'
# input_file = '../../../Data/website_data.csv'
# output_file = 'categories.csv'
# extract_unique_categories(input_file, output_file)