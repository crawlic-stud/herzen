from aiogram.utils.exceptions import RetryAfter

from config import bot, dp


@dp.errors_handler(exception=RetryAfter)
async def flood_error(update, error):
    try:
        chat_id = update["chat"]["id"]
        seconds = str(filter(lambda char: char.isdigit(), error))
        bot.send_message(chat_id, f"Вы спамили слишком много. Прежде чем отправить другую команду подождите {seconds} секунд :)")
    except Exception as e:
        pass
    finally:
        return True
