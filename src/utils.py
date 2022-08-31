from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests

import random

def create_inline_list(data):
    """Creates inline keyboard for list with item's index as callback_data"""
    btns = [InlineKeyboardButton(item, callback_data=i) for i, item in enumerate(data)]
    inline_kb = InlineKeyboardMarkup()
    [inline_kb.add(btn) for btn in btns]
    return inline_kb


def create_inline_table(data, num_cols=2):
    """Creates inline table for list with item's index as callback_data"""
    btns = [InlineKeyboardButton(item, callback_data=i) for i, item in enumerate(data)]
    inline_kb = InlineKeyboardMarkup()
    for i in range(len(btns)//num_cols+1):
        lower_limit = i*num_cols
        upper_limit = (i+1)*num_cols
        inline_kb.row(*btns[lower_limit:upper_limit])
    return inline_kb


async def send_schedule(message, texts):
    """Sends schedule for all message's texts"""
    [await message.answer(text) for text in texts]


def get_random_emoji():
    emoji_on_error = random.choice("🖖 ✌️ 🐣".split(" "))
    req = requests.get("https://ranmoji.herokuapp.com/emojis/api/v.1.0/")
    if req.status_code == 200:
        return req.json().get("emoji", emoji_on_error)
    return emoji_on_error

if __name__ == "__main__":
    print(get_random_emoji())
