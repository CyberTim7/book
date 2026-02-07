from aiogram import Router, F
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.filters import Command
from lexicons.lexicon_RU import lexicon_RU
from database.database import append_db
from services.downloads_service import processed_file, SQL_NOW, SQL_NOW_DEL, get_path_book
from services.user_services import open_file, next_click, down_click, get_path_book_then, get_page
from keyboards.keyboards import keyboard_yes_no, keyboard_book
from services.directory_services import checking_books
from filters.filters import filter_code1, filter_code2
import asyncio


user_router = Router()
lock = asyncio.Lock()


@user_router.message(Command(commands="start"))
async def start_command(message:Message):
    append_db(user_id=message.from_user.id)  
    await message.answer(lexicon_RU["start"])

@user_router.message(Command(commands="help"))
async def help_command(message:Message):
    await message.answer(lexicon_RU["help"])

@user_router.message(F.content_type == ContentType.DOCUMENT)
async def doc_answer(message:Message):
    async with lock:
        book_path = await processed_file(message)
        if book_path:
            await message.answer(lexicon_RU["processed"], reply_markup=keyboard_yes_no)
            await SQL_NOW(message, book_path)
        


@user_router.callback_query(F.data == "button_yes_click")
async def answer_yes(callback:CallbackQuery): 
    async with lock: 
        await callback.answer(lexicon_RU["loading"]) 
        book_path = await get_path_book(callback)
        if book_path:
            await open_file(book_path, callback)
        else:
            await callback.message.edit_text(lexicon_RU["error_callback"])

        
            
@user_router.callback_query(F.data == "button_next_click")
async def next_page(callback:CallbackQuery):
    async with lock: 
        await callback.answer(lexicon_RU["loading"])
        book_path = await get_path_book(callback)  
        if book_path:  
            await next_click(book_path, callback)
        else:
            await callback.message.edit_text(lexicon_RU["error_callback"])

@user_router.callback_query(F.data == "button_down_click")
async def down_page(callback:CallbackQuery):
    async with lock: 
        await callback.answer(lexicon_RU["loading"])
        book_path = await get_path_book(callback)
        if book_path:   
            await down_click(book_path, callback)
        else:
            await callback.message.edit_text(lexicon_RU["error_callback"])
        
@user_router.callback_query(F.data == "button_no_click")
async def answer_no(callback:CallbackQuery):
    await callback.answer(lexicon_RU["loading"]) 
    await callback.message.edit_text(text=lexicon_RU["button_no_click"])


@user_router.message(Command(commands="my_books"))
async def book_list(message:Message):
    async with lock:
        user_books_keyboard = checking_books(str(message.from_user.id))
        if user_books_keyboard:
            SQL_NOW_DEL(message)
            await message.answer(lexicon_RU["your_books"], reply_markup=user_books_keyboard)
        else:
            await message.answer(lexicon_RU["you_havent_books"])

            



@user_router.callback_query(filter_code1())
async def print_book(callback:CallbackQuery):
    async with lock:
        await callback.answer(lexicon_RU["loading"])
        book_path = get_path_book_then(callback)
        if book_path:
            page_real = get_page(callback)   
            await open_file(book_path, callback, page=page_real)
            await SQL_NOW(callback, book_path)
        else:
            await callback.message.edit_text(lexicon_RU["no_file"])

@user_router.message(Command(commands="delete_my_book"))
async def book_list_copy(message:Message):
    async with lock:
        user_books_keyboard = checking_books(str(message.from_user.id))
        if user_books_keyboard:
            SQL_NOW_DEL(message)
            await message.answer(lexicon_RU["change_your_books"], reply_markup=user_books_keyboard)
        else:
            await message.answer(lexicon_RU["you_havent_books"])


        