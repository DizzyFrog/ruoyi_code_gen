from common.ai_chat import get_response_with_tongyi
from common.read_file import read_excel_to_dict


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

if __name__ == '__main__':
    data_dict = read_excel_to_dict()
    for item in data_dict[:4]:
        table_name = item['表号']
        table_desc = item['功能']
        sql = _gen_sql_create_table(table_name, table_desc)
        print(f"Table Name: {table_name}")
        print(f"SQL: {sql}")
        print("=" * 50)