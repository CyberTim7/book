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
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id BIGINT NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS book (book_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,"
                                                     "user_id BIGINT NOT NULL UNIQUE, FOREIGN KEY (user_id) REFERENCES user(user_id),"
                                                     "path VARCHAR(200) UNIQUE NOT NULL,"
                                                     "page INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user_access (user_id BIGINT NOT NULL,"
                                                           "full_name VARCHAR(100))")
    connect.commit()
    terminate_connect(connect)