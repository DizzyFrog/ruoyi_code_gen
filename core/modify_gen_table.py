from common.Sql_client import MySQLClient
from config.mysql_config import MySQLConfig  # 导入数据库配置

def update_gen_table_path():
    # 数据库配置
    db_config = MySQLConfig.get_config()  # 使用 MySQLConfig 获取数据库配置

    # 初始化客户端
    client = MySQLClient(**db_config)

    try:
        # 更新 gen_table 表中的 gen_path 字段
        
        update_query = """
        UPDATE gen_table 
        SET gen_path = '/Users/robben/Desktop/0521/ruoyi_code_gen_parent4.7.9/ruoyi-admin/src',
            options = '{"parentMenuId":"2000","treeName":"","treeParentCode":"","parentMenuName":"业务接口","treeCode":""}',
            gen_type = '1',
            form_col_num = '1',
            function_author = 'robben',
            business_name = class_name,
            package_name = CONCAT('com.ruoyi.project.bizmanage.', class_name),
            module_name = 'bizmanage'
            
        """
        client.execute_query(update_query)
        print("所有行的 gen_path 已更新")
    except Exception as e:
        print(f"更新出错: {e}")
    finally:
        # 关闭连接
        client.close()
        

if __name__ == "__main__":
    update_gen_table_path() 