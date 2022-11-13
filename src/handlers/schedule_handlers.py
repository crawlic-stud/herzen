from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from dataclasses import asdict
from datetime import datetime

from config import dp, database, CALENDAR 
from herzen.get_schedule import get_date_schedule_link, get_today_link, get_tomorrow_link, get_full_schedule_link, construct_one_day_link
from herzen.get_schedule import get_table_from_link
from utils import send_schedule
from messages import UPDATE_REGISTRATION_MESSAGE, NEED_REGISTER_MESSAGE
from handlers.spam_handler import on_spam
from simple_calendar import SimpleCalendar, calendar_callback


THROTTLE_RATE = 10


async def validate_user(message, on_success):
    await types.ChatActions.typing()
    user = database.get_user(message.chat.id)
    if not user:
        await message.answer(NEED_REGISTER_MESSAGE)

    elif database.user_has_empty_fields(user):
        await message.answer(UPDATE_REGISTRATION_MESSAGE)
    
    else:
        # if everything is fine
        await on_success(user.data)


@dp.message_handler(commands=["today"])
@dp.throttled(on_spam, rate=THROTTLE_RATE)
async def send_today(message):
    async def on_success(user_data):
        date_link = get_date_schedule_link(**asdict(user_data))
        schedule_link = get_today_link(date_link)
        await send_schedule(message, get_table_from_link(schedule_link))
    await validate_user(message, on_success=on_success)


@dp.message_handler(commands=["tomorrow"])
@dp.throttled(on_spam, rate=THROTTLE_RATE)
async def send_tomorrow(message):
    async def on_success(user_data):
        date_link = get_date_schedule_link(**asdict(user_data))
        schedule_link = get_tomorrow_link(date_link)
        await send_schedule(message, get_table_from_link(schedule_link))
    await validate_user(message, on_success=on_success)


@dp.message_handler(commands=["week"])
@dp.throttled(on_spam, rate=THROTTLE_RATE)
async def send_week(message):
    async def on_success(user_data):
        schedule_link = get_full_schedule_link(**asdict(user_data))
        await send_schedule(message, get_table_from_link(schedule_link))
    await validate_user(message, on_success=on_success)


# form to ask date
class DateForm(StatesGroup):
    ask = State()  


# one line date command
@dp.message_handler(lambda message: get_valid_date(message.text.split()[-1]))
@dp.throttled(on_spam, rate=THROTTLE_RATE)
async def send_date(message):
    async def on_success(user_data):
        date = get_valid_date(message.text.split()[-1])
        date_link = get_date_schedule_link(**asdict(user_data))
        schedule_link = construct_one_day_link(date_link, date)
        await send_schedule(message, get_table_from_link(schedule_link))
    await validate_user(message, on_success=on_success)


# date command which asks to enter date
@dp.message_handler(commands=["date"], state="*")
# @dp.throttled(on_spam, rate=THROTTLE_RATE)
async def send_date(message: types.Message, state: State):
    async def on_success(user_data):
        async with state.proxy() as data:
            data["user_data"] = user_data
            await DateForm.ask.set()
            await message.answer("Выберите дату или введите в формате дд.мм.гггг:", reply_markup=await SimpleCalendar().start_calendar())
    await validate_user(message, on_success=on_success)


@dp.callback_query_handler(calendar_callback.filter(), state="*")
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    
    async def on_success(user_data):
        async with state.proxy() as data:
            data["user_data"] = user_data
            date_link = get_date_schedule_link(**asdict(data["user_data"]))
            schedule_link = construct_one_day_link(date_link, date)
            await send_schedule(callback_query.message, get_table_from_link(schedule_link))
    
    if selected:
        await callback_query.message.edit_text("Секундочку...")
        await validate_user(callback_query.message, on_success)
        await state.finish()


def get_valid_date(date_str):
    try:
        date = datetime.strptime(date_str.replace("/", ".").replace("-", "."), "%d.%m.%Y")
        return date
    except ValueError:
        return False


@dp.message_handler(state=DateForm.ask)
async def process_date(message, state):
    date = get_valid_date(message.text)
    if date:
        async with state.proxy() as data:
            date_link = get_date_schedule_link(**asdict(data["user_data"]))
            schedule_link = construct_one_day_link(date_link, date)
            await send_schedule(message, get_table_from_link(schedule_link))
    else:
        await message.answer("Неверный формат даты.")
    
    await state.finish()
