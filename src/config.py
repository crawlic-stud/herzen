from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

from database import Database


API_TOKEN = ""

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()   
dp = Dispatcher(bot, storage=storage)

database = Database(
    database_url="https://herzenbot-default-rtdb.europe-west1.firebasedatabase.app/", 
    key_path="src/firebase_key.json")


# commands (to botfather)
"""
today - Расписание на сегодня
tomorrow - Расписание на завтра
week - Расписание на неделю
date - Расписание на определенную дату
register - Зарегистрироваться в боте
cancel - Отменить регистрацию
help - Помощь 
start - Приветственное сообщение
"""