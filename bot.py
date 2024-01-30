import openai
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import handlers
from config import config


def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    openai.api_key = config.ai_token.get_secret_value()

    # Setup handlers
    handlers.setup_handlers(dp)

    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
