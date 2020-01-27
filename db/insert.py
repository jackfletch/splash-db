import json
from typing import Dict, List, Sequence, Tuple, Union

from db import db
from db.schema import Franchise, Player, Season, Shot, Team
from utils.season import seasonyear

SeasonFormattedForDatabase = List[Tuple[int, str]]
TeamRaw = List[Union[str, int, Sequence[str]]]
TeamFormattedForDatabase = Tuple[
    int, str, str, str, str, str, str, int, int, str, str, str
]
FranchiseRaw = List[Union[str, int]]
FranchiseFormattedForDatabase = Tuple[
    int, str, str, int, int, int, int, int, int, float, int, int, int, int
]


def insert_seasons(seasons: SeasonFormattedForDatabase):
    Season(database=db).insert_many(
        seasons, fields=[Season.id, Season.string]
    ).on_conflict(action="IGNORE").execute()


def get_seasons() -> SeasonFormattedForDatabase:
    return [(year, seasonyear(year)) for year in range(1946, 2020)]


def init_seasons():
    seasons = get_seasons()
    insert_seasons(seasons)


def insert_teams(teams):
    Team(database=db).insert_many(
        teams,
        fields=[
            Team.id,
            Team.franchise_id,
            Team.abbr,
            Team.code,
            Team.city,
            Team.name,
            Team.conference,
            Team.division,
            Team.season_from,
            Team.season_to,
            Team.games,
            Team.wins,
            Team.losses,
            Team.playoff_appearances,
            Team.division_titles,
            Team.conference_titles,
            Team.league_titles,
            Team.color_primary,
            Team.color_secondary,
            Team.color_tertiary,
        ],
    ).on_conflict(action="IGNORE").execute()


def insert_franchises(franchises):
    Franchise(database=db).insert_many(
        franchises, fields=[Franchise.id, Franchise.season_from, Franchise.season_to],
    ).on_conflict(action="IGNORE").execute()


ConferenceIdToString: Dict[int, str] = {
    1: "Eastern",
    2: "Western",
}

DivisionIdToString: Dict[int, str] = {
    1: "Atlantic",
    2: "Central",
    3: "Northwest",
    4: "Pacific",
    5: "Southeast",
    6: "Southwest",
}

TeamFirstSeason: Dict[str, int] = {
    "ATL": 1949,
    "BOS": 1946,
    "BKN": 1976,
    "CHA": 1988,
    "CHI": 1966,
    "CLE": 1970,
    "DAL": 1980,
    "DEN": 1976,
    "DET": 1948,
    "GSW": 1946,
    "HOU": 1967,
    "IND": 1976,
    "LAC": 1970,
    "LAL": 1948,
    "MEM": 1995,
    "MIA": 1988,
    "MIL": 1968,
    "MIN": 1989,
    "NOP": 2002,
    "NYK": 1946,
    "OKC": 1967,
    "ORL": 1989,
    "PHI": 1949,
    "PHX": 1968,
    "POR": 1970,
    "SAC": 1948,
    "SAS": 1976,
    "TOR": 1995,
    "UTA": 1974,
    "WAS": 1961,
}


def get_teams_from_stats_ptsd():

    with open("stats_ptsd.json") as f:
        data = json.load(f)

    def is_nba_team(team: TeamRaw) -> bool:
        return team[7] == 0

    def unpack_colors(colors) -> Tuple[str, str, str]:
        primary = colors[0]
        secondary = colors[1]
        tertiary = colors[2] if len(colors) == 3 else None
        return primary, secondary, tertiary

    def unpack_team(team: TeamRaw) -> TeamFormattedForDatabase:
        franchise_id = int(team[0])
        abbr, code, city, name = team[1:5]
        conference = ConferenceIdToString[team[5]]
        division = DivisionIdToString[team[6]]
        season_from = TeamFirstSeason[abbr]
        season_to = team[8]
        color_primary, color_secondary, color_tertiary = unpack_colors(team[10])
        id = f"{franchise_id}-{season_from}"

        return (
            id,
            franchise_id,
            abbr,
            code,
            city,
            name,
            conference,
            division,
            season_from,
            season_to,
            color_primary,
            color_secondary,
            color_tertiary,
        )

    return [unpack_team(team) for team in data["data"]["teams"] if is_nba_team(team)]


def combine_teams(franchise_team, stats_team=None):
    (
        id,
        franchise_id,
        city,
        name,
        abbr,
        season_from,
        season_to,
        _years,
        games,
        wins,
        losses,
        _win_pct,
        playoff_appearances,
        division_titles,
        conference_titles,
        league_titles,
    ) = franchise_team
    if stats_team:
        (
            _id,
            _franchise_id,
            _abbr,
            code,
            _city,
            _name,
            conference,
            division,
            _season_from,
            _season_to,
            color_primary,
            color_secondary,
            color_tertiary,
        ) = stats_team
    else:
        code = None
        conference = None
        division = None
        color_primary = None
        color_secondary = None
        color_tertiary = None
    return (
        id,
        franchise_id,
        abbr,
        code,
        city,
        name,
        conference,
        division,
        season_from,
        season_to,
        games,
        wins,
        losses,
        playoff_appearances,
        division_titles,
        conference_titles,
        league_titles,
        color_primary,
        color_secondary,
        color_tertiary,
    )


def get_teams():
    stats_teams = get_teams_from_stats_ptsd()
    franchise_teams = get_teams_from_franchisehistory()

    seen_ids = []
    fteams = []
    for team in franchise_teams:
        franchise_id = team[1]
        if franchise_id not in seen_ids:
            stats_team = [t for t in stats_teams if t[1] == franchise_id][0]
            seen_ids.append(franchise_id)
            fteam = combine_teams(team, stats_team)
        else:
            fteam = combine_teams(team)
        fteams.append(fteam)
    # for team in fteams:
    #     print(team)
    return fteams


def get_teams_from_franchisehistory():
    with open("franchisehistory.json") as f:
        data = json.load(f)

    def unpack_franchise_teams(
        franchise: FranchiseRaw,
    ) -> FranchiseFormattedForDatabase:
        (
            _league_id,
            franchise_id,
            city,
            name,
            abbr,
            start_year,
            end_year,
            years,
            games,
            wins,
            losses,
            win_pct,
            playoff_appearances,
            division_titles,
            conference_titles,
            league_titles,
        ) = franchise
        id = f"{franchise_id}-{start_year}"
        return (
            id,
            franchise_id,
            city,
            name,
            abbr,
            int(start_year),
            int(end_year),
            years,
            games,
            wins,
            losses,
            win_pct,
            playoff_appearances,
            division_titles,
            conference_titles,
            league_titles,
        )

    # print(data["resultSets"][0]["headers"])
    unpacked = [
        unpack_franchise_teams(franchise)
        for franchise in data["resultSets"][0]["rowSet"]
    ]

    def count_id(franchise):
        franchise_id = franchise[1]
        return sum(franchise_id in franchise for franchise in unpacked)

    last_id = None
    first_seen_idx = []
    for i, franchise in enumerate(unpacked):
        franchise_id = franchise[1]
        if franchise_id == last_id:
            continue
        else:
            first_seen_idx.append(i)
            last_id = franchise_id

    single_ids = [i for i, franchise in enumerate(unpacked) if count_id(franchise) == 1]
    totaling_franchises = [i for i in first_seen_idx if i not in single_ids]
    totaled_teams = [
        team for i, team in enumerate(unpacked) if i not in totaling_franchises
    ]
    totaling_franchises_plus1 = list(map(lambda x: x + 1, totaling_franchises))
    latest_teams_idx = single_ids + totaling_franchises_plus1
    return totaled_teams


def get_franchises():
    with open("franchisehistory.json") as f:
        data = json.load(f)

    def unpack_franchise(franchise: FranchiseRaw) -> FranchiseFormattedForDatabase:
        (
            _league_id,
            id,
            _team_city,
            _team_name,
            _team_abbr,
            start_year,
            end_year,
            _years,
            _games,
            _wins,
            _losses,
            _win_pct,
            _playoff_appearances,
            _division_titles,
            _conference_titles,
            _league_titles,
        ) = franchise

        return (
            id,
            int(start_year),
            int(end_year),
        )

    # print(data["resultSets"][0]["headers"])
    unpacked = [
        unpack_franchise(franchise) for franchise in data["resultSets"][0]["rowSet"]
    ]

    def count_id(franchise):
        franchise_id = franchise[0]
        return sum(franchise_id in franchise for franchise in unpacked)

    last_id = None
    first_seen_idx = []
    for i, franchise in enumerate(unpacked):
        franchise_id = franchise[0]
        if franchise_id == last_id:
            continue
        else:
            first_seen_idx.append(i)
            last_id = franchise_id

    single_ids = [i for i, franchise in enumerate(unpacked) if count_id(franchise) == 1]
    totaling_franchises = [i for i in first_seen_idx if i not in single_ids]
    return [unpacked[i] for i in first_seen_idx]


def init_teams():
    teams = get_teams()
    insert_teams(teams)


def init_franchises():
    franchises = get_franchises()
    insert_franchises(franchises)


def insert_player(
    id, name_last_first, name_first_last, code, season_from, season_to, franchise_id
):
    Player(database=db).insert(
        id=id,
        name_last_first=name_last_first,
        name_first_last=name_first_last,
        code=code,
        season_from=season_from,
        season_to=season_to,
        franchise_id=franchise_id,
    ).on_conflict(action="IGNORE").execute()


def insert_shots(shots):
    Shot(database=db).insert_many(
        shots,
        fields=[
            Shot.game_id,
            Shot.game_event_id,
            Shot.player_id,
            Shot.franchise_id,
            Shot.period,
            Shot.minutes_remaining,
            Shot.seconds_remaining,
            Shot.action_type,
            Shot.shot_type,
            Shot.shot_zone_basic,
            Shot.shot_zone_area,
            Shot.shot_zone_range,
            Shot.distance,
            Shot.x,
            Shot.y,
            Shot.made,
            Shot.game_date,
            Shot.home_franchise,
            Shot.visitor_franchise,
            Shot.season_type,
        ],
    ).on_conflict(action="IGNORE").execute()


if __name__ == "__main__":
    init_seasons()
    init_franchises()
    init_teams()
