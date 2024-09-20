import json
import csv

def json_to_csv(json_file, csv_file):
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 准备CSV文件
    with open(csv_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        # 写入CSV头部
        writer.writerow(['id', 'code', 'name_en', 'name_cn', 'category_name', 'name_de', 'name_es', 'name_fr', 'name_jp', 'name_pt', 'name_ru', 'name_tw'])

        # 遍历JSON数据并写入CSV
        for category in data:
            category_name = category['name']
            for child in category['children']:
                writer.writerow([
                    '',  # id 留空
                    child['name'],  # code 使用 name_en 的值
                    child['name'],  # name_en
                    '',  # name_cn 留空
                    category_name,  # category_name
                    '', '', '', '', '', '', ''  # 其他语言暂时留空
                ])

    print(f"数据已成功转换并保存到 {csv_file}")

if __name__ == "__main__":
    json_file = 'data_007.json'  # JSON文件路径
    csv_file = 'tag_data.csv.csv'    # 输出的CSV文件路径
    json_to_csv(json_file, csv_file)