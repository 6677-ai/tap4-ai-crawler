import json
import csv
import pandas as pd
import os
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

def handle_submit_data(input_file_path, output_file_path):
    """
    处理submit文件里面的数据为爬虫标准输入数据。默认的标签为AI工具/AI常用工具
    
    :param input_file_path: 输入 CSV 文件的路径
    :param output_file_path: 输出 CSV 文件的路径
    """
    df = pd.read_csv(input_file_path)

    result = df[['name', 'url']].copy()  

 
    result.rename(columns={'url': 'site'}, inplace=True)

    result['category_name'] = 'AI工具'
    result['tags'] = "['AI常用工具']"
    result = result[['category_name', 'tags', 'site','name']]
    if os.path.exists(output_file_path):
        with open(output_file_path, 'a') as f:
            f.write('\n')  # 添加换行符
    result.to_csv(output_file_path, mode='a', header=False, index=False)
    print("INFO: 文件成功写入")

# 使用示例
if __name__ == '__main__':
    handle_submit_data('../../Data/submit.csv', '../../Data/hulian.csv')
    # read_site_data_file(csv_file_path, output_path)
    
