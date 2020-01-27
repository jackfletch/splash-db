from peewee import (
    AutoField,
    BooleanField,
    CharField,
    ForeignKeyField,
    IntegerField,
    SmallIntegerField,
)

from .BaseModel import BaseModel
from .Franchise import Franchise
from .Player import Player


class Shot(BaseModel):
    id = AutoField()
    game_id = IntegerField()
    game_event_id = CharField()
    player_id = ForeignKeyField(Player, backref="shots")
    distance = IntegerField()
    x = IntegerField()
    y = IntegerField()
    made = BooleanField()
    franchise_id = ForeignKeyField(Franchise, backref="shots")
    period = SmallIntegerField()
    minutes_remaining = SmallIntegerField()
    seconds_remaining = SmallIntegerField()
    action_type = CharField()
    shot_type = CharField()
    shot_zone_basic = CharField()
    shot_zone_area = CharField()
    shot_zone_range = CharField()
    game_date = IntegerField()
    season_type = SmallIntegerField()
    home_franchise = ForeignKeyField(Franchise, backref="shots_as_home")
    visitor_franchise = ForeignKeyField(Franchise, backref="shots_as_visitor")

    class Meta:
        table_name = "shots"
