# 1. 执行gen_table.py

生成数据库文件ddl，并插入到mysql_config 配置的数据库

# 2. 执行 importTable.py

将上一步生成的多个表，导入 到数据库的gen_table

# 3.执行 modify_gen_table.py

实现的事修改代码生成路径，等各种配置，对每一个页面

# 4. 执行gen_code

该步骤会直接生成（前后端）代码到项目

# 5. 配置前端

菜单管理那里配置下路由，待优化，目前手动批量复制也很快（直接复制数据库的一列到另一列，用datagrip）
