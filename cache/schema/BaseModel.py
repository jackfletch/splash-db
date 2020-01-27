from peewee import Model

from cache import db


class BaseModel(Model):
    class Meta:
        database = db
