import pandas as pd
import ast  # 用于处理字符串格式的列表


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

# 示例调用
# sort_by_category('./all_categories_and_tags.csv', './cate.csv')
# 示例调用
# process_website_data('../../Data/website_data_flag.csv', '../../Data/processed_website_data_flag.csv')