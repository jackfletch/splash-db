from peewee import CharField
from playhouse.sqlite_ext import JSONField

from .BaseModel import BaseModel


class Request(BaseModel):
    url = CharField(unique=True)
    response = JSONField()

    class Meta:
        table_name = "requests"
