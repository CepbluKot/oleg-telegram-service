""" Система для выбора услуг"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bots_setting.bot_elements.getters.services_getters import get_all_services_names, get_service_days, get_service_weeks


class choose_service_fsm(StatesGroup):
    " FSM для выбора услуги и даты ее предоставления"
    choose_service_name = State()
    choose_service_week = State()
    choose_service_day = State()


async def choose_service_name(message: types.Message, state: FSMContext):
    " (choose_service_fsm) выбираем имя услуги"

    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for data in get_all_services_names():
        markup.add(KeyboardButton(data))

    await choose_service_fsm.choose_service_name.set()
    await message.reply('Выберите услугу из списка', reply_markup=markup)


async def choose_service_week(message: types.Message, state: FSMContext):
    " (choose_service_fsm) выбираем неделю предоставления услуги"
    service_name = message.text
    await state.update_data(service_name=service_name)
    
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)

    for data in get_service_weeks(service_name):
        markup.add(KeyboardButton(data))

    await choose_service_fsm.choose_service_week.set()
    await message.reply('Выберите неделю предоставления услуги', reply_markup=markup)


async def choose_service_day(message: types.Message, state: FSMContext):
    " (choose_service_fsm) выбираем день предоставления услуги"
    service_week = message.text
    await state.update_data(service_week=service_week)
    
    fsm_data = await state.get_data()
    service_name = fsm_data['service_name']
    
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    for data in get_service_days(service_name=service_name, service_week=service_week):
        markup.add(KeyboardButton(data))

    await choose_service_fsm.choose_service_day.set()
    await message.reply('Выберите день предоставления услуги', reply_markup=markup)


async def choose_service_final(message: types.Message, state: FSMContext):
    " (choose_service_fsm) генерируем окончательную инфу об услуге"
    service_day = message.text
    
    fsm_data = await state.get_data()
    service_week = fsm_data['service_week']
    service_name = fsm_data['service_name']
    
    await message.reply('Выбранная услуга: \n' + ' Название: ' + str(service_name) + ' Неделя: ' + service_week + ' День: ' + str(service_day))


def register_handler_services(dp: Dispatcher):
    dp.register_message_handler(choose_service_name, commands="select_service", state="*")
    dp.register_message_handler(choose_service_week, state=choose_service_fsm.choose_service_name)
    dp.register_message_handler(choose_service_day, state=choose_service_fsm.choose_service_week)
    dp.register_message_handler(choose_service_final, state=choose_service_fsm.choose_service_day)
