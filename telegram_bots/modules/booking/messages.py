import typing, math
from aiogram import types
from telegram_bots.modules.booking.data_structures import Booking, BookingMenu
from telegram_bots.modules.booking.repository.bookings_viewer_repository.output import booking_viewer_repository
from telegram_bots.modules.booking.repository.api_repository.output import booking_repository_abstraction
from telegram_bots.bots import bot


# test_usr_tg_id = 99999
bookings_per_page = 5

# to-do : show 5 bookings at once


class BookingMessages:
    def booking_view_menu_message(self, bookings: typing.List[Booking], current_begin_page_id: int):
        message_text = ''

        current_booking_id = current_begin_page_id * bookings_per_page
        last_booking_id_on_page = current_booking_id + bookings_per_page - 1

        container_lenth = len(bookings)
        if container_lenth - current_booking_id - 1 <= bookings_per_page:
            last_booking_id_on_page = container_lenth - 1


        while current_booking_id <= last_booking_id_on_page:
            current_booking = bookings[current_booking_id]

            service_name = current_booking.subscription_service.name_service
            begin_day = current_booking.booking_day_start
            end_day = current_booking.booking_day_end
            begin_time = current_booking.booking_time_start
            end_time = current_booking.booking_time_end
            comment = current_booking.comment
            booking_id = current_booking.id_booking

            message_text += f'\nМероприятие {service_name}\n'
            message_text += f'С {begin_day} {begin_time} до {end_day} {end_time}\n'
            message_text += f'Комментарий: {comment}\n'
            message_text += f'id: {booking_id}\n'
            message_text += f'Отменить запись - /cancel_{current_booking_id}\n'
            current_booking_id += 1

        num_of_pages = math.ceil(len(bookings) / bookings_per_page)


        buttons = [
            types.InlineKeyboardButton(
                text="<", callback_data="previous_booking"),
            types.InlineKeyboardButton(
                text=f"{current_begin_page_id+1} / {num_of_pages}", callback_data="do_nothing"),
            types.InlineKeyboardButton(text=">", callback_data="next_booking"),
            types.InlineKeyboardButton(
                text="Закрыть", callback_data="close_booking_view_menu"),
        ]

        return message_text, buttons

    async def previous_booking(self, call: types.CallbackQuery):
        await call.answer()

        current_booking_viewer_state = booking_viewer_repository.read(call.message.chat.id)
        current_page_id = current_booking_viewer_state.page_id

        if current_page_id > 0:
            current_page_id -= 1
            all_bookings = await booking_repository_abstraction.get_users_bookings(call.message.chat.id)
            message_text, buttons = self.booking_view_menu_message(
                bookings=all_bookings, current_begin_page_id=current_page_id)

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await bot.delete_message(call.message.chat.id, current_booking_viewer_state.current_message_id)
            answer_msg = await call.message.answer(message_text, reply_markup=keyboard)
            booking_viewer_repository.update(tg_id=call.message.chat.id, data=BookingMenu(
                page_id=current_page_id, current_message_id=answer_msg.message_id))

    async def next_booking(self, call: types.CallbackQuery):
        await call.answer()
        current_booking_viewer_state = booking_viewer_repository.read(
            call.message.chat.id)
        current_page_id = current_booking_viewer_state.page_id

        all_bookings = await booking_repository_abstraction.get_users_bookings(call.message.chat.id)

        if current_page_id + 1 < math.ceil(len(all_bookings) / bookings_per_page):
            current_page_id += 1

            message_text, buttons = self.booking_view_menu_message(
                bookings=all_bookings, current_begin_page_id=current_page_id)

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await bot.delete_message(call.message.chat.id, current_booking_viewer_state.current_message_id)

            answer_msg = await call.message.answer(message_text, reply_markup=keyboard)
            booking_viewer_repository.update(tg_id=call.message.chat.id, data=BookingMenu(
                page_id=current_page_id, current_message_id=answer_msg.message_id))


    async def close_booking_view_menu(self, call: types.CallbackQuery):
        await call.answer()
        current_booking_viewer_state = booking_viewer_repository.read(
            call.message.chat.id)
        await bot.delete_message(call.message.chat.id, current_booking_viewer_state.current_message_id)
        booking_viewer_repository.delete(call.message.chat.id)

    async def do_nothing(self, call: types.CallbackQuery):
        await call.answer()
