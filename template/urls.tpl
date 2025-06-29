"""
URL configuration for apidemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import Optional
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from decimal import Decimal

{% for controllerName in controllerNameList %}
  # {{ contr }}
from {{appName}}.controller import {{controllerName}}
{% endfor %}


from ninja.renderers import BaseRenderer
import orjson

class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        
        # 递归转换 Decimal 为 float
        def convert_decimal(obj):
            if isinstance(obj, Decimal):
                return float(obj)  # 或 str(obj) 保留精度
            if isinstance(obj, dict):
                return {k: convert_decimal(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_decimal(item) for item in obj]
            return obj
        
        # 处理数据并序列化
        processed_data = convert_decimal(data)
        
        
        
        return orjson.dumps(
            processed_data,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_DATACLASS 
        )

# 初始化NinjaAPI实例，用于创建RESTful API接口
api = NinjaAPI(renderer=ORJSONRenderer())

# 添加用户路由
# 将 user_controller.router 中定义的所有用户相关接口，统一挂载到 /users/ 路径下。
# - 例如：若 user_controller 中有 @router.get("/list") 接口，
# 则完整访问路径为 /api/users/list （因 api 实例已挂载在 /api/ 路由下）。



# 重要 需要在api初始的时候注册异常的拦截函数
from {{appName}}.exception.exceptionhandlers.exceptionHandler import register_exception_handlers
register_exception_handlers(api)


# 定义controller路由 
{% for controllerName in controllerNameList %}
  # {{ contr }}
api.add_router("", {{controllerName}}.router)
{% endfor %}




# 定义api基本路由
urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理后台路由
    path("api/", api.urls),   # 加减法接口路由入口
 
]
