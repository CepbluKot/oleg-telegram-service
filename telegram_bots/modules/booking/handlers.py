from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.booking.repository.api_repository.output import booking_repository_abstraction
from telegram_bots.modules.booking.repository.bookings_viewer_repository.output import booking_viewer_repository
from telegram_bots.modules.booking.messages import BookingMessages
from telegram_bots.modules.booking.data_structures import BookingMenu
from telegram_bots.bots import bot


test_user_id = 99999
messages = BookingMessages()


async def get_bookings(message: types.Message):
    bookings = await booking_repository_abstraction.get_users_bookings(test_user_id)
  
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


def register_booking_handlers(dp: Dispatcher):
    dp.register_message_handler(get_bookings, commands="my_bookings")
    dp.register_callback_query_handler(messages.next_booking, text='next_booking')
    dp.register_callback_query_handler(messages.previous_booking, text='previous_booking')
    dp.register_callback_query_handler(messages.close_booking_view_menu, text='close_booking_view_menu')
    dp.register_callback_query_handler(messages.do_nothing, text='do_nothing')
