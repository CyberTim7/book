from environs import Env
from dataclasses import dataclass

@dataclass
class Tgbot:
    Bot_token:str

@dataclass
class Config:
    Bot:Tgbot

def load_config(path:str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(Bot=Tgbot(Bot_token=env("bot_token")))
    


