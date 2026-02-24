import os
from keyboards.keyboard_books import main_builder
import logging
from aiogram.types import Message, CallbackQuery
from database.database_init import create_connect, terminate_connect
from services.database_services import get_book_path_from_book


logger = logging.getLogger(__name__)


def checking_books(user_id, code):
    connect, cursor = create_connect()
    path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{user_id}"
    path = path.replace("\\", "/")
    os.chdir(path)
    user_books = os.listdir()
    real_books = []
    real_names_books = []
    
    sql_query = '''SELECT book_id FROM book WHERE path = %s'''
    for books in user_books:
        if books.split(".")[-1] != "json":
            book_name = books[:books.rfind(".")] + ".json"
            path = f"{path}/{book_name}"
            logger.debug(f"Путь к которому обратилась бд: {path}")
            cursor.execute(sql_query, (path,))
            book_id = cursor.fetchone()[0]
            real_books.append(str(book_id))
            real_names_books.append(books)
    if real_books == []:
        return False
    else:
        logger.debug(f"Список id книг: {real_books}")
        keyboard1 = main_builder(real_names_books, real_books, user_id, code)
        return keyboard1

def delete_user_book(callback):
    lst = str(callback.data).split(".")
    logger.warning(f'{callback.data}')
    user_id = callback.from_user.id
    book_id = lst[0]
    logger.debug(f"BOOK ID {book_id}")
    path = get_book_path_from_book(book_id)
    logger.debug(f"ПУТЬ json {path}")
    book_path_pdf = path[:path.rfind(".")] + ".pdf"
    logger.warning(f'ПУТЬ pdf {book_path_pdf}')
    os.remove(f"{path}")
    os.remove(f"{book_path_pdf}")