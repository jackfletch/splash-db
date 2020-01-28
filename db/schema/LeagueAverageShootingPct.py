from peewee import AutoField, CharField, FloatField, ForeignKeyField, IntegerField

from .BaseModel import BaseModel
from .Season import Season


class LeagueAverageShootingPct(BaseModel):
    id = AutoField()
    distance = IntegerField()
    season_id = ForeignKeyField(Season, backref="LeagueAverageShootingPct")
    pct = FloatField()

    class Meta:
        table_name = "league_average_shooting_pct"
