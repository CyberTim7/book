from aiogram import Bot, Dispatcher
from configs.config import load_config
from handlers.user import user_router
import os
import asyncio

config = load_config(path="C:\\Users\\Lena\\Desktop\\github proects\\book_bot\\configs\\.env")
bot_token = config.Bot.Bot_token

bot = Bot(token=bot_token)
dp = Dispatcher()
dp.include_router(user_router)

async def main():
    print('Начинаю опрос сервера')
    try:
        await asyncio.wait_for(dp.start_polling(bot), timeout=200)
    
    except TimeoutError:
        print('Опрос сервера завершен')

if __name__ == "__main__":
    asyncio.run(main())






