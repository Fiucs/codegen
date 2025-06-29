# 服务器异常
from typing import Optional
from {{appName}}.exception.customBaseException import CustomBaseException



class ServiceUnavailableError(CustomBaseException):
    def __init__(self, msg: str, data: Optional[dict] = None):
        # 继承关系 ：继承自 CustomBaseException ，复用基础异常类的错误处理逻辑
        super().__init__(msg, data)


