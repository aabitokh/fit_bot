from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from db.db import exersices, exersices_for_muscle_group
from logger.logger import get_logger

logger_keyboards = get_logger()


def get_exc_markup(muscle_group: str) -> InlineKeyboardMarkup:
    logger_keyboards.info(f'создается клавиатура с выбором упражнений для {muscle_group}')

    kp_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    width = 1 
    for key in exersices_for_muscle_group[muscle_group].keys():
        buttons.append(InlineKeyboardButton(text=key, callback_data= exersices_for_muscle_group[muscle_group][key]))

    buttons.append(InlineKeyboardButton(text = LEXICON_RU['another_muscle_group'],
                                         callback_data = 'choose_muscle_group'))

    kp_builder.row(*buttons, width=width)
    #in the end just return markup
    return kp_builder.as_markup()

def continiue_training_markp():

    logger_keyboards.info(f'создается клавиатура с продолжением тренировки')
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU['continiue_training'],
            callback_data='continiue_training'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['finish'],
            callback_data='finish'
        ),
        InlineKeyboardButton(
            text=LEXICON_RU['choose_muscle_group'],
            callback_data='choose_muscle_group'
        ),
        width=1
    )
    return kb_builder.as_markup()
