import asyncio
from aiogram import types, bot
from bots import prepod_bot, student_bot
from bot_modules.settings.input_output_repositories import settings_repository_abs


async def prepod_delete_previous_messages(
    last_message_to_delete: types.Message,
    num_of_messages_to_delete: int,
    timer: bool = True,
):
    user_data = settings_repository_abs.get_user_settings(
        user_id=last_message_to_delete.chat.id
    )
    if user_data and user_data.message_delete_switch:
        if timer:
            await asyncio.sleep(user_data.message_delete_delay)

        current_delete_id = (
            last_message_to_delete.message_id - num_of_messages_to_delete
        )
        while current_delete_id != last_message_to_delete.message_id:

            await prepod_bot.delete_message(
                chat_id=last_message_to_delete.chat.id, message_id=current_delete_id
            )
            current_delete_id += 1
        await prepod_bot.delete_message(
            chat_id=last_message_to_delete.chat.id, message_id=current_delete_id
        )


async def student_delete_previous_messages(
    last_message_to_delete: types.Message,
    num_of_messages_to_delete: int,
    timer: bool = True,
):
    user_data = settings_repository_abs.get_user_settings(
        user_id=last_message_to_delete.chat.id
    )
    if user_data and user_data.message_delete_switch:
        if timer:
            await asyncio.sleep(user_data.message_delete_delay)
        current_delete_id = (
            last_message_to_delete.message_id - num_of_messages_to_delete + 1
        )
        while current_delete_id != last_message_to_delete.message_id:

            await student_bot.delete_message(
                chat_id=last_message_to_delete.chat.id, message_id=current_delete_id
            )
            current_delete_id += 1

        await student_bot.delete_message(
            chat_id=last_message_to_delete.chat.id, message_id=current_delete_id
        )


async def student_delete_previous_polls(
    last_message_to_delete: types.PollAnswer,
    num_of_messages_to_delete: int,
    timer: bool = True,
):
    user_data = settings_repository_abs.get_user_settings(
        user_id=last_message_to_delete.user.id
    )
    if user_data and user_data.message_delete_switch:
        if timer:
            await asyncio.sleep(user_data.message_delete_delay)
        current_delete_id = (
            int(last_message_to_delete.poll_id) - int(num_of_messages_to_delete) + 1
        )
        while str(current_delete_id) != str(last_message_to_delete.poll_id):

            await student_bot.delete_message(
                chat_id=last_message_to_delete.user.id, message_id=current_delete_id
            )
            current_delete_id += 1

        await student_bot.delete_message(
            chat_id=last_message_to_delete.user.id, message_id=current_delete_id
        )


async def student_delete_previous_calls(
    last_message_to_delete: types.CallbackQuery,
    num_of_messages_to_delete: int,
    timer: bool = True,
):
    user_data = settings_repository_abs.get_user_settings(
        user_id=last_message_to_delete.chat.id
    )
    if user_data and user_data.message_delete_switch:
        if timer:
            await asyncio.sleep(user_data.message_delete_delay)
        current_delete_id = (
            last_message_to_delete.message.message_id - num_of_messages_to_delete + 1
        )
        while current_delete_id != last_message_to_delete.message.message_id:

            await student_bot.delete_message(
                chat_id=last_message_to_delete.from_user.id,
                message_id=current_delete_id,
            )
            current_delete_id += 1

        await student_bot.delete_message(
            chat_id=last_message_to_delete.from_user.id, message_id=current_delete_id
        )
