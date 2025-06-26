
import os

# 上下文类
class MyContext:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'application.yaml')
