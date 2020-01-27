from peewee import AutoField, ForeignKeyField, IntegerField

from .BaseModel import BaseModel
from .Franchise import Franchise
from .Player import Player
from .Season import Season
from .Team import Team


class Roster(BaseModel):
    id = AutoField()
    player_id = ForeignKeyField(Player, backref="rosters")
    season_id = ForeignKeyField(Season, backref="rosters")
    team_id = ForeignKeyField(Team, backref="rosters")
    franchise_id = ForeignKeyField(Franchise, backref="rosters")
    debut_date = IntegerField()

    class Meta:
        table_name = "rosters"
