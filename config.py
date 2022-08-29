from ast import parse
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging


API_TOKEN = ""

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()   
dp = Dispatcher(bot, storage=storage)
