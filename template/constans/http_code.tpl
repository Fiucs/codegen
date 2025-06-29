# 定义常见的http响应code,注释

# 请求成功
HTTP_CODE_200 = 200
# 无效请求（参数错误或格式不正确）
HTTP_CODE_400 = 400
# 身份验证失败（未提供有效凭证）
HTTP_CODE_401 = 401
# 权限不足（禁止访问资源）
HTTP_CODE_403 = 403
# 资源不存在
HTTP_CODE_404 = 404
# 参数校验失败
HTTP_CODE_422=422
# 服务器内部错误
HTTP_CODE_500 = 500
# 服务暂时不可用（维护或过载）
HTTP_CODE_503 = 503

# 定义常见的http响应code的注释
HTTP_CODE_200_MSG = "success"
HTTP_CODE_400_MSG = "Bad Request"
HTTP_CODE_401_MSG = "Unauthorized"
HTTP_CODE_403_MSG = "Forbidden"
HTTP_CODE_404_MSG = "Not Found"
HTTP_CODE_422_MSG=  "Unprocessable Entity"
HTTP_CODE_500_MSG = "Internal Server Error"
HTTP_CODE_503_MSG = "Service Unavailable"
