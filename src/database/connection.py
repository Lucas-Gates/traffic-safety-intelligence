import os
import time
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        retries = 10
        while retries > 0:
            try:
                _pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="traffic_pool",
                    pool_size=5,
                    host=os.getenv("DB_HOST", "127.0.0.1"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    database=os.getenv("DB_NAME", "traffic_safety"),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", ""),
                )
                break
            except mysql.connector.Error as err:
                retries -= 1
                if retries == 0:
                    raise err
                print("Waiting for database to become available... retrying in 3s")
                time.sleep(3)
    return _pool

def get_db():
    pool = get_pool()
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()