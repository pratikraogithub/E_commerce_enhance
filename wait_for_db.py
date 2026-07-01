# wait_for_db.py

import time
import psycopg2
from psycopg2 import OperationalError

DB_NAME = "ecommerce_db"
DB_USER = "ecommerce_user"
DB_PASSWORD = "strongpassword"
DB_HOST = "db"
DB_PORT = "5432"

while True:
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.close()
        print("✅ Database is ready!")
        break
    except OperationalError:
        print("⏳ Waiting for database...")
        time.sleep(2)
