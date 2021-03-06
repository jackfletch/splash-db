from db import db
from db.schema import (
    Franchise,
    LeagueAverageShootingPct,
    Player,
    PlayerSeason,
    Roster,
    Season,
    Shot,
    Team,
)


def create_tables():
    db.connect(reuse_if_open=True)
    db.create_tables(
        [
            Season,
            Franchise,
            Player,
            Team,
            PlayerSeason,
            Roster,
            Shot,
            LeagueAverageShootingPct,
        ]
    )


if __name__ == "__main__":
    create_tables()
