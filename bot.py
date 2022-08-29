import logging

from aiogram import Bot, Dispatcher, executor, types

from test import API_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_start(message):
    await message.answer("hi!")


@dp.message_handler(commands=["help"])
async def send_help(message):
    await message.answer("help")


@dp.message_handler(commands=["schedule"])
async def send_schedule(message):
    # TODO: checks if message.user.id in database, if so - send them schedule
    # TODO: make event chaining to add user to database
    await message.answer("schedule")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
