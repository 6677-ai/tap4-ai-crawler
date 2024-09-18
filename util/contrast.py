import pandas as pd

def contras_data(ori_file, db_file):
    # 读取第一个 CSV 文件
    site_df = pd.read_csv(ori_file)

    # 读取第二个 CSV 文件
    url_df = pd.read_csv(db_file)

    # 为site加上 “https://”，并去除末尾斜杠
    site_df['site'] = 'https://' + site_df['site'].str.strip().str.rstrip('/')
    url_df['url'] = url_df['url'].str.strip().str.rstrip('/')

    # 找出第一个文件独有的 URL
    unique_in_site = site_df[~site_df['site'].isin(url_df['url'])]

    # 找出第二个文件独有的 URL
    unique_in_url = url_df[~url_df['url'].isin(site_df['site'])]

    # 为每个表添加标记列，标记来源
    unique_in_site['source'] = 'unique_in_site'
    unique_in_url['source'] = 'unique_in_url'

    # 合并结果用于对比展示
    comparison_df = pd.concat([unique_in_site, unique_in_url], ignore_index=True)

    # 选择并规范化展示列
    if 'site' in comparison_df.columns:
        comparison_df = comparison_df[['url', 'source', 'site']]
    else:
        comparison_df = comparison_df[['url', 'source']]

    return comparison_df

# 调用函数
comparison_result = contras_data('../Data/website_data.csv', '../Data/DB/web_navigation9.18.csv')

# 打印对比结果
print(comparison_result)