import asyncio
import logging
import dotenv
from aiogram import Bot, Dispatcher
import os 
from config_data.config import load_config, Config
from handlers.user_handlers import router as user_router
from logger import logger
from aiogram.fsm.storage.memory import MemoryStorage
from models.db_models import Training_session
from db.main_db import init_app
from aiogram.types import BotCommand

# Инициализируем логгер

logger = logger.get_logger()

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command='/start',
            description= 'Начнем тренировку 🔥'
        ) 
    ]
    await bot.set_my_commands(main_menu_commands)

# Функция конфигурирования и запуска бота
async def main():
    logger.info('Starting bot')
    config: Config = load_config()
    bot = Bot(
        token=config.tg_bot.token,
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(user_router)
    await set_main_menu(bot)

    # Пропускаем накпившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    init_app()
    asyncio.run(main())