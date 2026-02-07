import mysql.connector
from configs.config import load_config


config = load_config(path="C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\configs\\.env")

connect = mysql.connector.connect(user=config.database.admin,
                          password=config.database.password,
                          host=config.database.host,
                          database=config.database.database)
cursor = connect.cursor()   

def init_database():
    cursor.execute("DELETE FROM sql_now;")
    connect.commit()