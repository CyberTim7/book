from aiogram import Bot, Dispatcher
from configs.config import load_config
from handlers.user import user_router
from setcommands import setcommands
import os
import asyncio
from database.database_init import create_connect, init_database, terminate_connect, config
import logging


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s in module %(module)s in line %(lineno)d'
)

bot_token = config.Bot.Bot_token

bot = Bot(token=bot_token)
dp = Dispatcher()
dp.workflow_data.update()


dp.include_router(user_router)

async def main():
    logger.warning("Start polling...")
    try:
        connect, cursor = create_connect()
        init_database()
        terminate_connect(connect)
        dp.startup.register(setcommands)
        await asyncio.wait_for(dp.start_polling(bot), timeout=500)
    
    except TimeoutError:
        logger.warning("Опрос сервера завершен")
        connect.close()


if __name__ == "__main__":
    asyncio.run(main())






