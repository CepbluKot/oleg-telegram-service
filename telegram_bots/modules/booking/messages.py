import typing
from aiogram import types
from telegram_bots.modules.booking.data_structures import Booking, BookingMenu
from telegram_bots.modules.booking.repository.bookings_viewer_repository.output import booking_viewer_repository
from telegram_bots.modules.booking.repository.api_repository.output import booking_repository_abstraction
from telegram_bots.bots import bot


test_usr_id = 3


class BookingMessages:
    def booking_view_menu_message(self, bookings: typing.List[Booking], current_booking_id: int):
        message_text = ''
        current_booking = bookings[current_booking_id]

        service_name = current_booking.subscription_service.name_service
        begin_day = current_booking.booking_day_start
        end_day = current_booking.booking_day_end
        begin_time = current_booking.booking_time_start
        end_time = current_booking.booking_time_end
        comment = current_booking.comment

        message_text += f'Мероприятие {service_name}\n'
        message_text += f'С {begin_day} {begin_time} до {end_day} {end_time}\n'
        message_text += f'Комментарий: {comment}'

        bookings_lenth = len(bookings)

        buttons = [
                types.InlineKeyboardButton(text="<", callback_data="previous_booking"),
                types.InlineKeyboardButton(text=f"{current_booking_id+1} / {bookings_lenth}", callback_data="do_nothing"),
                types.InlineKeyboardButton(text=">", callback_data="next_booking"),
                types.InlineKeyboardButton(text="Закрыть", callback_data="close_booking_view_menu"),
            ]

        return message_text, buttons

    async def previous_booking(self, call: types.CallbackQuery):
        current_booking_viewer = booking_viewer_repository.read(call.message.chat.id)
        current_page_id = current_booking_viewer.page_id

        if current_page_id > 0:
            current_page_id -= 1
            all_bookings = await booking_repository_abstraction.get_users_bookings(test_usr_id)
            message_text, buttons = self.booking_view_menu_message(bookings=all_bookings, current_booking_id=current_page_id)

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await bot.delete_message(call.message.chat.id, current_booking_viewer.current_message_id)
            answer_msg = await call.message.answer(message_text, reply_markup=keyboard)
            booking_viewer_repository.update(tg_id=call.message.chat.id, data=BookingMenu(page_id=current_page_id, current_message_id=answer_msg.message_id))
  

    async def next_booking(self, call: types.CallbackQuery):
        current_booking_viewer = booking_viewer_repository.read(call.message.chat.id)
        current_page_id = current_booking_viewer.page_id

        all_bookings = await booking_repository_abstraction.get_users_bookings(test_usr_id)
        print('wtf', all_bookings)
        if current_page_id + 1 < len(all_bookings):
            
            current_page_id += 1
            
            message_text, buttons = self.booking_view_menu_message(bookings=all_bookings, current_booking_id=current_page_id)

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await bot.delete_message(call.message.chat.id, current_booking_viewer.current_message_id)
            answer_msg = await call.message.answer(message_text, reply_markup=keyboard)
            booking_viewer_repository.update(tg_id=call.message.chat.id, data=BookingMenu(page_id=current_page_id, current_message_id=answer_msg.message_id))
    

    def close_booking_view_menu(self):
        pass
