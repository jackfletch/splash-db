from .constants import DATABASE, HOST, PASSWORD, USER, db
from .create import create_tables
from .drop import drop_tables
from .insert import init_seasons, init_teams


def init_db():
    init_seasons()
    init_teams()
