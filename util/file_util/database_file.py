# 处理supabsae数据库中的数据
import pandas as pd
import os
import re
import csv
def clean_data(row):
    """清理数据，去掉 category_name 和 tag_name 字段外面的双引号"""
    row['category_name'] = row['category_name'].strip('[]"')
    row['tag_name'] = row['tag_name'].str.replace('^"|"$', '', regex=True)
    return row

def save_errors(df, column, error_file):
    """保存包含 null 值的错误数据"""
    if df[column].isnull().any():
        error_data = df[df[column].isnull()][['category_name', 'tag_name', 'url']]
        error_data = error_data.apply(lambda x: clean_data(x), axis=1)
        # 保存错误数据到 CSV 文件
        error_data.to_csv(error_file, index=False, header=not os.path.exists(error_file) or os.path.getsize(error_file) == 0)
        print(f"发现 {column} 列的 null 值，错误数据已输出到 {error_file}")

def append_unique_errors(df, column, condition, error_file, exclude_files=None):
    """检查条件并将错误数据追加到错误文件中，避免重复"""
    error_check = df[condition]
    
    if not error_check.empty:
        existing_errors = pd.DataFrame()
        if os.path.exists(error_file) and os.path.getsize(error_file) > 0:
            existing_errors = pd.read_csv(error_file)
        
        # 排除文件处理
        if exclude_files:
            for exclude_file in exclude_files:
                if os.path.exists(exclude_file):
                    exclude_errors = pd.read_csv(exclude_file)
                    error_check = error_check[~error_check.isin(exclude_errors).all(axis=1)]
        
        # 过滤重复错误
        unique_errors = error_check[~error_check.isin(existing_errors).all(axis=1)]
        
        if not unique_errors.empty:
            unique_errors = unique_errors[['category_name', 'tag_name', 'url',]]
            unique_errors = unique_errors.apply(lambda x: clean_data(x), axis=1)
            print(f"准备将 {len(unique_errors)} 条错误数据追加到 {error_file}...")
            try:
                unique_errors.to_csv(error_file, mode='a', index=False, header=not os.path.exists(error_file) or os.path.getsize(error_file) == 0)
                print(f"{len(unique_errors)} 条数据已成功追加到 {error_file}.")
            except Exception as e:
                print(f"写入 {error_file} 时出错: {e}")

def check_website_navigation(file_path):
    """
    检查数据库文件内容

    :param file_path: 数据库导出文件 web_navigation_rows.csv
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return

    # 检查 null 值
    null_checks = {
        'title_cn': './Data/title_errors.csv',
        'detail_en': './Data/detail_errors.csv',
        'website_data_en': './Data/website_data_errors.csv'
    }
    
    for column, error_file in null_checks.items():
        save_errors(df, column, error_file)

    # 检查 title_cn 中是否包含 "404"（排除 "Cloudflare"）
    title_cn_condition = (
        ~df['title_cn'].str.contains("Cloudflare", na=False) & 
        (df['title_cn'].str.contains("404", na=False) |
         df['title_cn'].str.contains("页面未找到", na=False) |
         df['title_cn'].str.contains("找不到内容", na=False) |
         df['title_cn'].str.contains("更新浏览器", na=False) |
         df['title_cn'].str.contains("IP 访问被拒绝", na=False) |
         df['title_cn'].str.contains("请稍等...", na=False) |
         df['title_cn'].str.contains("403 禁止访问", na=False))
    )
    append_unique_errors(df, 'title_cn', title_cn_condition, './Data/title_errors.csv', 
                         ['./Data/detail_errors.csv', './Data/website_data_errors.csv'])

    # 检查 detail_en 是否以 "### What is tap4.ai?" 开头
    detail_en_condition = df['detail_en'].str.startswith("### What is tap4.ai?", na=False)
    append_unique_errors(df, 'detail_en', detail_en_condition, './Data/detail_errors.csv', 
                         ['./Data/title_errors.csv', './Data/website_data_errors.csv'])

    # 检查 website_data_en 是否以 "```markdown" 开头
    website_data_en_condition = df['website_data_en'].str.startswith("```markdown", na=False)
    append_unique_errors(df, 'website_data_en', website_data_en_condition, './Data/website_data_errors.csv', 
                         ['./Data/title_errors.csv', './Data/detail_errors.csv'])

    print("检查完成，错误数据已输出到相应的文件。")

def add_quotation(origin_file, quotation_file, columns):
    """
    为指定列的值添加双引号并将结果写入新的 CSV 文件。

    :param origin_file: 输入 CSV 文件路径
    :param quotation_file: 输出 CSV 文件路径
    :param columns: 需要添加双引号的列名称列表
    """
    with open(origin_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = []
        for row in reader:
            for col in columns:
                if col in row:  
                    row[col] = f'"{row[col]}"' 
            rows.append(row)

    # 将修改后的数据写入新的 CSV 文件
    with open(quotation_file, mode='w', encoding='utf-8', newline='') as outfile:
        fieldnames = reader.fieldnames  # 获取列名称
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(rows)
    print('添加双引号成功！')


def reset_id_column(input_csv_file_path, output_csv_file_path):
    """
    重置id
    """
    df = pd.read_csv(input_csv_file_path)
    start_num = 1

    df['id'] = range(start_num, len(df) + start_num)

    df.to_csv(output_csv_file_path, index=False)
    print('重置id成功！')
    # columns = ['code', 'category_name']
    # add_quotation(input_csv_file_path, output_csv_file_path, columns)


def remove_rows_by_id(file_path, start, end, output_path, save_mode=False):
    """
    删除CSV文件中ID在start到end范围内的行，并保存到新的CSV文件。

    :param file_path: CSV文件路径
    :param start: 要删除的起始ID（包含）
    :param end: 要删除的结束ID（不包含）
    :param output_path: 新的CSV文件路径
    :raises ValueError: 如果start或end不合法
    :raises FileNotFoundError: 如果文件不存在
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if df.empty:
        print("DataFrame is empty.")
        return


    if save_mode:
        # 保存指定范围内的行
        df = df[df['id'].between(start, end)]
    else:
        # 删除指定范围内的行
        df = df[~df['id'].between(start, end)]

    # 保存到新的CSV文件
    df.to_csv(output_path, index=False)
    action = "保存" if save_mode else "删除"
    print(f"成功{action}从 {start} 到 {end} 的数据，保存至 {output_path}.")


if __name__ == '__main__':
    input_path = "./Data/web_navigation_rows.csv"
    output_path = "./Data/web_navigation_rowsresetid.csv"
    # remove_rows_by_id('./Data/cate.csv', 1, 300, './Data/delete_modified_file.csv')
    remove_rows_by_id('./Data/cate.csv', 901, 1192, './Data/saved_file.csv', save_mode=True)

    # reset_id_column(input_path, output_path)
    # add_quotation(
    #     './Data/navigation_tag_rows_resetid.csv',
    #     './Data/navigation_tag_rows_resetid_updated.csv',
    #     ['code', 'category_name']  
    # )
