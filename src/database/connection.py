import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

#use connection pooling to handle concurrent requests cleanly
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="traffic_pool",
    pool_size=5,
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", 3306)),
    database=os.getenv("DB_NAME", "traffic_safety"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
)

def get_db():
    conn = db_pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()