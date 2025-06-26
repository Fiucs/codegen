from {{appName}}.model.{{model_class_name}} import {{model_class_name}}
from peewee import DoesNotExist, IntegrityError


class {{class_name}}:
    @staticmethod
    def get_one_by_id(user_id: int):
        try:
            return {{model_class_name}}.get_by_id(user_id)
        except DoesNotExist:
            return None
    
    @staticmethod
    def get_all():
        return list({{model_class_name}}.select().order_by({{model_class_name}}.id))
    
    @staticmethod
    def create_one(user_data: dict):
        try:
            return {{model_class_name}}.create(**user_data)
        except IntegrityError:
            # 处理唯一约束冲突（如用户名重复）
            return None
    
    @staticmethod
    def update_one( user_update: {{model_class_name}}):
        user_id=user_update.id
        # 移除None值
        update_data = {k: v for k, v in user_update.to_dict().items() if v is not None}
        # update_data.pop("id")
        
        if not update_data:
            return None
            
        try:
            query = {{model_class_name}}.update(**update_data).where({{model_class_name}}.id == user_id)
            rows_updated = query.execute()
            if rows_updated > 0:
                return {{model_class_name}}.get_by_id(user_id)
            return None
        except IntegrityError:
            # 处理唯一约束冲突
            return None
    
    @staticmethod
    def delete_one(user_id: int):
        try:
            user = {{model_class_name}}.get_by_id(user_id)
            user.delete_instance()
            return True
        except DoesNotExist:
            return False