from aiogram import executor

    
if __name__ == '__main__':
    import config
    import handlers.basic_handlers
    import handlers.registration
    executor.start_polling(config.dp, skip_updates=True)
