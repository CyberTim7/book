import mysql.connector
from configs.config import load_config

config = load_config(path="C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\configs\\.env")


def create_connect():
    connect = mysql.connector.connect(user=config.database.admin,
                          password=config.database.password,
                          host=config.database.host,
                          database=config.database.database)
    cursor = connect.cursor()   
    return connect, cursor

def terminate_connect(connect):
    connect.close()


def init_database():
    connect, cursor = create_connect()
    cursor.execute("DELETE FROM sql_now;")
    connect.commit()
    terminate_connect(connect)