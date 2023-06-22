from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from .states import ApplicationStates
from user.keyboards import inline


@dp.message_handler(state=ApplicationStates.MAIN_STATE)
async def text_msg(message: Message, state: FSMContext):
	await message.answer(f"Your application has been successfully sent", reply_markup=inline.menu())
	await state.finish()
