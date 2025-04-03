import pymysql
from config import DB_CONFIG

try:
    conn = pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG["port"]
    )
    print("Connection to database successful.")


except pymysql.MySQLError as err:
    print(f"Error connecting to database: {err}")
    conn.close()
