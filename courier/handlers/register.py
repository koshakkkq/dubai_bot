import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from .courier_menu import menu_callback
from loader import dp

import courier.keyboards
import courier.messages
import utils.decorators as decorators

from courier.logic.registration import *
class CourierRegister(StatesGroup):
	pending_code = State()
	pending_name = State()
	pending_phone = State()
	finish = State()


@dp.callback_query_handler(
	filters.Text(equals="register_courier"),
	state="*",
)
@decorators.picked_language
async def shop_registration_proceed(callback: types.CallbackQuery, state: FSMContext, language='eng'):
	await state.reset_data()
	status = await shop_get_courier_status(callback.from_user.id)
	if status == 'courier':
		await menu_callback(callback, state)
		return
	if status == 'can_be_courier':
		await begin_registration(callback, state, language)
		return

	msg = courier.messages.messages[language]['get_code']

	keyboard = courier.keyboards.keyboards[language]['to_client_menu']
	await state.set_state(CourierRegister.pending_code.state)
	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()


@dp.message_handler(
	state = CourierRegister.pending_code,
)
@decorators.picked_language
async def get_code(message: types.Message, state: FSMContext, language='eng'):
	await state.reset_data()
	code = message.text

	status = await is_code_correct(message.from_user.id, code)

	msg = courier.messages.messages[language]['code_incorrect']
	keyboard = courier.keyboards.keyboards[language]['to_client_menu']

	if status == True:
		msg = courier.messages.messages[language]['code_correct']
		keyboard = courier.keyboards.keyboards[language]['code_correct']

	await message.answer(text=msg,reply_markup=keyboard)

async def begin_registration(callback: types.CallbackQuery, state: FSMContext, language='eng'):
	await state.reset_data()
	await state.set_state(CourierRegister.pending_phone.state)

	msg = courier.messages.messages[language]['get_courier_phone']
	keyboard = courier.keyboards.keyboards[language]['to_client_menu']

	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()

@dp.message_handler(
	state=CourierRegister.pending_phone
)
@decorators.picked_language
async def get_name(message: types.Message, state: FSMContext, language='eng'):
	phone = message.text
	await state.update_data(courier_phone=phone)
	await state.set_state(CourierRegister.pending_name.state)

	msg = courier.messages.messages[language]['get_courier_name']
	keyboard = courier.keyboards.keyboards[language]['to_client_menu']

	await message.answer(text=msg, reply_markup=keyboard)


@dp.message_handler(
	state=CourierRegister.pending_name
)
async def get_phone(message: types.Message, state: FSMContext, language='eng'):
	name = message.text
	await state.set_state(CourierRegister.finish.state)
	data = await state.get_data()

	await create_courier(message.from_user.id, data['courier_phone'], name)

	msg = courier.messages.messages[language]['courier_finish_registration']
	keyboard = courier.keyboards.keyboards[language]['code_correct']

	await message.answer(text=msg, reply_markup=keyboard)

