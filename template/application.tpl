# 这里用来配置应用的端口号，数据库等信息
server:
  port: 8080
  url:   

# 配置数据库信息，指定数据库连接，用户名，密码，数据库类型
datasource:
  # database: sqlite3
  # 如果是本地数据库，url可以指定为文件路径。
  # 例如sqlite3,这里是相对于项目根目录路径  apidemo/db/demo.db
  # url: db/demo.db
  database: mysql
  url: 192.168.17.129
  port: 3306
  dbname: demo
  username: root
  password: 123
  charset: utf8mb4



