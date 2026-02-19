from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicons.lexicon_RU import lexicon_RU


def keyboard_yes_no(book_path):
    book_name = book_path.split("\\")[-1]
    button_yes = InlineKeyboardButton(text=lexicon_RU["yes"], callback_data=f"button_yes_click_{book_name}")
    button_no = InlineKeyboardButton(text=lexicon_RU["no"], callback_data="button_no_click")

    keyboard_yes_no = InlineKeyboardMarkup(inline_keyboard=[[button_yes], [button_no]])

    return keyboard_yes_no

def button_next_down(book_path):
    book_name = book_path.split("\\")[-1]
    button_next = InlineKeyboardButton(text=lexicon_RU["button_next"], callback_data=f"button_next_click_{book_name}")
    button_down = InlineKeyboardButton(text=lexicon_RU["button_down"], callback_data=f"button_down_click_{book_name}")

    keyboard_book = InlineKeyboardMarkup(inline_keyboard=[[button_down], [button_next]])
    return keyboard_book

