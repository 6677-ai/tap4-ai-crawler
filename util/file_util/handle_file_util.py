import json
import csv
import pandas as pd
import os
csv_file_path = '../Data/all_website_data.csv'
output_path = '../Data/website_data.csv'


def process_website_data(input_file, output_file):
    """
    处理网站数据，新增列并调整列的顺序。

    :param input_file: 原始 CSV 文件路径
    :param output_file: 处理后的 CSV 文件路径
    """
    # 读取原始 CSV 文件
    df = pd.read_csv(input_file)

    # 新增 name 列，内容取自 site 列
    df['name'] = df['site']

    # 新增 category_name 列并设置为 'proxy'
    df['category_name'] = 'proxy'

    # 调整列的顺序
    df = df[['category_name', 'tags', 'site', 'name']]

    # 保存到一个新的 CSV 文件
    df.to_csv(output_file, index=False)

    print("数据处理完成，文件已保存到：", output_file)

def sort_by_category(input_file, output_file):
    """
    将相同 category_name 的行放在一起，并重新排序。

    :param input_file: 原始 CSV 文件路径
    :param output_file: 排序后的 CSV 文件路径
    """
    # 读取原始 CSV 文件
    df = pd.read_csv(input_file)

    # 根据 category_name 对 DataFrame 排序
    df_sorted = df.sort_values(by='category_name')

    # 保存排序后的结果到新的 CSV 文件
    df_sorted.to_csv(output_file, index=False)

    print("排序成功！文件已保存到：", output_file)

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
                            'tags': json.dumps(combined_array)
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
