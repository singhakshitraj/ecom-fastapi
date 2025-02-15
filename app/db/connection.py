import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
def get_db_connection():
    load_dotenv()
    conn = psycopg2.connect(
        database = os.environ.get('DATABASE'),
        user = os.environ.get('USER'),
        password = os.environ.get('PASSWORD'),
        host = os.environ.get('HOST'),
        port = os.environ.get('PORT'),
        cursor_factory=RealDictCursor
    )
    return conn;