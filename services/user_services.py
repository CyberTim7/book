import json
from keyboards.keyboards import keyboard_book
from lexicons.lexicon_RU import lexicon_RU
import os
from database.database_init import connect, cursor, config
from aiogram.exceptions import TelegramBadRequest


async def open_file(book_path, callback:CallbackQuery, page="1"):
    '''Отправляет пользователю страницу книги'''
    with open(book_path, "r+", errors='replace', encoding="utf-8") as file:
        book = json.load(file)
        key = book.get(page)
        if key == None and int(page) != 0:
            await callback.message.edit_text(lexicon_RU["end_file"], reply_markup=keyboard_book)
        elif key == None and int(page) == 0:
            await callback.message.edit_text(lexicon_RU["begin_file"], reply_markup=keyboard_book)
        else:
            await callback.message.edit_text(text=book[page], reply_markup=keyboard_book)
            await callback.answer()



async def next_click(book_path, callback:CallbackQuery):
    '''Обрабатывает нажатие кнопки следующей страницы'''
    user_id = callback.from_user.id
    with open(book_path, "r", encoding="utf-8") as file:
        book = json.load(file)  
    sql_select = """SELECT page FROM book WHERE user_id = %s"""
    cursor.execute(sql_select, (user_id,))
    next_page = cursor.fetchone()[0] + 1
    
    try:
        await callback.message.edit_text(book[str(next_page)], reply_markup=keyboard_book)
        sql_select = """UPDATE book SET page = %s  WHERE user_id = %s"""
        cursor.execute(sql_select, (next_page, user_id))
    except KeyError:
        try:
            await callback.message.edit_text(lexicon_RU["end_file"], reply_markup=keyboard_book)
            sql_select = """UPDATE book SET page = %s  WHERE user_id = %s"""
            cursor.execute(sql_select, (next_page, user_id))
            
        except TelegramBadRequest:
            pass
    
        

async def down_click(book_path, callback:CallbackQuery):
    '''Обрабатывает нажатие кнопки предыдущей страницы'''
    user_id = callback.from_user.id
    with open(book_path, "r", encoding="utf-8") as file:
        book = json.load(file)  
    sql_select = """SELECT page FROM book WHERE user_id = %s"""
    cursor.execute(sql_select, (user_id,))
    down_page = cursor.fetchone()[0] - 1
    try:
        await callback.message.edit_text(book[str(down_page)], reply_markup=keyboard_book)
        sql_select = """UPDATE book SET page = %s  WHERE user_id = %s"""
        cursor.execute(sql_select, (down_page, user_id))
    except KeyError:
        try:
            await callback.message.edit_text(lexicon_RU["begin_file"], reply_markup=keyboard_book)
            sql_select = """UPDATE book SET page = %s  WHERE user_id = %s"""
            cursor.execute(sql_select, (down_page, user_id))
        except TelegramBadRequest:
            pass


def get_path_book_then(callback:CallbackQuery):
    '''Получает путь к книге пользователя если она есть'''
    user_id = str(callback.from_user.id)
    book_name = str(callback.data).split("_")[-2]
    book_path = f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}\\{book_name}"
    os.chdir(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{int(user_id)}")
    if os.path.exists(f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{int(user_id)}\\{book_name}"):
        return book_path
    else:
        return False

def get_page(callback):
    '''Получает страницу книги из базы данных'''
    user_id = str(callback.from_user.id)
    book_name = str(callback.data).split("_")[-2]
    book_path = f"C:/Users/Lena/Desktop/github proects/book_bot/database/users_books/{user_id}/{book_name}"
    sql_select = """SELECT page FROM book WHERE user_id = %s AND path = %s"""
    cursor.execute(sql_select, (user_id, book_path))
    page = cursor.fetchone()[0]

    return page

