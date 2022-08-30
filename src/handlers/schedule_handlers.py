from aiogram.dispatcher.filters.state import State, StatesGroup

from dataclasses import asdict
from datetime import datetime

from config import dp, database 
from herzen.get_schedule import get_date_schedule_link, get_today_link, get_tomorrow_link, get_full_schedule_link, construct_one_day_link
from herzen.get_schedule import get_table_from_link
from utils import send_schedule
from messages import *


@dp.message_handler(commands=["today"])
async def send_today(message):
    user_data = database.get_user_data(message.from_id)
    if user_data:
        date_link = get_date_schedule_link(**asdict(user_data))
        schedule_link = get_today_link(date_link)
        await send_schedule(message, get_table_from_link(schedule_link))
    else:
        await message.answer(NEED_REGISTER_MESSAGE)


@dp.message_handler(commands=["tomorrow"])
async def send_tomorrow(message):
    user_data = database.get_user_data(message.from_id)
    if user_data:
        date_link = get_date_schedule_link(**asdict(user_data))
        schedule_link = get_tomorrow_link(date_link)
        await send_schedule(message, get_table_from_link(schedule_link))
    else:
        await message.answer(NEED_REGISTER_MESSAGE)


@dp.message_handler(commands=["week"])
async def send_week(message):
    user_data = database.get_user_data(message.from_id)
    if user_data:
        schedule_link = get_full_schedule_link(**asdict(user_data))
        await send_schedule(message, get_table_from_link(schedule_link))
    else:
        await message.answer(NEED_REGISTER_MESSAGE)


# form to ask date
class DateForm(StatesGroup):
    ask = State()  


@dp.message_handler(commands=["date"])
async def send_date(message, state):
    user_data = database.get_user_data(message.from_id)
    if user_data:
        async with state.proxy() as data:
            data["user_data"] = user_data
            await DateForm.ask.set()
            await message.answer("Введите дату в формате дд.мм.гггг:")
    else:
        await message.answer(NEED_REGISTER_MESSAGE)


@dp.message_handler(state=DateForm.ask)
async def process_date(message, state):
    date_str = message.text.replace("/", ".").replace("-", ".")
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y")
        async with state.proxy() as data:
            date_link = get_date_schedule_link(**asdict(data["user_data"]))
            schedule_link = construct_one_day_link(date_link, date)
            await send_schedule(message, get_table_from_link(schedule_link))
    except ValueError:
        await message.answer("Неверный формат даты.")
    
    await state.finish()