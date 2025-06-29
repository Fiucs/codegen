# PyCodeGen

一个强大的Python代码生成工具，能够根据数据库结构自动生成各类代码文件，提高开发效率。生成的代码文件包含：
- 控制器（controller）：处理HTTP请求和响应的代码
- 服务层（service）：封装业务逻辑的代码
- 数据操作层（mapper）：负责数据的增删改查操作
- 模型（Model）：定义数据库表结构的Python类
- 

## 项目框架
- Django-Ninja：用于快速创建RESTful API的库
- Peewee ORM：用于数据库操作的Python ORM库


## 功能特性
- **多数据源支持**：和`getTablesData_peewee.py`（Peewee ORM）方式获取数据库表结构数据，兼容不同开发习惯
- **模板引擎集成**：基于`jinjia2Render.py`实现Jinja2模板渲染，支持动态填充数据库字段、表关系等元数据
- **多类型代码生成**：内置`template`目录包含模型（`modelTemplate.tpl`）、控制器（`controllerTemplate.tpl`）、服务层（`serviceTemplate.tpl`）等10+种模板，覆盖MVC架构核心组件
- **项目结构生成**：自动生成`out/demo/`类似的完整项目目录，包含`app/`业务代码和`manage.py`入口文件，直接支持本地运行
- **配置扩展能力**：通过`template/context.tpl`可自定义全局上下文变量，支持添加额外元数据（如作者信息、版本号）到生成代码中

## 安装步骤
```bash
pip install -r requirements.txt
```

## 使用方法
1. 连接sqlite3 数据库，mysql，postgresql
2. 配置路径设置和数据库连接设置，在`jinjia2Render.py`中
    db_config = {
        "db_name":'demo', # 数据库名称
        "db_type": "mysql", # 数据库类型
        "db_url": "192.168.17.129", # 数据库地址（sqlite3直接填写数据库文件地址即可，数据库名称不填）
        "db_port":3306, # 数据库端口
        "db_user":'root', # 数据库用户名
        "db_password":'123', # 数据库密码
    }
    
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

2. 运行代码生成命令：
生成代码
python jinjia2Render.py

```bash
生成的项目是django-ninja ,运行命令
cd out
python manage.py runserver
```

## 项目结构
```
pycodegen/
├── db/
│   └── codegen.db
├── template/
│   ├── modelTemplate.tpl
│   └── controllerTemplate.tpl
├── out/
│   └──    
django-ninja 项目基本结构
         -- 项目目录结构
         -- app 目录
         ------controller文件夹
         ------service文件夹
         ------mapper文件夹
         ------model文件夹
         ------exception文件夹
         ------application.yaml 项目配置，端口，数据库
         ------database.py 数据库初始化
         ------urls.py 路由配置
         ------settings.py django项目设置
         ------asgi.py  ASGI 配置
         ------wsgi.py WSGI 配置
         -- manage.py 项目管理脚本
├── .gitignore
├── LICENSE
├── README.md

```

## 功能待开发
- [x] 支持sqlite3
- [ ] 支持mysql
- [ ] 支持postgresql
- [ ] 支持oracle
- [ ] 支持sqlserver


## 许可证
本项目采用MIT许可证 - 详情参见LICENSE文件

## 贡献
欢迎提交issues和pull requests来帮助改进这个项目

## 联系方式
如有问题，请联系项目维护者: example@example.com