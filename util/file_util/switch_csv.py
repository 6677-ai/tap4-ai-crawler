# -*- coding: utf-8 -*-
import json
import csv

# 将爬取后的json文件转换为cvs((['category_name', 'tags', 'site', 'name']))文件
def switch_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['category_name', 'tags', 'site', 'name'])

        # 遍历 JSON 数据结构
        for category in json_data:
            category_name = category['name']
            for child in category['children']:
                # 将 tags 作为数组
                tags = [child['name']]
                for item in child['children']:
                    site = item['url']
                    name = item['name']
                    tags_str = str(tags)
                    writer.writerow([category_name, tags_str, site, name])

    print(f"成功将 {json_file} 数据转换到 {csv_file}")


if __name__ == '__main__':
    switch_csv("../crawler_util/crawler_vmlogin/data.json", ".website_data1.csv")
