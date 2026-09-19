import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
    )

def get_cursor():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    return conn, cursor