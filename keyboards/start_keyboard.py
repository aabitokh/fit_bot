from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from db.db import exersices
from logger.logger import get_logger

logger = get_logger()

def create_start_keyboard(*args: int) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()
    #TODO Добавляем в конце "Редактировать"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['/start_training'],
            callback_data='start_training'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['/cancel'],
            callback_data='cancel'
        ),
        width=2
    )
    return kb_builder.as_markup()

def choose_muscle_group() -> InlineKeyboardMarkup:

    logger.info('создается клавиатура с выбором упражнений')

    kp_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    width = 1 
    for key in exersices.keys():
        buttons.append(InlineKeyboardButton(text=key, callback_data= exersices[key]))
    buttons.append(InlineKeyboardButton(text='Не, не хочу', callback_data='cancel'))
    kp_builder.row(*buttons, width=width)
    
    logger.info("отправлена клавиатура с группами мышц")

    return kp_builder.as_markup()
