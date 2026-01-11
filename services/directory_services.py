import os
from keyboards.keyboard_books import main_builder


def checking_books(user_id):
    os.chdir(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}")
    user_books = os.listdir()
    real_books = []
    for books in user_books:
        if books.split(".")[-1] != "json":
            real_books.append(books)
    keyboard1 = main_builder(real_books, user_id)
    return keyboard1