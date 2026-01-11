from aiogram.types import BotCommand

async def setcommands(bot):
    commands = [
        BotCommand(command="/start",
                   description="Запуск бота"),
        BotCommand(command="/help",
                   description="Список доступных команд"),
        BotCommand(command="/my_books",
                   description="Список ваших книг")]

               
    await bot.set_my_commands(commands)