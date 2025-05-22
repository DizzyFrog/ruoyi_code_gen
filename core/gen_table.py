from common.ai_chat import get_response_with_tongyi
from common.read_file import read_excel_to_dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
from functools import partial
import logging
from typing import List, Tuple, Dict

def retry_on_error(func, max_retries=3, delay=2):
    """
    装饰器：处理重试逻辑
    
    Args:
        func: 要重试的函数
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    raise e
                logging.warning(f"第{attempt + 1}次尝试失败: {str(e)}, {delay}秒后重试...")
                time.sleep(delay)
        return None
    return wrapper

@retry_on_error
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
    3.包含大约 10 个以上与功能相关且有意义的字段
    4.必须包含主键 id 字段，且为自增
    5.除主键 id 和日期字段外，所有字段使用 VARCHAR(255) 类型
    6.最多包含 3 个与时间相关的字段，日期字段使用 DATETIME 类型
    7.只返回 SQL 语句，不添加任何额外文本
    """
    response = get_response_with_tongyi(prompt)
    return table_name, table_desc, response

def process_single_table(item, index):
    """
    处理单个表的生成
    
    Args:
        item: 表数据
        index: 原始顺序索引
    """
    table_name = item['表号']
    table_desc = item['功能']
    return index, _gen_sql_create_table(table_name, table_desc)

def gen_sql_to_file(data_dict, file_path, max_workers=5) -> Tuple[List[Dict], List[Dict]]:
    """
    将生成的 SQL 语句写入文件，使用多线程处理
    
    Args:
        data_dict: 数据字典
        file_path: 输出文件路径
        max_workers: 最大线程数，默认为5
        
    Returns:
        Tuple[List[Dict], List[Dict]]: 返回成功和失败的表列表
    """
    results = []
    failed_tables = []
    success_tables = []
    
    # 使用进度条显示处理进度
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务，并记录原始索引
        future_to_item = {
            executor.submit(process_single_table, item, idx): (idx, item) 
            for idx, item in enumerate(data_dict)
        }
        
        # 使用tqdm显示进度
        with tqdm(total=len(data_dict), desc="生成SQL") as pbar:
            for future in as_completed(future_to_item):
                idx, item = future_to_item[future]
                try:
                    idx, (table_name, table_desc, sql) = future.result()
                    results.append((idx, table_name, table_desc, sql))
                    success_tables.append(item)
                except Exception as e:
                    error_msg = f"处理表 {item['表号']} 时发生错误: {e}"
                    logging.error(error_msg)
                    failed_tables.append(item)
                pbar.update(1)
    
    # 按原始索引排序结果
    results.sort(key=lambda x: x[0])
    
    # 写入文件
    with open(file_path, 'w') as f:
        for _, table_name, table_desc, sql in results:
            sql = sql.replace("```sql", "").replace("```", "")
            f.write(f"# Table Name: {table_name}\n")
            f.write(f"# Table Description: {table_desc}\n")
            f.write(f"{sql}\n")
            f.write("-" * 50 + "\n")
    
    return success_tables, failed_tables

if __name__ == '__main__':
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    data_dict = read_excel_to_dict()
    sql_file_path = 'data/output/sql_statements.sql'
    # 可以根据实际情况调整线程数
    success_tables, failed_tables = gen_sql_to_file(data_dict, sql_file_path, max_workers=8)
    
    # 输出统计信息
    total_tables = len(data_dict)
    success_count = len(success_tables)
    failed_count = len(failed_tables)
    
    logging.info(f"\n处理完成统计信息:")
    logging.info(f"总表数: {total_tables}")
    logging.info(f"成功数: {success_count}")
    logging.info(f"失败数: {failed_count}")
    
    if failed_tables:
        logging.error("\n以下表生成失败:")
        for table in failed_tables:
            logging.error(f"表号: {table['表号']}, 功能: {table['功能']}")
    
    print(f"\nSQL statements generated and saved to {sql_file_path}")