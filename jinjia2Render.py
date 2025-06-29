#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import shutil
import uuid
from jinja2 import Environment, FileSystemLoader, select_autoescape



# —— 1. 你的元数据字典 —— #
metadata = {
        "department": {
            "columns": [
                {
                    "name": "id",
                    "type": "INTEGER",
                    "nullable": False,
                    "default": None,
                    "autoincrement": False,
                    "comment": "部门ID",
                    "primary_key": True
                },
                {
                    "name": "dept_name",
                    "type": "TEXT",
                    "nullable": False,
                    "default": None,
                    "autoincrement": False,
                    "comment": "部门名称",
                    "primary_key": False
                },
                {
                    "name": "dept_code",
                    "type": "TEXT",
                    "nullable": True,
                    "default": None,
                    "autoincrement": False,
                    "comment": "部门代码",
                    "primary_key": False
                },
                {
                    "name": "create_time",
                    "type": "TEXT",
                    "nullable": True,
                    "default": "datetime('now','localtime')",
                    "autoincrement": False,
                    "comment": "创建时间",
                    "primary_key": False
                }
            ],
            "primary_keys": ["id"],
            "foreign_keys": []
        }
        # …可以继续加更多表…
}

# —— 2. 类型映射 —— #
type_map = {
    "sqlite3":{
        # AutoField
        "INTEGER": ("IntegerField"  , "int"),
        "INT":     ("IntegerField", "int"),
        "TEXT":    ("TextField"   , "str"),
        "BLOB":    ("BlobField"   , "bytes"),
        "REAL":    ("FloatField"  , "float"),
    },
        # 其他 SQL 类型可按需补充
     "mysql":{
        "INTEGER": ("IntegerField"  , "int"),
        "INT":     ("IntegerField", "int"),
        "VARCHAR": ("CharField"   , "str"),
        "TEXT":    ("TextField"   , "str"),
        "ENUM":    ("CharField"   , "str"),
        "DATE":    ("DateField"   , "datetime.date"),
        "DATETIME":("DateTimeField", "datetime.datetime"),
        "TIMESTAMP":("TimestampField", "datetime.datetime"),
        "DECIMAL": ("DecimalField", "Decimal"),
        "FLOAT":   ("FloatField"  , "float"),
        "DOUBLE":  ("DoubleField" , "float"),
        "TINYINT": ("IntegerField", "int"),
        "JSON":    ("TextField"   , "str"),
        "BLOB":    ("BlobField"   , "bytes"),
        "BIGINT":  ("BigIntegerField", "int"),
        "CHAR":    ("CharField"   , "str"),
        # 其他类型待补充....-


     },
    
}


# 生成model代码
def handleModel(table_name:str,info:dict,base_out_dir:str,template,app_name:str,db_config:dict):

        db_type=db_config.get("db_type","")
        # 将表面转化为驼峰命名的类名，首字母小写，拼接上Model
        class_name = ''.join([i.capitalize() for i in table_name.split('_')])
        class_name = class_name[0].lower() + class_name[1:] + "Model"
        pk_col = info["primary_keys"][0] if info["primary_keys"] else info["columns"][0]["name"]
        # 取第一个非PK的文本列作为 __str__ 用的字段
        str_col = next((c["name"] for c in info["columns"] if c["type"].startswith("TEXT") and not c["primary_key"]), pk_col)

        cols = []
        for col in info["columns"]:
            name_lower = col["name"].lower()
            sql_type = col["type"].upper()
            # 优先根据字段名判断 DateField
            if "date" in name_lower or "time" in name_lower:
                field_type, py_type = "DateField", "datetime.date"
            #判断是自增主键就是用AutoField
            elif col["autoincrement"]:
                field_type, py_type = "AutoField", "int"
            else:
                
                # 注意可能存在integer(10)的情况需要截取，并转为大写
                if "(" in sql_type:
                    sql_type = sql_type.split("(")[0]
                    sql_type = sql_type.upper()
                field_type, py_type = type_map.get(db_type,{}).get(sql_type, ("CharField", "str"))
                # 根据类型
            # sql_type = col["type"].upper()
            # field_type, py_type = type_map.get(sql_type, ("CharField", "str"))

            params = []
            if col.get("primary_key", False):
                params.append("primary_key=True")
            else:
                if not col.get("nullable", True):
                    params.append("null=False")
                else:
                    params.append("null=True")

             # 默认值：对 DateField 使用 datetime.datetime.now()
            # 对 DateField 强制添加 formats 参数
            if field_type == "DateField":
                # 默认值处理：DateField 一律用 datetime.datetime.now()（若有默认）
                if col.get("default") is not None:
                    params.append("default=datetime.datetime.now()")
                # 无论是否有 default，都补充 formats
                params.append("formats='%Y-%m-%d'")
            elif field_type in ["CharField","TextField"]:
                # 对于 CHAR 类型，补充 max_length
                defaultValue=col.get("default","")
                if defaultValue: 
                    params.append(f'''default="{defaultValue}"''')
                else:
                    params.append(f'''default={defaultValue}''')
    
            else:
                # 非 DateField 的默认值，保持原元数据
                if col.get("default") is not None:
                    params.append(f"default={col['default']}")    

            # 添加注释作为 verbose_name
            # 默认值是''
            comment = col.get("comment","")
            if comment:
                params.append(f"verbose_name='{comment}'")
            cols.append({
                "name": col["name"],
                "field_type": field_type,
                "params": ", ".join(params),
                "py_type": py_type,
                # Schema 默认值
                "default": "None" if col.get("nullable", True) else "None",
                "comment": comment,
            })

        # 处理索引元组，示例里只简单把主键做索引
        indexes = [f"('{pk_col}',), True"]

        ctx = {
            "table_name": table_name,
            "class_name": class_name,
            "model_name":   class_name[0].upper() + class_name[1:],  #class_name的首字母大小
            "model_schema_name":  f'{class_name}Schema',  #class_name+"Schema"
            "pk_col": pk_col,
            "str_col": str_col,
            "columns": cols,
            "indexes": indexes,
            "appName":app_name,
            
        }

        rendered = template.render(**ctx)
        write_to_file(base_out_dir,"model",f"{class_name}.py",rendered)
        # 返回解析出来的每个表的上下文
        return ctx



# 生成代码
def generate_code(ge_config,db_config:dict={}):
    
    base_project_path=ge_config["base_app_path"]
    app_name=ge_config["app_name"]
    includes_table_names=ge_config["includes_table_names"]
    
    # 1.初始化metadata
    import orjson
    # from getTablesData import read_db_construct
    from getTablesData_peewee import read_db_construct
    database_schema = read_db_construct(db_config,includes_table_names)
    # 转成json,使用orjson
    metadata = database_schema


    # —— 3. 初始化 Jinja2 环境 —— #
    env = Environment(
        loader=FileSystemLoader(searchpath="./template"),
        autoescape=select_autoescape([]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    modelTemplate = env.get_template("modelTemplate.tpl")
    serviceTemplate = env.get_template("serviceTemplate.tpl")
    controllerTemplate = env.get_template("controllerTemplate.tpl")
    mapperTemplate = env.get_template("mapperTemplate.tpl")
    controllerNameList=[]
    # 定义基本上下文

    # —— 4. 逐表渲染 —— #
    for table_name, info in metadata.items():
        # model生成
        modelCtx=handleModel(table_name,info,base_project_path,modelTemplate,app_name,db_config)    


        # mapper生成
        mapper_class_name = ''.join([i.capitalize() for i in table_name.split('_')])
        mapper_class_name = mapper_class_name[0].lower() + mapper_class_name[1:] + "Mapper"
        mapper_ctx = {
            "table_name": table_name,
            "class_name": mapper_class_name,
            "model_class_name": modelCtx["class_name"],
            # "model_name": modelCtx["model_name"],
            "columns": info["columns"],
            "primary_keys": info["primary_keys"],
            "appName":app_name,
        }
        rendered_mapper = mapperTemplate.render(**mapper_ctx)
        write_to_file(base_project_path, "mapper", f"{mapper_class_name}.py", rendered_mapper)
        

        # # service生成
        service_class_name = ''.join([i.capitalize() for i in table_name.split('_')])
        service_class_name = service_class_name[0].lower() + service_class_name[1:] + "Service"
        service_ctx = {
            "table_name": table_name,
            "class_name": service_class_name,
            "mapper_class_name": mapper_class_name,
            "model_class_name": modelCtx["class_name"],
            # "model_name": modelCtx["model_name"],
            "appName":app_name,
        }
        rendered_service = serviceTemplate.render(**service_ctx)
        write_to_file(base_project_path, "service", f"{service_class_name}.py", rendered_service)

        # # controller生成
        controller_class_name = ''.join([i.capitalize() for i in table_name.split('_')])
        controller_class_name = controller_class_name[0].lower() + controller_class_name[1:] + "Controller"
        controller_ctx = {
            "table_name": table_name,
            "class_name": controller_class_name,
            "service_class_name": service_class_name,
            "model_class_name": modelCtx["class_name"],
            "model_schema_name": modelCtx["model_schema_name"],
            "appName":app_name,
        }
        rendered_controller = controllerTemplate.render(**controller_ctx)
        write_to_file(base_project_path, "controller", f"{controller_class_name}.py", rendered_controller)
        controllerNameList.append(controller_class_name)
        


    # 处理其他文件
    ctx={
        "appName":app_name, # app的名称
        "controllerNameList":controllerNameList,
    }
    # 获取env中所有的template
    template_names=env.list_templates()

  

    for template_name in template_names:
        # 并且其中不包含'Template'字符
        if template_name.endswith(".tpl") and not "Template" in template_name:
            template=env.get_template(template_name)
            rendered = template.render(**ctx)
            # 输出到 base_out_dir 文件夹下。判断template_name是path则需要分理出路径和文件名信息
            if "/" in template_name:
                # 有路径
                path,filename=os.path.split(template_name)
                write_to_file(base_project_path,path,filename.replace(".tpl",".py"),rendered)
            else :   
                    # 如果包含manage 则输出到base_project_path的上一级目录下
                if "manage" in template_name:
                    base_path=base_project_path.replace("/"+app_name,"")
                    write_to_file(base_path,"",template_name.replace(".tpl",".py"),rendered)
                elif "application" in template_name : 
                    # 如果是application 则输出为yaml
                    write_to_file(base_project_path,"",template_name.replace(".tpl",".yaml"),rendered)
                else:
                    # 无路径，直接输出到根目录文件夹下
                    write_to_file(base_project_path,"",template_name.replace(".tpl",".py"),rendered)
        # 非.tpl文件的处理
        elif not template_name.endswith(".tpl"):
            path,filename=os.path.split(template_name)
            # 采用copy的方式 path=base_project_path+"/"+path，从
            # 获取template的路径
            # 采用copy的方式,不存在文件则创建
            if not os.path.exists(base_project_path+"/"+path):
                os.makedirs(base_project_path+"/"+path)
            shutil.copyfile(os.path.join("template",template_name), base_project_path+"/"+path+"/"+filename)
            

            
        
            

# 将模板渲染到文件中
def write_to_file(base_out_dir,package_name,file_name,rendered):
    model_dir = f"{base_out_dir}/{package_name}"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    out_file = f"{model_dir}/{file_name}"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(rendered)
    if(package_name=="model"):
        print(f"✔️ 生成model文件：{out_file}")
    elif(package_name=="mapper"):
        print(f"✔️ 生成mapper文件：{out_file}")
    elif(package_name=="service"):
        print(f"✔️ 生成service文件：{out_file}")
    elif(package_name=="controller"):
        print(f"✔️ 生成controller文件：{out_file}")
    else:
        print(f"✔️ 生成文件：{out_file}")
    

if __name__ == "__main__":

    # 数据库连接配置
    db_config = {
        "db_name":'demo',
        "db_type": "mysql",
        "db_url": "192.168.17.129", 
        "db_port":3306,
        "db_user":'root',
        "db_password":'123',
    }
    
    #     db_config = {
    #     "db_type": "sqlite3",
    #     "db_url": "db/codegen.db",
    # }
    # 代码生成规则配置
    # django-ninja 项目基本结构
    # -- 项目目录结构
    # -- app 目录
    # ------controller文件夹
    # ------service文件夹
    # ------mapper文件夹
    # ------model文件夹
    # ------exception文件夹
    # ------application.yaml 项目配置，端口，数据库
    # ------database.py 数据库初始化
    # ------urls.py 路由配置
    # ------settings.py django项目设置
    # ------asgi.py  ASGI 配置
    # ------wsgi.py WSGI 配置
    # -- manage.py 项目管理脚本

    
    ge_config={
        # 设置基本输出路径
        "base_out_dir" : "out",
    # 设置项目名称
        "base_project_name" : "demo",
        # 设置app名称
        "app_name": "app",
        # 包含的表名 ,为空则是不进行过滤
        "includes_table_names": [],
    }
    base_out_dir=ge_config["base_out_dir"]
    base_project_name=ge_config["base_project_name"]
    app_name=ge_config["app_name"]
    
    # 如果不存在out,out/demo,out/demo/demo 则创建
    if not os.path.exists(base_out_dir):
        os.makedirs(base_out_dir)
    if not os.path.exists(f"{base_out_dir}/{base_project_name}"):
        os.makedirs(f"{base_out_dir}/{base_project_name}")
        os.makedirs(f"{base_out_dir}/{base_project_name}/{app_name}")
    base_project_path = f"{base_out_dir}/{base_project_name}"
    base_app_path=f"{base_out_dir}/{base_project_name}/{app_name}"
    # 设置project路径
    ge_config["base_project_path"]=base_project_path
    # 设置app 的路径
    ge_config["base_app_path"]=base_app_path
    
    generate_code(ge_config,db_config)