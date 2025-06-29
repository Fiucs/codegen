
# 自定义基础异常
from typing import Optional
from {{appName}}.exception.customBaseException import CustomBaseException

class ValidErrorException(CustomBaseException):
    def __init__(self, msg: str, data: Optional[dict] = None):
        self.msg = msg
        self.data = data
    def getMsg(self) -> str:
        return self.msg or "Service is unavailable"
    def getData(self):
        return self.data




