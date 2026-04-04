import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

DB_USER_NAME = os.environ.get("DB_USER_NAME")
DB_PWD = os.environ.get("DB_PWD")

def get_connection():
    return psycopg2.connect(
        dbname="twitter_automation_bot",
        user=DB_USER_NAME,
        password=DB_PWD,
        host="localhost",
        port="5432"
    )