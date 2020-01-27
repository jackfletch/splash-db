from peewee import AutoField, ForeignKeyField

from .BaseModel import BaseModel
from .Player import Player
from .Season import Season


class PlayerSeason(BaseModel):
    id = AutoField()
    player_id = ForeignKeyField(Player, backref="seasons")
    season_id = ForeignKeyField(Season, backref="players")

    class Meta:
        table_name = "player_seasons"
