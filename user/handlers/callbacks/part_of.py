from loader import dp
from aiogram.types import CallbackQuery
from user.keyboards import inline
from user.keyboards import reply
from aiogram.dispatcher import FSMContext
from user.filters.states import ApplicationStates
from user.utils import send_message_of_interest


@dp.callback_query_handler(lambda call: "price_of" == call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("Company information:\n\n\nCompany name:\n\n📍 Location:\n\n📲 Phone:\n\n!PRICE!\n\nChoose your next action ⤵️", 
		reply_markup=inline.choice_company())


@dp.callback_query_handler(lambda call: "to_delivery_method" == call.data)
async def to_delivery_method(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("Company information:\n\n\nCompany name:\n\n📍 Location:\n\n📲 Phone:\n\n!PRICE!\n\nChoose your next action ⤵️", 
		reply_markup=inline.delivery_method())


@dp.callback_query_handler(lambda call: "was_deliveried" in call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("We're glad you got it all!\nPlease rate the quality of service ❤️\nSEND NUMBERS FROM 1 TO 5 ⤵️", reply_markup=inline.mark_keyboard())


@dp.callback_query_handler(lambda call: "wasnt_deliveried" == call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("Can you please tell me what is the problem?", reply_markup=None)
	await ApplicationStates.MAIN_STATE.set()


@dp.callback_query_handler(lambda call: "mark" == call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("Thank you", reply_markup=None)