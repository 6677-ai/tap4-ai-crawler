# 修改各个表中的code
import pandas as pd
from database_file import add_quotation
def modify_csv_column(input_file, output_file, target_column, source_column):
    """
    修改列的字段

    Parameters:
    - input_file (str): 输入文件
    - output_file (str): 修改后的输出文件
    - target_column (str): 需要修改的字段
    - source_column (str): 参照的字段
    """
    df = pd.read_csv(input_file)

    df[target_column] = df[source_column].str.lower()
    df.to_csv(output_file, index=False)
    
    print("修改成功")
    columns = ['code', 'category_name']
    # add_quotation(input_csv_file_path, output_csv_file_path, columns)
    add_quotation(output_file, output_file, columns)
    


modify_csv_column('./Data/navigation_category_rows.csv', './Data/navigation_category_modify_code.csv', 'code', 'name_en')