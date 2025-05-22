class MySQLConfig:
    """MySQL数据库配置类"""
    HOST = '10.28.148.200'
    USER = 'cosmic'
    PASSWORD = 'Asiainfo1234%'
    DATABASE = 'ruoyi_yunnan2022'

    @classmethod
    def get_config(cls) -> dict:
        """获取数据库配置字典
        
        Returns:
            dict: 数据库配置信息
        """
        return {
            'host': cls.HOST,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE
        }