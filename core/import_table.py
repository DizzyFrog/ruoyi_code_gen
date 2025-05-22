from common.read_file import read_excel_to_dict
from config.api_config import API_URL, headers
import requests
import logging

logger = logging.getLogger(__name__)

def import_tables(tables: str) -> dict:
    """导入指定的表
    
    Args:
        tables (str): 要导入的表名，多个表用逗号分隔
        
    Returns:
        dict: 接口返回结果
    """
    

    
    # 设置请求参数
    params = {
        'tables': tables
    }
    
    try:
        response = requests.post(API_URL, headers=headers, params=params)  # 使用配置的 API_URL
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"导入表失败: {str(e)}")
        raise
    
if __name__ == '__main__':
    data_dict = read_excel_to_dict()
    table_names = ['table_'+str(item['表号']) for item in data_dict]
    result = import_tables(','.join(table_names))
    if result.get('code') == 0:
        logger.info("表导入成功")
        logger.info(f"返回消息: {result.get('msg')}")
    else:
        logger.error(f"表导入失败: {result.get('msg')}")
