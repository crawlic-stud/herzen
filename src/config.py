from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

from database import Database
from api_token import API_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()   
dp = Dispatcher(bot, storage=storage)

database = Database(
    database_url="https://herzenbot-default-rtdb.europe-west1.firebasedatabase.app/", 
    key_path="src/firebase_key.json")

DONATE_LINK = "https://www.tinkoff.ru/cf/1BhnB9qPA3j"
ADMIN_ID = 361944343

# commands (to botfather)
"""
today - Расписание на сегодня
tomorrow - Расписание на завтра
week - Расписание на неделю
date - Расписание на определенную дату
me - Информация о пользователе
register - Зарегистрироваться или поменять данные
cancel - Отменить регистрацию
help - Помощь 
start - Приветственное сообщение
about - Информация о разработчике
"""