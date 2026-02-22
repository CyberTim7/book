import os
from keyboards.keyboard_books import main_builder
import logging
from aiogram.types import Message, CallbackQuery
logger = logging.getLogger(__name__)


def checking_books(user_id, code):
    path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{user_id}"
    os.chdir(path)
    user_books = os.listdir()
    real_books = []
    for books in user_books:
        if books.split(".")[-1] != "json":
            real_books.append(books)
    if real_books == []:
        return False
    else:
        keyboard1 = main_builder(real_books, user_id, code)
        return keyboard1

def delete_user_book(callback):
    lst = str(callback.data).split("_")
    user_id = callback.from_user.id
    book_name_json = lst[1]
    index = lst[1].rfind(".")
    book_name_pdf = lst[1][:index + 1] + "pdf"
    path = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{user_id}"
    os.chdir(path)
    os.remove(f"{path}\\{book_name_json}")
    os.remove(f"{path}\\{book_name_pdf}")