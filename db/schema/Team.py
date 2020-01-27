from peewee import CharField, ForeignKeyField, IntegerField, SmallIntegerField

from .BaseModel import BaseModel
from .Franchise import Franchise
from .Season import Season


class Team(BaseModel):
    id = CharField(primary_key=True, unique=True)
    franchise_id = ForeignKeyField(Franchise, backref="teams")
    abbr = CharField(max_length=3)
    code = CharField(null=True)
    city = CharField()
    name = CharField()
    conference = CharField(null=True)
    division = CharField(null=True)
    season_from = ForeignKeyField(Season, backref="teams_from")
    season_to = ForeignKeyField(Season, backref="teams_to")
    games = IntegerField()
    wins = IntegerField()
    losses = IntegerField()
    playoff_appearances = SmallIntegerField()
    division_titles = SmallIntegerField()
    conference_titles = SmallIntegerField()
    league_titles = SmallIntegerField()
    color_primary = CharField(max_length=7, null=True)
    color_secondary = CharField(max_length=7, null=True)
    color_tertiary = CharField(max_length=7, null=True)

    class Meta:
        table_name = "teams"
