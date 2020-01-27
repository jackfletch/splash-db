import os
from pathlib import Path

from dotenv import load_dotenv
from peewee import PostgresqlDatabase

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE = os.getenv("DB_DATABASE")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")

db = PostgresqlDatabase(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
