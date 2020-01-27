from db import db
from db.schema import Franchise, Player, PlayerSeason, Roster, Season, Shot, Team


def drop_tables():
    db.connect(reuse_if_open=True)
    db.drop_tables([PlayerSeason, Roster, Shot])
    db.drop_tables([Player])
    db.drop_tables([Team, Franchise])
    db.drop_tables([Season])


if __name__ == "__main__":
    drop_tables()
