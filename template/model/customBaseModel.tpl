import datetime
from peewee import DateTimeField, Model, AutoField, CharField, IntegerField, DateField
#此处是从database中读取数据库信息作为源
from ..database import db
class customBaseModel(Model):
    id = AutoField(primary_key=True, verbose_name="主键")

    # 如果数据库有这些字段才放开注释
    # create_time = DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    # update_time = DateTimeField(default=datetime.datetime.now, verbose_name="更新时间")
    # create_by = CharField(max_length=50, verbose_name="创建人")
    # update_by = CharField(max_length=50, verbose_name="更新人")

    class Meta:
        database = db

