from aiogram import executor


if __name__ == '__main__':
    import config
    import handlers.spam_handler
    import handlers.error_handlers
    import handlers.basic_handlers
    import handlers.registration_handlers
    import handlers.schedule_handlers
    
    executor.start_polling(config.dp, skip_updates=True)
