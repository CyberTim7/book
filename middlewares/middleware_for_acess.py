from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from services.database_services import get_user_acess
from configs.config import load_config
import time
import logging
import os

logger = logging.getLogger(__name__)

path_config = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\configs\\.env"
config = load_config(path_config)
admin_lst = config.admin_lst.admins

class Middleware_for_acess(BaseMiddleware):
    
    def __init__(self):
        self.cashe = set()
        self.cashe_limit = 50
        self.time_start_cashe = time.monotonic()
        self.cashe_time = 50
    
    
    async def __call__(
        self,
        handler,
        event,
        data):
        user = event.from_user
        user_id = user.id
        user_name = user.first_name
        user_surname = user.last_name
        user_username = user.username
        if (str(user_id) in admin_lst) or (str(user_id) in self.cashe):
            pass
        
        elif get_user_acess(event):
            print(
                f"Несанкционированный доступ: id = {user_id},"
                f"\nname = {user_name},"
                f"\nsurname = {user_surname},"
                f"\ntg = {user_username}\n\n"
                ) 
            return
        
        else:
            if time.monotonic() - self.time_start_cashe <= self.cashe_time and len(self.cashe) < self.cashe_limit:
                self.cashe.add(str(user_id))
                
            elif len(self.cashe) >= self.cashe_limit:
                self.cashe.pop()
                self.cashe.add(str(user_id))
                
            else:
                self.cashe = set()
                self.cashe.add(str(user_id))
        
        result = await handler(event, data)
