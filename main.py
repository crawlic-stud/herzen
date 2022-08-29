from aiogram import executor

    
if __name__ == '__main__':
    import bot
    import handlers.basic_handlers
    import handlers.registration
    executor.start_polling(bot.dp, skip_updates=True)
