import json
from typing import Dict, List, Sequence, Tuple, Union

from peewee import JOIN, Value

from db import db, init_db
from db.insert import insert_player, insert_shots
from db.schema import Player, Roster, Shot, Team
from endpoints import commonallplayers, shotchartdetail
from utils.fetch import fetch
from utils.season import SeasonType, seasonyear

SEASON_ID_CURRENT = 2019
SEASON_ID_FIRST_SHOTCHARTDETAIL = 1996


def get_season_abbr_to_franchise_id_map(season_id: int) -> Dict[str, int]:
    return {
        t.abbr: t.franchise_id.id
        for t in Team.select().where(
            Team.season_from <= season_id, Team.season_to >= season_id
        )
    }


def get_abbr_to_franchise_id_map():
    totalmap = {}
    for season in range(SEASON_ID_FIRST_SHOTCHARTDETAIL, SEASON_ID_CURRENT):
        tmap = get_season_abbr_to_franchise_id_map(season)
        totalmap.update(tmap)

    totalmap["CHH"] = 1610612766
    return totalmap


def get_shots(player_id: int, season_id: int):
    franchise_id_map = get_abbr_to_franchise_id_map()
    for season_type in [SeasonType.regular_season, SeasonType.playoffs]:
        url = shotchartdetail.build_shotchartdetail_url(
            player_id=player_id, season_id=season_id, season_type=season_type
        )
        res = fetch(
            url=url, description=f"get_shots {player_id} {season_id} {season_type.name}"
        )
        shots = res["resultSets"][0]["rowSet"]
        fshots = []
        indexes_to_remove = [0, 4, 6, 10, 19]
        for shot in shots:
            shot.append(season_type.value)
            shot[-3] = franchise_id_map[shot[-3]]
            shot[-2] = franchise_id_map[shot[-2]]
            # if shot[12] == None:
            #     print(*shot)
            #     if shot[16] < 18:
            #         shot[12] = "2PT Field Goal"
            fshot = tuple([v for i, v in enumerate(shot) if i not in indexes_to_remove])
            fshots.append(fshot)

        insert_shots(fshots)


def get_players(season_id: int):
    url = commonallplayers.build_players_url(season_id=season_id)
    res = fetch(url=url, description=f"get_players {season_id}")
    # print(res["resultSets"][0]["headers"])
    players = res["resultSets"][0]["rowSet"]

    fplayers = []
    # indexes_to_remove = [0, 4, 6, 10, 19]
    indexes_to_remove = []
    for player in players:
        fplayer = tuple([v for i, v in enumerate(player) if i not in indexes_to_remove])
        fplayers.append(fplayer)

    for p in fplayers:
        (
            id,
            name_last_first,
            name_first_last,
            _roster_status,
            season_from,
            season_to,
            playercode,
            franchise_id,
            _team_city,
            _team_name,
            _team_abbr,
            _team_code,
            _games_plgames_playedayed,
            _otherleague_exp_ch,
        ) = p
        franchise_id = None if franchise_id == 0 else franchise_id
        insert_player(
            id=id,
            name_last_first=name_last_first,
            name_first_last=name_first_last,
            season_from=season_from,
            season_to=season_to,
            code=playercode,
            franchise_id=franchise_id,
        )


SeasonFormattedForDatabase = List[Tuple[int, str]]


def get_all_players_shots(player_id: int):
    player = Player(database=db).get_by_id(player_id)
    season_from, season_to = player.season_from.id, player.season_to.id
    i = 0
    if season_to >= SEASON_ID_FIRST_SHOTCHARTDETAIL:
        start = max(season_from, SEASON_ID_FIRST_SHOTCHARTDETAIL)
        end = min(season_to, SEASON_ID_CURRENT)
        for season in range(start, end + 1):
            get_shots(player.id, season)


def get_all_players(season_id: int):
    players = (
        Player.select()
        .where(Player.season_to == season_id)
        .order_by(Player.name_last_first)
    )
    for player in players:
        print(season_id, player, player.name_last_first)
        shots_by_player = Shot.select().where(Shot.player_id == player)
        if len(shots_by_player) == 0 or player.id == 376:
            get_all_players_shots(player)


def insert_roster(
    player_id: int, season_id: int, team_id: int, franchise_id: int, debut_date: int
):
    Roster(database=db).insert(
        debut_date=debut_date,
        franchise_id=franchise_id,
        player_id=player_id,
        season_id=season_id,
        team_id=team_id,
    ).on_conflict(action="IGNORE").execute()


def get_player_rosters(player_id: int):
    season_id = (Shot.game_date - 1000) / 10000
    distinct_franchises = (
        Shot.select(Shot.franchise_id, season_id.alias("season_id"), Shot.game_date)
        .distinct(Shot.franchise_id, season_id)
        .where(Shot.player_id == player_id)
        .order_by(Shot.franchise_id, season_id)
    )
    franchise_season = (
        Shot.select(
            distinct_franchises.c.franchise_id,
            distinct_franchises.c.season_id,
            distinct_franchises.c.game_date,
        )
        .from_(distinct_franchises)
        .order_by(distinct_franchises.c.game_date)
    )
    rosters = (
        Team.select(
            Team.id,
            Team.franchise_id,
            Team.abbr,
            franchise_season.c.season_id,
            franchise_season.c.game_date,
        )
        .join(
            franchise_season,
            JOIN.INNER,
            on=((franchise_season.c.franchise_id == Team.franchise_id)),
        )
        .where(
            franchise_season.c.season_id >= Team.season_from_id,
            franchise_season.c.season_id <= Team.season_to_id,
        )
        .namedtuples()
    )
    for t in rosters:
        # print(player_id, t.season_id, t.id, t.franchise_id, t.game_date)
        insert_roster(
            debut_date=t.game_date,
            franchise_id=t.franchise_id,
            player_id=player_id,
            season_id=t.season_id,
            team_id=t.id,
        )


def get_players_rosters():
    players = Player.select().where(Player.season_to >= SEASON_ID_FIRST_SHOTCHARTDETAIL)
    for player in players:
        get_player_rosters(player.id)


if __name__ == "__main__":
    init_db()
    # for i in range(SEASON_ID_CURRENT, SEASON_ID_FIRST_SHOTCHARTDETAIL - 1, -1):
    #     get_all_players(i)
    # get_players_rosters()
    # get_player_rosters(203957)
