from aiogram import executor, Dispatcher

import config
import handlers


if __name__ == '__main__':
    executor.start_polling(config.dp, skip_updates=True)
