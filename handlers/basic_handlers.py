from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import dp, bot




@dp.message_handler(commands=["start"])
async def send_start(message):
    btns = [InlineKeyboardButton(str(i) * 30, callback_data=str(i) * 10) for i in range(50)]
    inline_kb = InlineKeyboardMarkup().add()
    [inline_kb.add(btn) for btn in btns]

    await message.answer("start", reply_markup=inline_kb)


@dp.callback_query_handler()
async def test_query(query, state):
    await bot.answer_callback_query(query.id, f"выбрано {query.data}")


@dp.message_handler(commands=["help"])
async def send_help(message):
    await message.answer("help")


@dp.message_handler(commands=["schedule"])
async def send_schedule(message):
    # TODO: checks if message.user.id in database, if so - send them schedule
    # TODO: make event chaining to add user to database
    await message.answer("schedule")