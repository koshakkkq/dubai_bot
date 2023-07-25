
from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from .states import AddressStates
from user.keyboards import inline

@dp.message_handler(state=AddressStates.ADDRESS_STATE)
async def text_msg(message: Message, state: FSMContext):
	await message.answer(f"Your address: {message.text}\n*purchase*\n\nthrough Stripe", reply_markup=inline.pay_btn())
	await state.finish()

