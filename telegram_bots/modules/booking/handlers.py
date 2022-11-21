from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.booking.repository.api_repository.output import booking_repository_abstraction
from telegram_bots.modules.booking.repository.bookings_viewer_repository.output import booking_viewer_repository
from telegram_bots.modules.booking.messages import BookingMessages


messages = BookingMessages()


async def get_bookings(message: types.Message):
    bookings = booking_repository_abstraction.get_users_bookings(message.chat.id)
    if not booking_viewer_repository.read(message.chat.id):
        booking_viewer_repository.create(tg_id=message.chat.id, page_id=0)
        
    current_booking_id = booking_viewer_repository.read(message.chat.id)
    booking_message_text, buttons = messages.booking_view_menu_message(bookings, current_booking_id)
    
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    await message.answer(booking_message_text, reply_markup=keyboard)


def register_booking_handlers(dp: Dispatcher):
    dp.register_message_handler(get_bookings, commands="my_bookings")
    dp.register_callback_query_handler(messages.next_booking, text='next_booking')
    dp.register_callback_query_handler(messages.previous_booking, text='previous_booking')
