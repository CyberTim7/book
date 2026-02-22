from environs import Env
from dataclasses import dataclass


@dataclass
class Tgbot:
    Bot_token:str


@dataclass
class MySql:
    password:str
    admin:str
    host:str
    database:str

@dataclass
class Admin:
    admins:set

@dataclass
class Config:
    Bot:Tgbot
    database:MySql
    admin_lst:Admin


def load_config(path:str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(Bot=Tgbot(Bot_token=env("bot_token")),
                  database=MySql(password=env("password"),
                                 admin=env("admin"),
                                 host=env("host"),
                                 database=env("database")),
                  admin_lst=Admin(admins=env("admins")))


    


