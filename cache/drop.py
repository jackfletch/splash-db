from . import db
from .schema import Request

if __name__ == "__main__":
    db.connect(reuse_if_open=True)
    db.drop_tables([Request])
