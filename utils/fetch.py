import httpx
from peewee import DoesNotExist

from cache import get_cached_request, insert_request


def fetch(url: str, description: str = ""):
    fetch_code = description or url
    try:
        res = get_cached_request(url)
    except DoesNotExist:
        print("cache-miss: %s" % fetch_code)
        res = fetch_url(url).json()
        insert_request(url=url, res=res)
    else:
        print("cache-hit: %s" % fetch_code)

    return res


def fetch_url(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "x-nba-stats-origin": "stats",
        "x-nba-stats-token": "true",
        "Connection": "keep-alive",
        "Referer": "https://stats.nba.com/events/",
    }
    return httpx.get(url, headers=headers)
