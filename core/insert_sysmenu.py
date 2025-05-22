# 读取dict_data

from common.Sql_client import MySQLClient
from config.mysql_config import MySQLConfig
from common.read_file import read_excel_to_dict

'''
INSERT INTO ruoyi_yunnan2022.sys_menu (menu_id, menu_name, parent_id, order_num, url, target, menu_type, visible, is_refresh, perms, icon, create_by, create_time, update_by, update_time, remark) VALUES (2003, '日志留存数据上报基础配置信息维护', 2002, 1, '/bizmanage/Table1', 'menuItem', 'C', '0', '1', null, '#', 'admin', '2025-05-21 11:29:04', '', null, '');
'''
def _update_sysmenu():
    db_config = MySQLConfig.get_config()
    data_dict = read_excel_to_dict()
    client = MySQLClient(**db_config)
    for item in data_dict:
        index = (item['表号'])
        table_name = 'table_'+str(index)
        class_name = 'Table'+str(index)
        table_desc = item['功能']
        sql = f"INSERT INTO ruoyi_yunnan2022.sys_menu ( menu_name, parent_id, order_num, url, target, menu_type, visible, is_refresh, perms, icon, create_by, create_time, update_by, update_time, remark) VALUES ( '{table_desc}', 2002, {index}, '/bizmanage/{class_name}', 'menuItem', 'C', '0', '1', null, '#', 'admin', '2025-05-21 11:29:04', '', null, '');"
        print(sql)
        client.execute_query(sql)

if __name__ == '__main__':
    _update_sysmenu()
