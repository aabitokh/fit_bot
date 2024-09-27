from dataclasses import dataclass

import os
import dotenv


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    dotenv.load_dotenv()
    BOT_TOKEN = os.getenv("TOKEN")
    ADMIN_ID = os.getenv("ADMIN_ID")
    return Config(
        tg_bot=TgBot(
            token=BOT_TOKEN,
            admin_ids=ADMIN_ID
        )
    )