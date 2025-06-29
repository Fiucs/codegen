{# userModel.tpl #}
from typing import Optional
from ninja import Schema
from peewee import AutoField,BlobField, FloatField, TextField, DateField,IntegerField
import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model
from pydantic import validator
from {{appName}}.model.customBaseModel import customBaseModel
# 如果遇到Type is not JSON serializable: bytes 。可在各自schema中进行转换，然后使用ResultSchema 进行返回
# 一般不是返回json 而是流式传输到前端
##例如 
    # 二进制数据  流式传输而非json
#    blob_data: Optional[str] = None
#    @validator("blob_data", pre=True)
#    def convert_bytes(cls, v):
#        if isinstance(v, bytes):
#            try:
#                return v.decode('utf-8')
#            except UnicodeDecodeError:
#                return v.hex()  # 二进制转十六进制
#        return v
class {{ class_name }}(customBaseModel):
{% for col in columns %}
  # {{ col.comment }}
    {{ col.name }} = {{ col.field_type }}({{ col.params }})
{% endfor %}

    class Meta:
        table_name = '{{ table_name }}'
        indexes = (
{% for idx in indexes %}
            {{ idx }},
{% endfor %}
        )

    def __str__(self):
        return f"{{ '{{' }}self.{{ str_col }}{{ '}}' }} (ID: {{ '{{' }}self.{{ pk_col }}{{ '}}' }})"

    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def to_model(cls, data: dict):
        return dict_to_model(cls, data)

    def to_schema(self):
        return {{ class_name }}Schema.from_orm(self)


class {{ class_name }}Schema(Schema):
{% for col in columns %}
    # {{ col.comment }}
    {{ col.name }}: Optional[{{ col.py_type }}] = {{ col.default }}
{% endfor %}

    def to_model(self, is_create: bool = False) -> {{ class_name }}:
        data = self.dict()
        if is_create and '{{ pk_col }}' in data:
            del data['{{ pk_col }}']
        return {{ class_name }}.to_model(data)
