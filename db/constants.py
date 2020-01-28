import os

from dotenv import load_dotenv
from peewee import PostgresqlDatabase

load_dotenv()

DATABASE = os.getenv("DB_DATABASE")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")

db = PostgresqlDatabase(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
