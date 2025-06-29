# initializing handler
# 异常拦截


# 定义异常拦截的注册
import http
from math import log

from {{appName}}.constans.http_code import *




def register_exception_handlers(api):
    from {{appName}}.exception.serviceUnavailableException import ServiceUnavailableError
    from {{appName}}.exception.customBaseException import CustomBaseException
    from {{appName}}.exception.validErrorException import ValidErrorException
    from ninja.errors import ValidationError as NinjaValidationError
    # 服务异常拦截
    @api.exception_handler(ServiceUnavailableError)
    def service_unavailable(request, exc: ServiceUnavailableError):
        return api.create_response(
            request,
            {"code": HTTP_CODE_503, "message": exc.getMsg(), "data": exc.getData()},
            status=HTTP_CODE_503,
        )
    @api.exception_handler(ValidErrorException)
    def valid_error_exception(request, exc: ValidErrorException):
        return api.create_response(
            
            request,
            {"code": HTTP_CODE_422, "message": exc.getMsg(), "data": exc.getData()},
            status=HTTP_CODE_422,
        )
        # 自定义异常拦截
    @api.exception_handler(CustomBaseException)
    def custom_exception(request, exc: CustomBaseException):
        return api.create_response(
            request,
            {"code": HTTP_CODE_500, "message": exc.getMsg(), "data": exc.getData()},
            status=HTTP_CODE_500,
        )
        # 参数校验异常拦截 拦截Pydantic的ValidationError异常
    @api.exception_handler(NinjaValidationError)
    def validation_exception_handler(request, exc: NinjaValidationError):
        # exc.errors 是 Pydantic 的标准错误列表
        error_list = exc.errors
        
        # 自定义格式，例如提取 msg 和字段名
        custom_errors = [
            {
                "field": ".".join([str(loc) for loc in err["loc"]]),
                "message": err["msg"],
                "type": err.get("type"),
            }
            for err in error_list
        ]

        return api.create_response(
            request,
            {
                "code": HTTP_CODE_422,
                "msg": "参数校验失败",
                "errors": custom_errors
            },
            status=HTTP_CODE_422
        )
    # 全局异常拦截
    @api.exception_handler(Exception)
    def global_exception(request, exc: Exception):
        print(f'全局异常拦截:{exc}')
        return api.create_response(
            request,
            {"code": HTTP_CODE_500, "message": "服务异常"+str(exc), "data": None},
            status=HTTP_CODE_500,
        )
