from peewee import ForeignKeyField, IntegerField

from .BaseModel import BaseModel
from .Season import Season


class Franchise(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    season_from = ForeignKeyField(Season, backref="franchises_from")
    season_to = ForeignKeyField(Season, backref="franchises_to")

    class Meta:
        table_name = "franchises"
