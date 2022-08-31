from aiogram.utils.exceptions import Throttled

from config import dp, bot
from messages import get_greeting, START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE
from keyboards import HELP_KEYBOARD, START_KEYBOARD, ABOUT_KEYBOARD, \
    START_DATA, HELP_DATA, ABOUT_DATA, REGISTER_DATA
from utils import get_random_emoji
from handlers.spam_handler import on_spam
from handlers.registration_handlers import start_register

@dp.message_handler(commands=["start"])
@dp.throttled(on_spam, rate=1)
async def send_start(message):
    await message.answer(get_greeting(message.from_user.first_name, get_random_emoji()) + START_MESSAGE,
        reply_markup=START_KEYBOARD,
        disable_web_page_preview=True)


@dp.message_handler(commands=["help"])
@dp.throttled(on_spam, rate=1)
async def send_help(message):
    await message.answer(HELP_MESSAGE,
        reply_markup=HELP_KEYBOARD,
        disable_web_page_preview=True)


@dp.message_handler(commands=["about"])
@dp.throttled(on_spam, rate=1)
async def send_about(message):
    await message.answer(ABOUT_MESSAGE,
        reply_markup=ABOUT_KEYBOARD,
        disable_web_page_preview=True)


@dp.callback_query_handler()
async def handle_inline_keyboard_input(query, state):
    if query.data == HELP_DATA:
        await query.message.edit_text(HELP_MESSAGE, reply_markup=HELP_KEYBOARD, disable_web_page_preview=True)
    elif query.data == ABOUT_DATA:
        await query.message.edit_text(ABOUT_MESSAGE, reply_markup=ABOUT_KEYBOARD, disable_web_page_preview=True)
    elif query.data == START_DATA:
        await query.message.edit_text(START_MESSAGE, reply_markup=START_KEYBOARD, disable_web_page_preview=True)
    elif query.data == REGISTER_DATA:
        await start_register(query.message, state)