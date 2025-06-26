{# userModel.tpl #}
from typing import Optional
from ninja import Schema
from peewee import AutoField, TextField, DateField,IntegerField
import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model
from {{appName}}.model.customBaseModel import customBaseModel

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
