import json
import os
from database.database_init import create_connect, terminate_connect
from configs.config import load_config
import mysql.connector





def append_db(user_id) -> None:
    '''Эта функция добавляет пользователя в базу данных, если его там нет а также создает персональную папку для него'''
    connect, cursor = create_connect()
    try:
        cursor.execute("INSERT INTO user"
                       "(user_id)"
                       "VALUES ({});".format(user_id))
        connect.commit()
        path = os.path.dirname(os.path.abspath(__file__)) + "\\users_books"
        os.chdir(path)
        os.mkdir(str(user_id))
    
    
    except mysql.connector.errors.IntegrityError:
        pass
    terminate_connect(connect)
    

def append_path(user_id, path):
    connect, cursor = create_connect()
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
    terminate_connect(connect)
    
    


    
