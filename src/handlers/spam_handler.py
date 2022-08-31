from utils import get_random_emoji


async def on_spam(message, *args, **kwargs):
    rate = kwargs.get("rate")
    if rate:
        await message.answer(f"⚠️ Интервал между одной и той же командой должен быть <b>не менее {rate} сек</b>\nПожалуйста, не спамьте.")
    else: 
        await message.answer(f"⚠️ Пожалуйста, не спамьте!")
