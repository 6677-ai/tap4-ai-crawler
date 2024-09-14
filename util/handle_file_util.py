import json
import csv

csv_file_path = '../Data/all_website_data.csv'
output_path = '../Data/website_data.csv'


# 处理csv文件数据
def read_site_data_file(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        csv_reader = csv.DictReader(file)

        # 设置输出文件的表头
        fieldnames = ['site', 'tags']  # 只包含 site 和 tags

        # 打开输出文件以写入数据
        with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()  # 写入表头

            for row in csv_reader:
                # 合并 page_type, page_location 和 page_usage
                page_type = json.loads(row.get('page_type', '[]'))
                page_location = json.loads(row.get('page_location', '[]'))
                page_usage = json.loads(row.get('page_usage', '[]'))

                # 合并并去重
                combined_array = list(set(page_type + page_location + page_usage))

                try:
                    details = json.loads(row['details'])
                    site = details.get('Site')

                    if site:
                        pass
                        csv_writer.writerow({
                            'site': site,
                            'tags': json.dumps(combined_array)  # 将 combined_array 转换为 JSON 字符串
                        })
                    else:
                        print("Site not found in details.")
                except json.JSONDecodeError:
                    print("Error decoding JSON from details:", row['details'])

if __name__ == '__main__':
    read_site_data_file(csv_file_path, output_path)
