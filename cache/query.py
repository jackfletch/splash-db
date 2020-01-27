from . import db
from .schema import Request


def get_cached_request(url):
    r = Request(database=db).get(url=url)
    return r.response
