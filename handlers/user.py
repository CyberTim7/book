from aiogram import Router, F
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicons.lexicon_RU import lexicon_RU
from database.database import append_db
from services.downloads_service import processed_file, SQL_NOW, SQL_NOW_DEL, get_path_book
from services.user_services import open_file, next_click, down_click, get_path_book_then, get_page
from keyboards.keyboards import keyboard_yes_no, button_next_down
from services.directory_services import checking_books, delete_user_book
from filters.filters import filter_code1, filter_code2, filter_button_yes, filter_button_next, filter_button_down
from services.database_services import delete_book_from_sql
import asyncio
import logging

logger = logging.getLogger(__name__)
user_router = Router()



@user_router.message(Command(commands="start"))
async def start_command(message:Message, state:FSMContext):
    append_db(user_id=message.from_user.id)  
    await message.answer(lexicon_RU["start"])

@user_router.message(Command(commands="help"))
async def help_command(message:Message):
    await message.answer(lexicon_RU["help"])

@user_router.message(F.content_type == ContentType.DOCUMENT)
async def doc_answer(message:Message, state:FSMContext):
    SQL_NOW_DEL(message)
    book_path = await processed_file(message)
    my_keyboard_yes_no = keyboard_yes_no(book_path)
    if book_path:
        await message.answer(lexicon_RU["processed"], reply_markup=my_keyboard_yes_no)
        await SQL_NOW(message, book_path)
        


@user_router.callback_query(filter_button_yes())
async def answer_yes(callback:CallbackQuery, state:FSMContext): 
    await callback.answer(lexicon_RU["loading"]) 
    book_name = str(callback.data)[17:]
    book_path = f'C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{callback.from_user.id}\\'+ book_name
    if book_path:
        await open_file(book_path, callback)
    else:
        await callback.message.edit_text(lexicon_RU["error_callback"])

        
            
@user_router.callback_query(filter_button_next())
async def next_page(callback:CallbackQuery, state:FSMContext):
    await callback.answer(lexicon_RU["loading"])
    book_name = str(callback.data)[18:]
    print(book_name)
    book_path = f'C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{callback.from_user.id}\\'+ book_name
    if book_path:  
        print(callback.data)
        await next_click(book_path, callback)
    else:
        await callback.message.edit_text(lexicon_RU["error_callback"])


@user_router.callback_query(filter_button_down())
async def down_page(callback:CallbackQuery, state:FSMContext):
    await callback.answer(lexicon_RU["loading"])
    book_name = str(callback.data)[18:]
    book_path = f'C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\database\\users_books\\{callback.from_user.id}\\'+ book_name
    if book_path:   
        await down_click(book_path, callback)
    else:
        await callback.message.edit_text(lexicon_RU["error_callback"])
        
@user_router.callback_query(F.data == "button_no_click")
async def answer_no(callback:CallbackQuery):
    await callback.answer(lexicon_RU["loading"]) 
    await callback.message.edit_text(text=lexicon_RU["button_no_click"])


@user_router.message(Command(commands="my_books"))
async def book_list(message:Message, state:FSMContext):
    user_books_keyboard = checking_books(str(message.from_user.id), code="1")
    if user_books_keyboard:
        SQL_NOW_DEL(message)
        await message.answer(lexicon_RU["your_books"], reply_markup=user_books_keyboard)
    else:
        await message.answer(lexicon_RU["you_havent_books"])

            
@user_router.callback_query(filter_code1())
async def print_book(callback:CallbackQuery, state:FSMContext):
    await callback.answer(lexicon_RU["loading"])
    book_path = get_path_book_then(callback)
    if book_path:
        page_real = get_page(callback)   
        await open_file(book_path, callback, page=page_real)
        await SQL_NOW(callback, book_path)
    else:
        await callback.message.edit_text(lexicon_RU["no_file"])

@user_router.message(Command(commands="delete_my_book"))
async def book_list_copy(message:Message, state:FSMContext):
    user_books_keyboard = checking_books(str(message.from_user.id), code="2")
    if user_books_keyboard:
        SQL_NOW_DEL(message)
        await message.answer(lexicon_RU["change_your_books"], reply_markup=user_books_keyboard)
    else:
        await message.answer(lexicon_RU["you_havent_books"])

@user_router.callback_query(filter_code2())
async def delete_book(callback:CallbackQuery, state:FSMContext):
    await callback.answer(lexicon_RU["loading"])
    try:
        delete_user_book(callback)
        delete_book_from_sql(callback)
        user_books_keyboard = checking_books(user_id=callback.from_user.id, code="2")
        if user_books_keyboard:
            await callback.message.edit_text(lexicon_RU["deleted_book"], reply_markup=user_books_keyboard)
        else:
            await callback.message.edit_text(lexicon_RU["you_havent_books"])
    except FileNotFoundError:
        await callback.message.edit_text(lexicon_RU["no_file"])





        