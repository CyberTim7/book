from aiogram.filters import BaseFilter

class filter_code1(BaseFilter):
    async def __call__(self, callback):
        if str(callback.data).split("_")[-1] == "code:1":
            return True
        else:
            print(str(callback.data).split("_")[-1])
            return False
            