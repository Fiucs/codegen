#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :getTablesData_peewee.py
# @Time      :2025/06/22 13:21:23
# @Author    :Ficus

import re
import sqlite3
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase
from typing import Dict, List, Tuple, Optional

# 数据库连接测试,创建数据库
def test_db_connection():
    """
    测试SQLite数据库连接
    
    返回：
        bool: 连接是否成功
    """
    try:
        db = SqliteDatabase('db/codegen.db')
        db.connect()
        db.close()
        return True
    except Exception as e:
        print(f"连接异常：{str(e)}")
        return False

# 从 sqlite_master 获取表注释

def parse_sqlite_comments(create_sql: str) -> Dict[str, str]:
    """
    解析 SQLite 创建表的 SQL 语句，提取字段注释
    参数:
        create_sql: 创建表的 SQL 语句
    返回:
        字段名到注释的映射字典
    """
    comments = {}
    if not create_sql:
        return comments

    # 分割为每一行处理
    lines = create_sql.splitlines()
    
    # 字段行提取正则
    field_line_pattern = re.compile(r'^\s*"(?P<field>[^"]+)"\s+.*?(--(?P<comment>.*))?$')

    for line in lines:
        line = line.strip()
        if not line or line.lower().startswith("create table") or line.startswith(")"):
            continue
        
        match = field_line_pattern.match(line)
        if match:
            field_name = match.group("field").strip()
            comment = match.group("comment")
            if comment:
                comment = comment.strip().rstrip(",")  # 清理尾部逗号
                comments[field_name] = comment
                print(f"[解析] 字段: {field_name}, 注释: {comment}")

    return comments


def get_database_schema_with_comments(db_path: str):
    """获取 SQLite 数据库结构及注释信息"""
    db = SqliteDatabase(db_path)
    db.connect()
    
    # 获取所有表的创建SQL
    table_sqls = {}
    try:
        cursor = db.execute_sql("SELECT name, sql FROM sqlite_master WHERE type='table'")
        for row in cursor.fetchall():
            table_name = row[0]
            create_sql = row[1]
            table_sqls[table_name] = create_sql
    except Exception as e:
        print(f"获取表SQL失败: {e}")
    
    # 解析每个表的注释
    table_comments = {}
    for table_name, create_sql in table_sqls.items():
        if create_sql is None:
            print(f"\n警告: 表 '{table_name}' 没有创建SQL语句")
            continue
            
        print(f"\n{'='*50}")
        print(f"解析表: {table_name}")
        comments = parse_sqlite_comments(create_sql)
        table_comments[table_name] = comments
    
    db.close()
    return table_comments

# 读取数据库构造
def read_db_construct_01(db,includes_table_names:List[str],dbConfig:dict):
    """
    读取数据库构造
    参数:
        dbName: 数据库名
        table_names: 要解析的表名列表
    返回:
        数据库结构字典
    """

    # 获取db的名字
    db_name = db.database
    db_type = dbConfig.get("db_type")

    # 获取db的类型
    
    # 获取所有表名
    table_names = []
    database_schema={}
    try:
        table_names=[]
        if db_type == 'sqlite3':
            # 这是sqlite3中的
            cursor = db.execute_sql("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [row[0] for row in cursor.fetchall()]
                
            print(f"数据库 '{db_name}' 中共有 {len(table_names)} 个表")
            print(f"表名: {table_names}")
            database_schema=get_sqlite3_cols(table_names=table_names,db=db,includes_table_names=includes_table_names)
        elif db_type == 'mysql':
            # 这是mysql中的
            table_names = db.get_tables()
            #  TODO 遍历每张表获取结构 
            # 调用MySQL表结构获取函数
            database_schema = get_mysql_cols(table_names=table_names, db=db, 
                                            includes_table_names=includes_table_names, 
                                            db_name=db_name)      
    except Exception as e:
        print(f"获取表名失败: {e}")

    

    db.close()
    return database_schema


# 获取MySQL表结构（添加注释支持）
def get_mysql_cols(table_names: List[str], db, includes_table_names: List[str], db_name: str):
    import re
    database_schema = {}
    
    for table_name in table_names:
        if includes_table_names and includes_table_names != [] and table_name not in includes_table_names:
            continue
            
        columns = []
        primary_keys = []
        foreign_keys = []
        
        try:
            # 获取列信息（包含注释）
            col_query = f"""
                SELECT 
                    COLUMN_NAME, 
                    COLUMN_TYPE, 
                    IS_NULLABLE, 
                    COLUMN_DEFAULT, 
                    EXTRA, 
                    COLUMN_KEY,
                    COLUMN_COMMENT
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """
            cursor = db.execute_sql(col_query)
            
            for row in cursor.fetchall():
                col_name, col_type, is_nullable, col_default, extra, col_key, col_comment = row
                
                columns.append({
                    'name': col_name,
                    'type': col_type.upper(),
                    'nullable': is_nullable == 'YES',
                    'default': col_default,
                    'autoincrement': 'auto_increment' in extra.lower(),
                    'primary_key': col_key == 'PRI',
                    'comment': col_comment  # 添加注释信息
                })
                
                # 记录主键
                if col_key == 'PRI':
                    primary_keys.append(col_name)
                    
            # 获取外键信息
            fk_query = f"""
                SELECT 
                    COLUMN_NAME, 
                    REFERENCED_TABLE_NAME, 
                    REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = '{db_name}' 
                    AND TABLE_NAME = '{table_name}' 
                    AND REFERENCED_TABLE_NAME IS NOT NULL
            """
            cursor = db.execute_sql(fk_query)
            
            for row in cursor.fetchall():
                col_name, ref_table, ref_col = row
                foreign_keys.append({
                    'constrained_columns': [col_name],
                    'referred_table': ref_table,
                    'referred_columns': [ref_col]
                })
                
            # 尝试获取表注释
            try:
                cursor = db.execute_sql(f"""
                    SELECT TABLE_COMMENT 
                    FROM information_schema.TABLES 
                    WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{table_name}'
                """)
                table_comment = cursor.fetchone()[0]
                if table_comment:
                    # 将表注释添加到表信息中
                    if database_schema.get(table_name):
                        database_schema[table_name]['comment'] = table_comment
            except:
                pass
                
        except Exception as e:
            print(f"处理表 {table_name} 时出错: {e}")
            continue
            
        # 构建表结构信息
        table_info = {
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys
        }
        database_schema[table_name] = table_info
        
    return database_schema
# 获取sqlite3中表的数据结构
def get_sqlite3_cols(table_names:List[str],db,includes_table_names:List[str]):
        # 存储所有表结构的字典
    database_schema = {}
    
    # 遍历每个表，获取字段信息
    for table_name in table_names:
        # 如果table_names为空则解析所有，如果不为空则判断是否在table_names中
        if includes_table_names and includes_table_names != [] and table_name not in includes_table_names:
            continue

        # 获取列信息
        columns = []
        try:
            cursor = db.execute_sql(f"PRAGMA table_info({table_name})")
            # PRAGMA table_info结果: [cid, name, type, notnull, dflt_value, pk]
            for row in cursor.fetchall():
                cid, name, type_, notnull, dflt_value, pk = row
                # type转成大写
                type_ = type_.upper()
                columns.append({
                    'name': name,
                    'type': type_ ,  
                    'nullable': not notnull,
                    'default': dflt_value,
                    'autoincrement': (type_.upper() == 'INTEGER' and pk) or False,
                    'primary_key': pk == 1
                })
        except Exception as e:
            print(f"获取表{table_name}列信息失败: {e}")
            continue
        
        # 获取主键信息
        primary_keys = [col['name'] for col in columns if col['primary_key']]
        
        # 获取外键信息
        foreign_keys = []
        try:
            cursor = db.execute_sql(f"PRAGMA foreign_key_list({table_name})")
            # PRAGMA foreign_key_list结果: [id, seq, table, from, to, on_update, on_delete, match]
            for row in cursor.fetchall():
                fk_id, seq, ref_table, from_col, to_col, *_ = row
                foreign_keys.append({
                    'constrained_columns': [from_col],
                    'referred_table': ref_table,
                    'referred_columns': [to_col]
                })
        except Exception as e:
            print(f"获取表{table_name}外键信息失败: {e}")
        
        # 构建表结构信息
        table_info = {
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys
        }
        
        database_schema[table_name] = table_info
        
    return database_schema



# 读取数据库构造并特殊处理注释
def read_db_construct(dbConfig:dict,table_names:List[str]):
    """
    读取数据库构造
    参数:
        dbName: 数据库名
        dbType: 数据库类型
        table_names: 要解析的表名列表
    返回:
        数据库结构字典
    """
        # todo 区分不同的数据库类型并连接
    # sqlite3，mysql,postgresql
    dbType = dbConfig.get("db_type","")
    dbUrl = dbConfig.get("db_url","")
    db=None
    if dbType == 'sqlite3':
        db = SqliteDatabase(dbUrl)
        db.connect()
    elif dbType == 'mysql':
        db = MySQLDatabase(
                dbConfig.get("db_name"),  # 数据库名称
                user=dbConfig.get("db_user"),      # 数据库用户名
                password=dbConfig.get("db_password"), # 数据库密码
                host=dbConfig.get("db_url"), # 数据库主机地址
                port=dbConfig.get("db_port"),        # 数据库端口
                charset='utf8mb4',
                use_unicode=True
)       
        db.connect()

    elif dbType == 'postgresql':
        print('postgresql暂不支持')
    database_schema = read_db_construct_01(db,table_names,dbConfig)
    print(f'得到数据库{database_schema}的构造')
    # 如果是sqlite3则调用get_database_schema_with_comments获取注释
    if dbType == 'sqlite3':
        # 去掉数据库一些默认的表，后期可通过传入指定的表来解析
        exclude_tables = ['sqlite_sequence']
        for table_name in exclude_tables:
            if table_name in database_schema:
                del database_schema[table_name]

        database_schema_comments = get_database_schema_with_comments(dbUrl)
        # 遍历数据库结构，添加注释
        for table_name, table_info in database_schema.items():
            # 获取表的注释
            table_cols = database_schema_comments.get(table_name, {})
            # 遍历字段，添加注释
            for col in table_info['columns']:
                # 获取字段的注释
                col_comment = table_cols.get(col['name'], '无描述')
                # 添加注释
                col['comment'] = col_comment
    elif(dbType == 'mysql'):
        print('mysql暂不支持')
    elif(dbType == 'postgresql'):
        print('postgresql暂不支持')
    elif(dbType == 'oracle'):
        print('oracle暂不支持')
    elif(dbType == 'sqlserver'):
        print('sqlserver暂不支持')
    else:
        print('其他数据库类型暂不支持')

    return database_schema

if __name__ == "__main__":
    # 初始化db
    # test_db_connection()
    import orjson
    dbConfig={
        "db_type": "sqlite3",
        "db_name": "db/codegen.db"
    }
    database_schema = read_db_construct(dbConfig,[])
    # 转成json,使用orjson
    database_schema_json = orjson.dumps(database_schema, option=orjson.OPT_SERIALIZE_NUMPY).decode('utf-8')


    print(f'得到数据库的构造\n{database_schema_json}')


    for table_name, table_info in database_schema.items():
        print(f'-------------------------表名:{table_name}--------------------------')
        for col in table_info['columns']:
            print(f'字段名:{col["name"]},字段类型:{col["type"]},字段注释:{col["comment"]}')

        print(f'--------------------------------------------------------------------')