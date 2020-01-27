from peewee import CharField, ForeignKeyField, IntegerField

from .BaseModel import BaseModel
from .Franchise import Franchise
from .Season import Season


class Player(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    name_last_first = CharField()
    name_first_last = CharField()
    code = CharField(null=True)
    season_from = ForeignKeyField(Season, backref="player_first_season")
    season_to = ForeignKeyField(Season, backref="player_final_season")
    franchise_id = ForeignKeyField(Franchise, backref="current_franchise", null=True)

    class Meta:
        table_name = "players"
