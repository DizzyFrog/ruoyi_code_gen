import pymysql


class MySQLClient:
    def __init__(self, host, user, password, database):
        """
        初始化 MySQL 客户端
        """
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=False  # 关闭自动提交，启用事务
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        """
        执行单个 SQL 语句
        """
        try:
            self.cursor.execute(query, params)
            self.connection.commit()  # 提交事务
        except pymysql.MySQLError as e:
            print(f"执行 SQL 出错: {e}")
            self.connection.rollback()
            raise

    def execute_transaction(self, queries_with_params):
        """
        执行一组 SQL 语句作为一个事务
        :param queries_with_params: 包含 (query, params) 的列表
        """
        try:
            for query, params in queries_with_params:
                self.cursor.execute(query, params)
            self.connection.commit()
            print("事务提交成功")
        except pymysql.MySQLError as e:
            print(f"事务出错: {e}")
            self.connection.rollback()
            print("事务已回滚")
            raise

    def close(self):
        """
        关闭连接
        """
        self.cursor.close()
        self.connection.close()


# 示例使用
if __name__ == "__main__":
    # 数据库配置
    db_config = {
        "host": "10.28.190.206",
        "user": "root",
        "password": "root",
        "database": "my_database",
    }

    # 初始化客户端
    client = MySQLClient(**db_config)

    try:
        # 创建表语句
        create_table_1 = "CREATE TABLE IF NOT EXISTS table1 (id INT PRIMARY KEY, value VARCHAR(50))"
        client.execute_query(create_table_1)
        insert = "INSERT INTO table1 (id, value) VALUES (%s, %s)"
        client.execute_transaction([
            (insert, (1, "Value1")),
            (insert, (2, "Value2")),
            (insert, (3, "Value3"))
        ])

    except Exception as e:
        print(f"程序运行出错: {e}")

    finally:
        # 关闭连接
        client.close()