import json
import os
import mysql.connector
from configs.config import load_config


config = load_config(path="C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\configs\\.env")
connect = mysql.connector.connect(user=config.database.admin,
                          password=config.database.password,
                          host=config.database.host,
                          database=config.database.database)

cursor = connect.cursor()


def append_db(user_id) -> None:
    '''Эта функция добавляет пользователя в базу данных, если его там нет а также создает персональную папку для него'''
    try:
        anti_acess(user_id) 
        cursor.execute("INSERT INTO user"
                       "(user_id)"
                       "VALUES ({});".format(user_id))
        connect.commit()
        os.chdir("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books")
        os.mkdir(str(user_id))
    
    
    except mysql.connector.errors.IntegrityError:
        pass
    

def append_path(user_id, path):
    '''Создает базовый словарь пользователя хотя бы с одной книгой'''
    index_end = path.rfind(".")
    index_st = path.rfind("\\") + 1
    book_name = path[index_st:index_end]
    path = path.replace("\\", "/")

    sql_query = """
    INSERT INTO book (user_id, path, page)
    VALUES (%s, %s, 1)
    """
    
    # Передаем параметры вторым аргументом execute()
    try:
        cursor.execute(sql_query, (user_id, path))
        connect.commit()
    except mysql.connector.errors.IntegrityError:
        pass
    
    

def anti_acess(user_id):
    'До создания антивируса функция блокирует пользователей с чужим id'
    if user_id != 6027578907 and user_id != 1898019149 and user_id != 5215143463:
       raise ValueError(f"Несанкционированный доступ: id = {user_id}")

