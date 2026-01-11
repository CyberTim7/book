import json
from keyboards.keyboards import keyboard_book
from lexicons.lexicon_RU import lexicon_RU


async def open_file(book_path, callback:CallbackQuery, page="1"):
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
    user_id = callback.from_user.id
    with open(book_path, "r", encoding="utf-8") as file:
        book = json.load(file)  
    with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        try:
            next_page = (data[str(user_id)][book_path.split('\\')[-1]]["page"]) + 1
        except KeyError:
            pass
    try:
        await callback.message.edit_text(book[str(next_page)], reply_markup=keyboard_book)
        with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "w", encoding="utf-8") as file:
            data[str(user_id)][book_path.split('\\')[-1]]["page"] = next_page
            json.dump(data, file, indent=2, ensure_ascii=False)
    except KeyError:
        await callback.message.edit_text(lexicon_RU["end_file"], reply_markup=keyboard_book)
        with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "w", encoding="utf-8") as file:
            data[str(user_id)][book_path.split('\\')[-1]]["page"] = next_page
            json.dump(data, file, indent=2, ensure_ascii=False)


async def down_click(book_path, callback:CallbackQuery):
    user_id = callback.from_user.id
    with open(book_path, "r", encoding="utf-8") as file:
        book = json.load(file)  
    with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        try:
            down_page = (data[str(user_id)][book_path.split('\\')[-1]]["page"]) - 1 
        except KeyError:
            pass
    

    try:
        await callback.message.edit_text(book[str(down_page)], reply_markup=keyboard_book)
        with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "w", encoding="utf-8") as file:
            data[str(user_id)][book_path.split('\\')[-1]]["page"] = down_page
            json.dump(data, file, indent=2, ensure_ascii=False)
    except KeyError:
        await callback.message.edit_text(lexicon_RU["begin_file"], reply_markup=keyboard_book)
        with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "w", encoding="utf-8") as file:
            data[str(user_id)][book_path.split('\\')[-1]]["page"] = down_page
            json.dump(data, file, indent=2, ensure_ascii=False)


def get_path_book_then(callback:CallbackQuery):
    user_id = str(callback.from_user.id)
    book_name = str(callback.data).split("_")[-2]
    book_path = f"C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{user_id}\\{book_name}"
    return book_path

def get_page(callback):
    user_id = str(callback.from_user.id)
    book_name = str(callback.data).split("_")[-2]
    with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        page = data[user_id][book_name]["page"]
    return page

