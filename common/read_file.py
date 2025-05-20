# 读取 data/input/functions.xlsx 并封装为字典
import pandas as pd
from pathlib import Path
def read_excel_to_dict():
    """
    读取Excel文件并转换为字典格式，只读取'表号'和'功能'两列
    :return: 包含Excel数据的字典
    """

    excel_file = Path('data/input/functions.xlsx')
    
    df = pd.read_excel(excel_file, usecols=['表号', '功能'])
    # 将DataFrame转换为字典
    data_dict = df.to_dict('records')
    
    return data_dict


if __name__ == '__main__':
    data_dict = read_excel_to_dict()
    for item in data_dict:
        print(item)
    
