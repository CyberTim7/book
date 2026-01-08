from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicons.lexicon_RU import lexicon_RU


button_yes = InlineKeyboardButton(text=lexicon_RU["yes"], callback_data="button_yes_click")
button_no = InlineKeyboardButton(text=lexicon_RU["no"], callback_data="button_no_click")

keyboard_yes_no = InlineKeyboardMarkup(inline_keyboard=[[button_yes], [button_no]])


button_next = InlineKeyboardButton(text=lexicon_RU["button_next"], callback_data="button_next_click")
button_down = InlineKeyboardButton(text=lexicon_RU["button_down"], callback_data="button_down_click")

keyboard_book = InlineKeyboardMarkup(inline_keyboard=[[button_down], [button_next]])