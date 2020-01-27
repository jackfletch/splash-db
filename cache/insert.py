from . import db
from .schema import Request


def insert_request(url: str, res: str):
    Request(database=db).insert(url=url, response=res).execute()
