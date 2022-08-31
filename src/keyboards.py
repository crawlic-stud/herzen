from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import DONATE_LINK


HELP = "Cписок команд"
HELP_DATA = "help"

ABOUT = "О разработчике"
ABOUT_DATA = "about"

START = "О боте"
START_DATA = "start"

REGISTER_DATA = "register"

START_KEYBOARD = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Начать работу с ботом!", callback_data=REGISTER_DATA)
).row(
    InlineKeyboardButton(HELP, callback_data=HELP_DATA),
    InlineKeyboardButton(ABOUT, callback_data=ABOUT_DATA)
)

HELP_KEYBOARD = InlineKeyboardMarkup().row(
    InlineKeyboardButton(ABOUT, callback_data=ABOUT_DATA),
    InlineKeyboardButton(START, callback_data=START_DATA),
)

ABOUT_KEYBOARD = InlineKeyboardMarkup().add(
    InlineKeyboardButton(HELP, callback_data=HELP_DATA),
    InlineKeyboardButton(START, callback_data=START_DATA),
    InlineKeyboardButton("Связаться со мной", url="https://t.me/crawlic"),
    InlineKeyboardButton("Мой Github", url="https://github.com/crawlic-stud"),
    InlineKeyboardButton("Поддержать проект", url=DONATE_LINK)
)

REGISTER_KEYBOARD = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Редактировать", callback_data=REGISTER_DATA)
)
