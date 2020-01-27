from . import db
from .schema import Request

if __name__ == "__main__":
    Request.create_table()
