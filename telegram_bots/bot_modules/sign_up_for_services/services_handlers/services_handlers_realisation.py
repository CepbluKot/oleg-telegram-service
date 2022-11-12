import asyncio
from email import message
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_modules.sign_up_for_services.input_output_realisations import services_abs


chosen_params_storage = {}


class ChooseServiceHandlers:
    class ChooseServiceFsm(StatesGroup):
        "FSM для выбора услуги и даты ее предоставления"
        choose_service_name = State()
        choose_service_week = State()
        choose_service_day = State()


    async def choose_service_name(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем имя услуги"
        markup = ReplyKeyboardMarkup(one_time_keyboard=True)

        services = services_abs.get_all_services()
        for service_id in services:
            markup.add(KeyboardButton(services[service_id].service_name))

        
        await message.reply("Выберите услугу из списка", reply_markup=markup)
        await self.ChooseServiceFsm.choose_service_name.set()

    async def choose_service_week(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем неделю предоставления услуги"
       
        service_name = message.text
        chosen_params_storage[message.chat.id] = service_name

        await state.update_data(service_name=service_name)
        service_id = services_abs.get_service_id_by_name(service_name=service_name)
        await state.update_data(service_id=service_id)

        

        markup = ReplyKeyboardMarkup(one_time_keyboard=True)

        for data in services_abs.get_service_weeks(service_id=service_id):
            markup.add(KeyboardButton(data))

        await self.ChooseServiceFsm.choose_service_week.set()
        await message.reply(
            "Выберите неделю предоставления услуги", reply_markup=markup
        )

    async def choose_service_day(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем день предоставления услуги"
        service_week = message.text

        fsm_data = await state.get_data()

        service_name = fsm_data["service_name"]


        await state.update_data(service_week=service_week)

        fsm_data = await state.get_data()

        markup = ReplyKeyboardMarkup(one_time_keyboard=True)

        for data in services_abs.get_service_days(service_id=fsm_data["service_id"]):
            markup.add(KeyboardButton(data))

        await self.ChooseServiceFsm.choose_service_day.set()
        await message.reply("Выберите день предоставления услуги", reply_markup=markup)

    async def choose_service_final(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) генерируем окончательную инфу об услуге"
        service_day = message.text


        fsm_data = await state.get_data()
        service_week = fsm_data["service_week"]
        service_name = fsm_data["service_name"]
        service_id = fsm_data["service_id"]



        services_abs.send_chosen_service_data(
            service_id=service_id,
            service_week=service_week,
            service_day=service_day,
            user_id=message.chat.id,
        )

        await message.reply(
            "Выбранная услуга: \n"
            + " Название: "
            + str(service_name)
            + " Неделя: "
            + service_week
            + " День: "
            + str(service_day)
        , reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


    def choose_service_name_checker(self, message: types.Message):
        if services_abs.get_service_id_by_name(service_name=message.text):
            return False
        return True


    def choose_service_week_checker(self, message: types.Message):
        service_id = services_abs.get_service_id_by_name(service_name=chosen_params_storage[message.chat.id])
        if service_id:
            if message.text in services_abs.get_service_weeks(service_id):

                return False
        return True


    def choose_service_day_checker(self, message: types.Message):
        service_id = services_abs.get_service_id_by_name(service_name=chosen_params_storage[message.chat.id])
        if service_id:
            if message.text in services_abs.get_service_days(service_id):
                return False
        return True


    async def choose_service_name_error(self, message: types.Message, state: FSMContext):
        await message.reply('выберите название услуги из списка')

    async def choose_service_week_error(self, message: types.Message, state: FSMContext):
        await message.reply('выберите неделю услуги из списка')

    async def choose_service_day_error(self, message: types.Message, state: FSMContext):
        await message.reply('выберите день услуги из списка')


    def services_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.choose_service_name, commands="sign_up_for_service", state="*"
        )

        dp.register_message_handler(
            self.choose_service_name_error, lambda msg: self.choose_service_name_checker(msg), state=self.ChooseServiceFsm.choose_service_name, 
        )

        dp.register_message_handler(
            self.choose_service_week_error, lambda msg: self.choose_service_week_checker(msg), state=self.ChooseServiceFsm.choose_service_week, 
        )

        dp.register_message_handler(
            self.choose_service_day_error, lambda msg: self.choose_service_day_checker(msg), state=self.ChooseServiceFsm.choose_service_day, 
        )

        dp.register_message_handler(
            self.choose_service_week, state=self.ChooseServiceFsm.choose_service_name, 
        )
        dp.register_message_handler(
            self.choose_service_day, state=self.ChooseServiceFsm.choose_service_week
        )
        dp.register_message_handler(
            self.choose_service_final, state=self.ChooseServiceFsm.choose_service_day
        )
