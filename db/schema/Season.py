from peewee import CharField, IntegerField

from .BaseModel import BaseModel


class Season(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    string = CharField(unique=True)

    class Meta:
        table_name = "seasons"
