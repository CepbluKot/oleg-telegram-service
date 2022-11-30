from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.booking.repository.api_repository.output import booking_repository_abstraction
from telegram_bots.modules.booking.repository.bookings_deleter_repository.output import bookigs_deleter_repository
from telegram_bots.modules.booking.repository.bookings_viewer_repository.output import booking_viewer_repository
from telegram_bots.modules.booking.messages import BookingMessages
from telegram_bots.modules.booking.data_structures import BookingMenu
from telegram_bots.bots import bot


# test_user_id = 1
messages = BookingMessages()


async def get_bookings(message: types.Message):
    bookings = await booking_repository_abstraction.get_users_bookings(message.chat.id)

    
    if not bookings.errors.has_error:
        if len(bookings.data):
            user_boking_viewer = booking_viewer_repository.read(message.chat.id)

            if not user_boking_viewer:
                user_boking_viewer = BookingMenu(page_id=0, current_message_id=-1)
                booking_viewer_repository.create(tg_id=message.chat.id, data=user_boking_viewer)
                cur_page_id = 0
            else:
                await bot.delete_message(message.chat.id, user_boking_viewer.current_message_id)
                cur_page_id = user_boking_viewer.page_id

            

            booking_message_text, buttons = messages.booking_view_menu_message(bookings, user_boking_viewer.page_id)
            
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)
            
            answer_msg = await message.answer(booking_message_text, reply_markup=keyboard)
            booking_viewer_repository.update(tg_id=message.chat.id, data=BookingMenu(page_id=cur_page_id, current_message_id=answer_msg.message_id))

        else:
            await message.answer('У вас нет актуальных записей')

    else:
        if bookings.errors.timeout:
            await message.answer('Ошибка подключения к сервису, пожалуйста, повторите позже')

        else:
            await message.answer('Возникла непредвиденная ошибка, пожалуйста, повторите позже')


async def cancel_booking_command_handler(message: types.Message):
    parsed = message.text.split('_')[1]
    bookigs_deleter_repository.create(message.chat.id, parsed)
    buttons = [
            types.InlineKeyboardButton(
                text="Да", callback_data="approve_booking_delete"),
            
            types.InlineKeyboardButton(
                text="Нет", callback_data="deny_booking_delete"),
        ]

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await message.answer('Вы уверены, что хотите отменить запись?', reply_markup=keyboard)


async def approve_booking_delete(call: types.CallbackQuery):
    response = await booking_repository_abstraction.delete_booking(bookigs_deleter_repository.read(call.message.chat.id))
    
    if not response.errors.has_error:
        await call.message.answer('Запись отменена')
    
    else:
        if response.errors.timeout:
            await call.message.answer('Ошибка подключения к сервису, пожалуйста, повторите позже')

        elif response.errors.booking_doesnt_exist:
            await call.message.answer('Данной записи не существует')

        else:
            await call.message.answer('Возникла непредвиденная ошибка, пожалуйста, повторите позже')


    bookigs_deleter_repository.delete(call.message.chat.id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    

async def deny_booking_delete(call: types.CallbackQuery):
    await call.message.answer('Окей, ничего не отменяем')
    bookigs_deleter_repository.delete(call.message.chat.id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_booking_handlers(dp: Dispatcher):
    dp.register_message_handler(get_bookings, commands="my_bookings")
    dp.register_message_handler(cancel_booking_command_handler, lambda message: message.text.startswith('/cancel_'))

    dp.register_callback_query_handler(messages.next_booking, text='next_booking')
    dp.register_callback_query_handler(messages.previous_booking, text='previous_booking')
    dp.register_callback_query_handler(messages.close_booking_view_menu, text='close_booking_view_menu')
    dp.register_callback_query_handler(messages.do_nothing, text='do_nothing')

    
    dp.register_callback_query_handler(approve_booking_delete, text='approve_booking_delete')
    dp.register_callback_query_handler(deny_booking_delete, text='deny_booking_delete')
