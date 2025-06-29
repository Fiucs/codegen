from ninja import Router
from {{appName}}.model.{{model_class_name}} import {{model_class_name}},{{model_schema_name}}
from {{appName}}.service.{{service_class_name}} import {{service_class_name}}
from {{appName}}.utils.response import Result,ResultSchema

router = Router(tags=["{{table_name}}"])

#默认使用表名为前缀
@router.get("/{{table_name}}/get_one/{id}/")
def get_one(request, id: int):
    """
    获取详情
    不指定response格式
    """
    user = {{service_class_name}}.get_one(id)
    if user:
        res=Result.ok(data=user.to_dict())
        return res
    return Result.error(code=404, msg="用户不存在")


@router.post("/{{table_name}}/crete/")
def create_one(request, payload: {{model_schema_name}}):
  
    """
    创建
    """
    user = {{service_class_name}}.create_one(payload.to_model(is_create=True))
    if user:
        return Result.ok(data=user.to_dict())
    return Result.error(code=400, msg="创建用户失败，可能是用户名已存在")
    


    #  使用schema作为response
# @router.get("/test_table/get_list/",response=ResultSchema)
# def list_all(request):
#     userList=testTableService.get_all()
#     userDictList=[]
#     for user in userList:
       
#         userDictList.append(user.to_schema())
#     return ResultSchema.ok(data=userDictList)

@router.get("/{{table_name}}/get_list/", )
def list_all(request):
    user_list=[user.to_dict() for user in {{service_class_name}}.get_all()]
    return Result.ok(data=user_list)

@router.put("/{{table_name}}/update/")
def update_one(request, payload: {{model_schema_name}}):
    if payload.id is None:
        return Result.error(code=400, msg="用户ID不能为空")
    # 检查用户是否存在
    if not {{service_class_name}}.get_one(payload.id):
        return Result.error(code=404, msg="用户不存在")
    user = {{service_class_name}}.update_one(payload.to_model(is_create=False))
    if user:
        return Result.ok(data=user.to_dict())
    return Result.error(code=400, msg="更新用户失败，可能是用户名已存在")

@router.delete("/{{table_name}}/delete/{id}/")
def delete_one(request, id: int):
    if {{service_class_name}}.delete_one(id):
        return Result.ok(data="删除成功")
    return Result.error(code=404, msg="删除失败,数据不存在")


