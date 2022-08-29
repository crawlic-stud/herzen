from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_inline_keyboard(data):
    btns = [InlineKeyboardButton(item, callback_data=i) for i, item in enumerate(data)]
    inline_kb = InlineKeyboardMarkup()
    [inline_kb.add(btn) for btn in btns]
    return inline_kb
