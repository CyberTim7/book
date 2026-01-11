from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def main_builder(button_list:list, user_id:str):
    result_keyboard = InlineKeyboardBuilder()
    for i in range(len(button_list)):
        button_name = InlineKeyboardButton(text=button_list[i], callback_data=user_id + "_" + str(*button_list[i].split(".")[:-1]) + ".json" + "_code:1")
        result_keyboard.row(button_name, width=1)
    return result_keyboard.as_markup()



