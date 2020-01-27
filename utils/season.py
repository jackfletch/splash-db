from enum import Enum
from typing import Dict, Union


class SeasonType(Enum):
    preseason = 1
    regular_season = 2
    all_star = 3
    playoffs = 4


SeasonTypeStringDict: Dict[int, str] = {
    1: "Pre Season",
    2: "Regular Season",
    3: "All Star",
    4: "Playoffs",
}


def seasonyear(year: Union[int, str]) -> str:
    next_year = str(int(year) + 1)[-2:]
    return f"{year}-{next_year}"


if __name__ == "__main__":
    print(seasonyear("2016"))
    print(seasonyear(2016))
