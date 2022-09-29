from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        # add removers

        await message.answer("Cancelled.", reply_markup=types.ReplyKeyboardRemove())
        return

    await state.finish()
    await message.answer("Cancelled.", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_cancel(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, commands="cancel", state="*")
