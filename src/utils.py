from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_inline_keyboard(data):
    """Creates inline keyboard for list with item's index as callback_data"""
    btns = [InlineKeyboardButton(item, callback_data=i) for i, item in enumerate(data)]
    inline_kb = InlineKeyboardMarkup()
    [inline_kb.add(btn) for btn in btns]
    return inline_kb


async def send_schedule(message, texts):
    """Sends schedule for all message's texts"""
    [await message.answer(text) for text in texts]
