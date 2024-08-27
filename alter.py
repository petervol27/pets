import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("db_host"),
        database=os.getenv("db_name"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        port=os.getenv("db_port"),
    )
    return conn


def alter_table_add_animal():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE pets ADD COLUMN animal VARCHAR(20);")
    conn.commit()
    conn.close()


alter_table_add_animal()
