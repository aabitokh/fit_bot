from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from keyboards.start_keyboard import create_start_keyboard, choose_muscle_group
from keyboards.traning_keyboards import get_exc_markup, continiue_training_markp
from logger import logger 
from models.training import Training 
from datetime import datetime 
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from db.db import exersices_for_muscle_group
from db.db import exersices, exc_list
from db.db_utils import add_trainig

logger = logger.get_logger()

class SetFSM(StatesGroup):
    muscle_group_trainig = State()
    set = State()


state_sets = SetFSM()
router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup= create_start_keyboard())

@router.callback_query(F.data == 'start_training', StateFilter(default_state))
async def start_training(callback: CallbackQuery, state: FSMContext):
    
    logger.info('start training was pressed')

    #собираем данные из контекста и добавляем их обратно
    data = await state.get_data()
    training_data = data.get('training', {})
    training_data['start_training'] = str(datetime.now())
    await state.update_data(training=training_data)

    await callback.message.edit_text(
            text=LEXICON_RU['choose_muscle_group'],
            reply_markup=choose_muscle_group(), 
        )
    await callback.answer()

@router.callback_query(F.data == 'cancel')
async def cancel_training(callback: CallbackQuery):
    #TODO: save context if exists
    await callback.message.answer(
        text=f'Окей, тогда увидимся в следующий раз! Если захочешь еще потренироваться, то просто жмякни /start'
    )

@router.callback_query(F.data.in_(exersices.values()), StateFilter(default_state))
async def add_muscle_group(callback: CallbackQuery, state: FSMContext):
    
    logger.info(f"выбрана группа мышц {callback.data}")

    data = await state.get_data()
    training_data = data.get('training', {})

    # Проверяем, существует ли ключ 'muscle_group' в training_data
    #TODO: вот этот ключ будто лучше уже при внесении подходов добавить, а пока менять current_muscle group 
    if 'muscle_group' not in training_data:
        training_data['muscle_group'] = {}
    # Добавляем новую группу мышц, если ее еще нет
    if callback.data not in training_data['muscle_group']:
        training_data['muscle_group'][callback.data] = {}

    
    await state.update_data(training=training_data)
    await state.update_data(current_muscle_group=callback.data)
    
    await callback.message.answer(
            text=f'✅ окей, тренируемся, выбирай упражнение для этой группы мышц!',
            reply_markup= get_exc_markup(callback.data)
        )
    await callback.answer()

@router.callback_query(F.data.in_(exc_list))
async def choose_hell(callback: CallbackQuery, state: FSMContext):
    #TODO: здесь надо бы внести возможность cancel на внесение сделать с удалением текущей группы мышц, если не тренировали
    await state.set_state(SetFSM.muscle_group_trainig)
    logger.info('бот переведен в режим внесения тренировки определенной группы мышц')


    data = await state.get_data()
    training_data = data.get('training', {})
    current_muscle_group = data.get('current_muscle_group')
    #выбранное упражнение для muscle group
    training_data['muscle_group'][current_muscle_group][callback.data] = []
    
    await state.update_data(training=training_data)
    await state.update_data(current_exercise=callback.data)

    await callback.message.answer(text='Давай запишем подходы, просто пришли их одной строкой с таким паттерном: |вес повторы, | ')
    await callback.answer()
    
    await state.set_state(SetFSM.set)
    logger.info('установлено состояние на внесение данных о подходе')


@router.message(StateFilter(SetFSM.set))
async def first_set(message:Message,  state: FSMContext):
    
    data = await state.get_data()
    training_data = data.get('training', {})
    current_muscle_group = data.get('current_muscle_group')
    current_exc = data.get('current_exercise') 
    logger.info(f"вносим подходы для {current_exc}")
    training_data['muscle_group'][current_muscle_group][current_exc].append(message.text)
    
    logger.info(f'текущая тренировка выглядит так: {training_data}')

    await state.set_state(default_state)
    await message.answer(text=f'Внесенно {message.text} для {current_exc}, что делаем дальше?', 
                         reply_markup=continiue_training_markp())

@router.callback_query(F.data == 'continiue_training', StateFilter(default_state))
async def continiue_training(callback: CallbackQuery, state: FSMContext, ):
    
    data = await state.get_data()
    training_data = data.get('training', {})
    current_muscle_group = data.get('current_muscle_group')


    logger.info(f'продолжаем тренировать {current_muscle_group}')
    
    await callback.message.answer( 
        text=f'🏋🏻 Выбирай новое упражнение для {current_muscle_group}', 
        reply_markup= get_exc_markup(current_muscle_group)
    )
    await callback.answer()

@router.callback_query(F.data == 'choose_muscle_group', StateFilter(default_state))
async def change_mg(callback: CallbackQuery, state: FSMContext, ):
    
    data = await state.get_data()
    training_data = data.get('training', {})
    current_muscle_group = data.get('current_muscle_group')

    logger.info(f'меняем текущую группу мышц с {current_muscle_group}')
    
    await callback.message.edit_text(
            text=LEXICON_RU['choose_muscle_group'],
            reply_markup=choose_muscle_group(), 
        )

    await callback.answer()

@router.callback_query(F.data == 'finish', StateFilter(default_state))
async def finish_training(callback: CallbackQuery,  state: FSMContext):
    
    logger.info("Завершается тренировка")
    data = await state.get_data()
    training_data = data.get('training', {})

    logger.info(f"Данные для внесения {training_data}")

    t = Training(data = training_data)
    add_trainig(t)

    await state.update_data(training={})
    await state.update_data(current_muscle_group='')

    await callback.message.answer(
        text=f'Окей, тогда увидимся в следующий раз! Если захочешь еще потренироваться, то просто жмякни /start'
        )