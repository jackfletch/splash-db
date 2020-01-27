from peewee import Model

from db import db


class BaseModel(Model):
    """A base model for PostgreSQL database"""

    class Meta:
        database = db
