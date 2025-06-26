from peewee import MySQLDatabase, SqliteDatabase
import os
import yaml

from {{appName}}.context import MyContext


# 初始化db
def init_db():
    
    base_dir = MyContext.BASE_DIR
    config_file_path = MyContext.CONFIG_FILE_PATH
    db=None
    print(f'init_db BASE_DIR:{base_dir}')
    print(f'init_db CONFIG_FILE_PATH:{config_file_path}')

    
    # DB_PATH = os.path.join(BASE_DIR, 'apidemo/db', 'demo.db')
    # 从application.yaml中读取数据库信息，判断 可sqlite3,mysql等数据库，然后进行连接
    # 读取application.yaml文件
    
    with open(config_file_path, 'r', encoding='utf-8') as file: 
        config = yaml.safe_load(file)
    # 获取数据库配置
    db_config = config['datasource']
    # 判断数据库类型
    if db_config['database'] == 'sqlite3':
        # 连接sqlite数据库
        db_path = db_config['url']
        #  判断是否是绝对路径
        if not os.path.isabs(db_path):
            # 如果不是绝对路径，转换为相对于项目根目录的路径
            db_path = os.path.join(base_dir, db_path)

            # 确保db目录存在
            # os.makedirs(os.path.dirname(db_path), exist_ok=True)
        else:
            # 如果是绝对路径，确保目录存在
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # 连接sqlite数据库
        db = SqliteDatabase(db_path, timeout=30)


    elif db_config['database'] == 'mysql':
        # 连接mysql数据库
        db = MySQLDatabase(db_config['url'], user=db_config['username'], password=db_config['password'], timeout=30)
    else:
        raise ValueError("Unsupported database type in application.yaml")
    
    return db


# 初始化数据库
db = init_db()
