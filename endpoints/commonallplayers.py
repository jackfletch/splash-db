from utils.build_url import build_url
from utils.season import SeasonType, SeasonTypeStringDict, seasonyear


def build_players_url(season_id: int, isOnlyCurrentSeason: int = 0,) -> str:
    season = seasonyear(season_id)
    params = {
        "LeagueID": "00",
        "Season": season,
        "isOnlyCurrentSeason": isOnlyCurrentSeason,
    }

    base_url = "https://stats.nba.com/stats/commonallplayers?"

    return build_url(base_url, params)
