import json
from keyboards.keyboards import keyboard_book
from lexicons.lexicon_RU import lexicon_RU


async def open_file(book_path, callback:CallbackQuery):
    with open(book_path, "r+", errors='replace', encoding="utf-8") as file:
        book = json.load(file)
    await callback.message.edit_text(text=book["1"], reply_markup=keyboard_book)
    await callback.answer()



async def next_click(book_path, callback:CallbackQuery):
    user_id = callback.from_user.id
    with open(book_path, "r", encoding="utf-8") as file:
        book = json.load(file)  
    with open("C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\SQL.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        next_page = (data[str(user_id)][book_path.split('\\')[-1]]["page"]) + 1
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
        down_page = (data[str(user_id)][book_path.split('\\')[-1]]["page"]) - 1 
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