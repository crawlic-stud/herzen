import asyncio

from aiogram import types

import config


MESSAGE = f"""Йоу всем привет, на связи админ бота 

Предлагаю вам заценить другой мой проект - <a href="https://t.me/motya_blog">Блог Моти</a> 

Это как ChatGPT, только в телеграме и от лица маленького тушканчика, который еще совсем маленький и только начинает познавать мир 🌍🥺
Тушканчик не простой, он умеет не только писать посты, но и рисовать по вашему запросу все что угодно🥰

В общем, если вам интересно - переходите, задавайте вопросы 💖

<span class="tg-spoiler">(спойлер: он даже умеет решать домашку)</span>"""


async def send_update():
    bot = config.bot
    send_id = "sent2"
    sent = config.database.ref.get().get(send_id)
    users = config.database.get_all_users().keys()
    if not sent:
        for user in users:
            try:
                await bot.send_message(user, MESSAGE)
                print(f"sent to {user}")
            except Exception as e:
                print(e)
                continue
    print("done sending")
    config.database.ref.child(send_id).set(True)


if __name__ == "__main__":
    asyncio.run(send_update())
