import os
import sys
import yaml
from {{appName}}.context import MyContext

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apidemo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
        # 初始化操作，读取application配置文件
    # 1. 读取application.yaml文件
    config = {}
    base_dir = MyContext.BASE_DIR
    config_file_path = MyContext.CONFIG_FILE_PATH
    
    with open(config_file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    # 2. 从config中获取端口号,默认8000

    if "runserver" in sys.argv:
        # 获取环境变量或使用默认值
        # port默认值 8081
        port = config.get('server').get('port')
        # 如果为None,则使用默认值
        port = port if port is not None else 8000
        # url默认值 127.0.0.1
        url = config.get('server').get('url')
        # 如果为None,则使用默认值
        url = url if url is not None else '127.0.0.1'
        
    if not any(":" in arg for arg in sys.argv):
        sys.argv.append(f"{url}:{port}")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


