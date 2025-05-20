from common.ai_chat import get_response_with_tongyi
from common.read_file import read_excel_to_dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


def _gen_sql_create_table(table_name, table_desc):
    """
    生成创建表的SQL语句
    """
    prompt = f"""
    请根据以下表描述生成创建表的MYSQL DDL语句：
    {table_desc}
    表名：table_{table_name}
    rules:
    1.使用 CREATE TABLE IF NOT EXISTS 语法
    2.为表和字段添加有意义的中文注释（最多四个汉字）
    3.包含大约 12 个字段
    4.必须包含主键 id 字段，且为自增
    5.除主键 id 和日期字段外，所有字段使用 VARCHAR(255) 类型
    6.最多包含 3 个与时间相关的字段，日期字段使用 DATETIME 类型
    7.只返回 SQL 语句，不添加任何额外文本
    """
    response = get_response_with_tongyi(prompt)
    return response


def process_table(item):
    """处理单个表的生成任务"""
    table_name = item['表号']
    table_desc = item['功能']
    try:
        sql = _gen_sql_create_table(table_name, table_desc)
        return {
            'table_name': table_name,
            'sql': sql,
            'success': True
        }
    except Exception as e:
        logging.error(f"生成表 {table_name} 的SQL时出错: {str(e)}")
        return {
            'table_name': table_name,
            'error': str(e),
            'success': False
        }


if __name__ == '__main__':
    # 配置日志
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    data_dict = read_excel_to_dict()
    items_to_process = data_dict[:4]

    # 创建线程池，最大工作线程数设为4（可根据需要调整）
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有任务到线程池
        future_to_item = {executor.submit(process_table, item): item for item in items_to_process}

        # 处理完成的任务结果
        for future in as_completed(future_to_item):
            result = future.result()
            if result['success']:
                print(f"Table Name: {result['table_name']}")
                print(f"SQL: {result['sql']}")
                print("=" * 50)
            else:
                print(f"生成表 {result['table_name']} 的SQL失败: {result['error']}")
                print("-" * 50)