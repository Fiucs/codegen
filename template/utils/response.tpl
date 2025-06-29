from typing import Any, Optional, Tuple

class Result:
    """
    统一API响应格式处理类
    
    示例:
        return Result.ok(data=user_data)
        return Result.error(code=404, msg="用户不存在")
    """

    @staticmethod
    def ok(
        data: Optional[Any] = None, 
        msg: str = "操作成功",
        code: int = 200
    ) -> Tuple[int, dict]:
        """成功响应"""
        return code, {
            "code": code,
            "msg": msg,
            "data": data
        }

    @staticmethod
    def error(
        msg: str = "操作失败",
        code: int = 400, 
        errors: Optional[Any] = None
    ) -> Tuple[int, dict]:
        """错误响应"""
        return code, {
            "code": code,
            "msg": msg,
            "errors": errors
        }

    @classmethod
    def make(cls, code: int, msg: str, data: Optional[Any] = None):
        """通用响应构造方法"""
        return code, {
            "code": code,
            "msg": msg,
            "data": data
        }



from pydantic import BaseModel
from typing import TypeVar, Generic, Optional    
T = TypeVar('T')

class ResultSchema(BaseModel, Generic[T]):
    
    code: int = 200
    msg: str = "操作成功"
    data: Optional[T] = None
    
    
    @staticmethod
    def ok(data: Optional[T] = None,msg: str = "操作成功",code: int = 200):
        return ResultSchema(code=code,msg=msg,data=data)
        

    @staticmethod
    def error(msg: str = "操作失败",code: int = 400, errors: Optional[Any] = None) :
        return ResultSchema(code=code,msg=msg,data=errors)        