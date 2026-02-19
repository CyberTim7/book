from aiogram.filters import BaseFilter

class filter_code1(BaseFilter): #код команды my_books
    async def __call__(self, callback):
        if str(callback.data).split("_")[-1] == "code:1":
            return True
        else:
            return False

class filter_code2(BaseFilter): #код команды delete_my_book
    async def __call__(self, callback):
        if str(callback.data).split("_")[-1] == "code:2":
            return True
        else:
            return False

class filter_button_yes(BaseFilter):
    async def __call__(self, callback):
        if "button_yes_click" in str(callback.data)[0:16]:
            return True
        else:
            return False


class filter_button_next(BaseFilter):
    async def __call__(self, callback):
        if "button_next_click" in str(callback.data)[0:17]:
            return True
        else:
            return False

class filter_button_down(BaseFilter):
    async def __call__(self, callback):
        if "button_down_click" in str(callback.data)[0:17]:
            return True
        else:
            return False
            