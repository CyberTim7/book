from aiogram.filters import BaseFilter

class filter_code1(BaseFilter):
    async def __call__(self, callback):
        if str(callback.data).split("_")[-1] == "code:1":
            return True
        else:
            return False

class filter_code2(BaseFilter):
    async def __call__(self, callback):
        if str(callback.data).split("_")[-1] == "code:2":
            return True
        else:
            return False
            