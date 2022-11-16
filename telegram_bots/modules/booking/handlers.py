from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.booking.repository.repository_abstraction import BookingRepositoryAbstraction
from telegram_bots.modules.booking.repository.repository_realisation import BookingRepositoryRealisationDatabase


booking_repository_realisation_database = BookingRepositoryRealisationDatabase()
booking_repository_abstraction = BookingRepositoryAbstraction(booking_repository_realisation_database)


async def get_bookings(message: types.Message):
    full_message = ''
    bookings = booking_repository_abstraction.get_users_bookings(message.chat.id)
    for booking in bookings:
        full_message += str(booking)

    message.reply(full_message)

def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(get_bookings, commands="my_bookings")
