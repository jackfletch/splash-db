from utils.build_url import build_url
from utils.season import SeasonType, SeasonTypeStringDict, seasonyear


def build_shotchartdetail_url(
    player_id: int,
    season_id: int,
    season_type: int = SeasonType.regular_season.value,
    outcome: str = "",
    period: int = 0,
) -> str:
    season = seasonyear(season_id)
    params = {
        "CFID": "33",
        "CFPARAMS": str(season),
        "ContextFilter": "",
        "ContextMeasure": "FGA",
        "DateFrom": "",
        "DateTo": "",
        "GameID": "",
        "GameSegment": "",
        "LastNGames": "0",
        "LeagueID": "00",
        "Location": "",
        "MeasureType": "Base",
        "Month": "0",
        "OpponentTeamID": "0",
        "Outcome": outcome,
        "PaceAdjust": "N",
        "PerMode": "PerGame",
        "Period": str(period),
        "PlayerID": str(player_id),
        "PlayerPosition": "",
        "PlusMinus": "N",
        "Position": "",
        "Rank": "N",
        "RookieYear": "",
        "Season": str(season),
        "SeasonSegment": "",
        "SeasonType": SeasonTypeStringDict[season_type.value],
        "TeamID": "0",
        "VsConference": "",
        "VsDivision": "",
        "mode": "Advanced",
        "showDetails": "0",
        "showShots": "1",
        "showZones": "0",
    }

    base_url = "http://stats.nba.com/stats/shotchartdetail?"

    return build_url(base_url, params)
