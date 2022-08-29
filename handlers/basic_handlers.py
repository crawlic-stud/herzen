from bot import dp


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