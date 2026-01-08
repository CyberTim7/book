from lexicons.lexicon_RU import lexicon_RU
from services.main_service import get_book
from database.database import append_path
import PyPDF2
import json


async def download_file(message:Message) -> str:
    '''Скачивает файл в специальную папку'''
    await message.answer(lexicon_RU["loading"])
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    download_file = await message.bot.download_file(file.file_path)
    file_name = message.document.file_name
    file_path_new = f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{file_name}"
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
            return False


def pdf_file(path):
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def save_book(path_origin, book):
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




    
