from lexicons.lexicon_RU import lexicon_RU
from services.main_service import get_book
from database.database import append_path
import PyPDF2
import json
from database.database_init import create_connect, terminate_connect
import os
from aiogram.types import Message, CallbackQuery


async def download_file(message:Message) -> str:
    '''Скачивает файл в специальную папку'''
    await message.answer(lexicon_RU["loading"])
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    download_file = await message.bot.download_file(file.file_path)
    file_name = message.document.file_name
    file_path_new = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\database\\users_books\\{message.from_user.id}\\{file_name}"
    result_file = open(file_path_new, "wb")
    result_file.write(download_file.read())
    result_file.close()
    index = file.file_path.rfind(".")
    if file.file_path[index:] == ".pdf":
        text = pdf_file(file_path_new)
        await message.answer(lexicon_RU["down file"])
        return text, file_path_new
    else:
        await message.answer(lexicon_RU["error_format"])
        
        

async def processed_file(message:Message):
    '''Использует функцию скачивания файла и создает итоговую книгу''' 
    if message.document.mime_type != "application/pdf":
        await message.answer(lexicon_RU["error_format"])
    else:  
        text, file_path = await download_file(message)
        book = get_book(text)
        if book:
            book_path = save_book(file_path, book)
            user_id = message.from_user.id
            append_path(user_id, book_path)
            return book_path
        else:
            await message.answer(lexicon_RU["error_format"])
        


def pdf_file(path):
    '''Извлекает текст из pdf'''
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def save_book(path_origin, book):
    '''Сохраняет книгу в json'''
    index = path_origin.rfind(".")
    new_file_path = path_origin[:index + 1] + "json"
    for keys in book:
        if book[keys] == "..":
            del book[keys]
            break

    with open(new_file_path, "w", encoding="utf-8") as file:
        file.seek(0)
        file.write(json.dumps(book, ensure_ascii=False))
    return new_file_path




async def get_path_book(callback:CallbackQuery):
    '''Получает путь к книге пользователя'''
    connect, cursor = create_connect()
    sql_select = """SELECT book_path FROM sql_now WHERE user_id = %s"""
    try:
        cursor.execute(sql_select, (callback.from_user.id,))
        try:
            book_path = cursor.fetchone()[0]
            return book_path
        except TypeError:
            return False
    except mysql.connector.errors.InternalError:
        return False
    terminate_connect(connect)
    

            
    

    
