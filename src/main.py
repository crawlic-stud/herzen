from aiogram import executor, Dispatcher

async def send_update(users, bot):
    for user in users:
        # await bot.send_message()
        pass


if __name__ == '__main__':
    import config
    import handlers
    
    async def on_startup(dispatcher: Dispatcher, *args, **kwargs):
        bot = dispatcher.bot
        send_id = "sent1"
        sent = config.database.ref.get().get("sent1")
        # test_users = [str(config.ADMIN_ID)]
        users = config.database.get_all_users().keys()
        if not sent:
            for user in users:
                try:
                    await bot.send_message(user, 
                        f"<b>Привет подпичники!</b>\n\n"
                        f"Не знаю пользуетесь вы еще этим ботом или нет, но я сделал обновление!\n\n"
                        f"Теперь по команде /date вылазит календарик, где можно натыкать расписание на любой день 🎉\n\n"
                        f"На этом пока что всё)"
                        f"\nЕсли хотите какие-то еще фичи, можете писать <a href='https://t.me/crawlic'>мне.</a>",
                        disable_web_page_preview=True
                        )
                except Exception as _:
                    continue
        config.database.ref.child(send_id).set(True)

    executor.start_polling(config.dp, skip_updates=True, on_startup=on_startup)
