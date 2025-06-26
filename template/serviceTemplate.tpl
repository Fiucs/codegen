from typing import List, Optional, Union
from {{appName}}.model.{{model_class_name}} import {{model_class_name}}
from {{appName}}.mapper.{{mapper_class_name}} import {{mapper_class_name}}
class {{class_name}}:
    @staticmethod
    def create_one(user_in: {{model_class_name}}) -> Optional[{{model_class_name}}]:
        user = {{mapper_class_name}}.create_one(user_in.to_dict())
        if user:
            return user
        return None
    
    @staticmethod
    def get_one(user_id: int) -> Optional[{{model_class_name}}]:
        user = {{mapper_class_name}}.get_one_by_id(user_id)

        if user:
            return user
        return None
    
    @staticmethod
    def get_all() -> List[{{model_class_name}}]:
        users = {{mapper_class_name}}.get_all()
        userList = list(users)
        print(userList)
        return userList
    
    @staticmethod
    def update_one( user_update: {{model_class_name}}) -> Optional[{{model_class_name}}]:

        user = {{mapper_class_name}}.update_one(user_update)
        if user:
            return user
        return None
    
    @staticmethod
    def delete_one(user_id: int) -> bool:
        return {{mapper_class_name}}.delete_one(user_id)
