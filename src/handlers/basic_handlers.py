from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import dp, bot




@dp.message_handler(commands=["start"])
async def send_start(message):
    await message.answer("start")


@dp.callback_query_handler()
async def test_query(query, state):
    await bot.answer_callback_query(query.id, f"выбрано {query.data}")


@dp.message_handler(commands=["help"])
async def send_help(message):
    await message.answer("help")