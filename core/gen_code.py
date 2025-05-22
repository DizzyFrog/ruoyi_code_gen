import requests

from config.api_config import gen_code_url  # 假设API配置在这个文件中
from config.api_config import headers
from common.read_file import read_excel_to_dict
import logging

logger = logging.getLogger(__name__)

def generate_code(table_name: str) -> None:
    """发送生成代码的GET请求
    
    Args:
        table_name (str): 表名
    """
    url = gen_code_url + table_name
    
    try:
        # 使用ApiConfig中的headers发送请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        logger.info(f"成功为表 {table_name} 生成代码")
        logger.info(f"响应状态码: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"生成代码失败: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        data_dict = read_excel_to_dict()
        table_names = ["table_"+str(item['表号']) for item in data_dict]
        logger.info(f"table_names: {table_names}")
        for table_name in table_names:
            # print(table_name)
            generate_code(table_name)
    except Exception as e:
        logger.error(f"执行失败: {str(e)}")