
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp
from .shop_menu import ShopMenuStates, shop_menu_callback
from shop.logic.registartion import *
import utils.decorators as decorators
import shop.messages
import shop.keyboards

class ShopCreationStates(StatesGroup):
	get_code = State()
	get_location = State()
	get_name = State()
	get_phone = State()
@dp.callback_query_handler(
	filters.Text(equals="register_store"),
	state="*",
)

@decorators.picked_language
async def shop_begin_registration(callback: types.CallbackQuery, state: FSMContext, language='eng'):
	await state.reset_data()
	status = await get_shop_member_status(callback.from_user.id)
	if status == 'member':
		await shop_menu_callback(callback, state)
		return
	if status == 'can_create_shop':
		await shop_registration_begin(callback, state, language)
		return

	msg = shop.messages.messages[language]['get_code']

	keyboard = shop.keyboards.keyboards[language]['to_client_menu']
	await state.set_state(ShopCreationStates.get_code.state)
	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()


@dp.message_handler(
	state = ShopCreationStates.get_code,
)
@decorators.picked_language
async def shop_get_code(message: types.Message, state: FSMContext, language='eng'):
	await state.reset_data()
	code = message.text

	status = await is_code_correct(message.from_user.id, code)

	msg = shop.messages.messages[language]['code_incorrect']
	keyboard = shop.keyboards.keyboards[language]['code_incorrect']

	if status == True:
		msg = shop.messages.messages[language]['code_correct']
		keyboard = shop.keyboards.keyboards[language]['code_correct']

	await message.answer(text=msg,reply_markup=keyboard)

async def shop_registration_begin(callback: types.CallbackQuery, state: FSMContext, language='eng'):
	await state.reset_data()
	await state.set_state(ShopCreationStates.get_name.state)

	msg = shop.messages.messages[language]['get_shop_name']
	keyboard = shop.keyboards.keyboards[language]['to_client_menu']

	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()

@dp.message_handler(
	state=ShopCreationStates.get_name
)
@decorators.picked_language
async def shop_registration_get_name(message: types.Message, state: FSMContext, language='eng'):
	name = message.text
	await state.update_data(shop_name=name)
	await state.set_state(ShopCreationStates.get_phone.state)

	msg = shop.messages.messages[language]['get_shop_phone']
	keyboard = shop.keyboards.keyboards[language]['to_client_menu']

	await message.answer(text=msg, reply_markup=keyboard)


@dp.message_handler(
	state=ShopCreationStates.get_phone
)
async def shop_registration_get_phone(message: types.Message, state: FSMContext, language='eng'):
	phone = message.text
	await state.update_data(shop_phone=phone)
	await state.set_state(ShopCreationStates.get_location.state)

	msg = shop.messages.messages[language]['get_shop_location']
	keyboard = shop.keyboards.keyboards[language]['to_client_menu']

	await message.answer(text=msg, reply_markup=keyboard)

@dp.message_handler(
	state=ShopCreationStates.get_location
)
async def shop_registration_get_location(message: types.Message, state: FSMContext, language='eng'):
	location = message.text
	await state.update_data(shop_location=location)

	data = await state.get_data()
	await state.reset_state()


	await create_shop(user_id=message.from_user.id, data=data)

	msg = shop.messages.messages[language]['get_shop_name']
	keyboard = shop.keyboards.keyboards[language]['creation_success']

	await message.answer(text=msg, reply_markup=keyboard)