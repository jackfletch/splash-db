from peewee import AutoField, CharField, ForeignKeyField

from .BaseModel import BaseModel
from .Season import Season
from .Team import Team


class TeamSeason(BaseModel):
    id = AutoField()
    season = ForeignKeyField(Season, backref="teams")
    team_id = ForeignKeyField(Team, backref="seasons")

    class Meta:
        table_name = "team_seasons"
