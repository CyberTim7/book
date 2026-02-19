import os
from keyboards.keyboard_books import main_builder
import logging

logger = logging.getLogger(__name__)


def checking_books(user_id, code):
    os.chdir(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}")
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
    
    os.chdir(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}")
    os.remove(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}\\{book_name_json}")
    os.remove(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}\\{book_name_pdf}")