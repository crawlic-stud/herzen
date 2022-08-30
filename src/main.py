from aiogram import executor


if __name__ == '__main__':
    import config
    import handlers.basic_handlers
    import handlers.registration
    import handlers.schedule_handlers
    
    executor.start_polling(config.dp, skip_updates=True)
