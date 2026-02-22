from database.database_init import create_connect, terminate_connect
import os
from aiogram.types import Message, CallbackQuery

def delete_book_from_sql(callback:CallbackQuery):
    connect, cursor = create_connect()
    sql_select = '''DELETE FROM book WHERE user_id = %s and path = %s'''
    user_id = callback.from_user.id
    lst = str(callback.data).split("_")
    book_name_json = lst[1]
    path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{user_id}\\{book_name_json}"
    path = path.replace("\\", "/")
    cursor.execute(sql_select, (user_id, path))
    connect.commit()
    terminate_connect(connect)

def get_book_id(book_path:str, message:Message):
    connect, cursor = create_connect()
    sql_query = '''SELECT book_id FROM book WHERE user_id = %s AND path = %s'''
    user_id = message.from_user.id
    book_path = book_path.replace("\\", "/")
    cursor.execute(sql_query, (user_id, book_path))
    book_id = cursor.fetchone()[0]
    terminate_connect(connect)
    return book_id


def get_book_path_from_book(book_id:int):
    connect, cursor = create_connect()
    sql_query = '''SELECT path FROM book WHERE book_id = %s'''
    cursor.execute(sql_query, (book_id,))
    path = cursor.fetchone()[0]
    terminate_connect(connect)
    return path

def get_user_acess(event:TelegramObject):
    user_id = event.from_user.id
    connect, cursor = create_connect()
    sql_query = '''SELECT 1 FROM user_acess WHERE user_id = %s LIMIT 1'''
    cursor.execute(sql_query, (user_id,))
    res = cursor.fetchone()
    if res:
        return False
    else:
        return True

    
