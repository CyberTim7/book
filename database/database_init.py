import mysql.connector
from configs.config import load_config
import os


path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\configs\\.env"
config = load_config(path_config)


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