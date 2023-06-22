import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp


import courier.keyboards
import courier.messages
import decorators
class CourierStates(StatesGroup):
	in_menu = State()
	available_orders = State()
	available_order_info = State()
	delivered_orders = State()


@decorators.picked_language
async def menu_msg_handler(message: types.Message, state:FSMContext, language= 'eng'):
	await state.reset_data()
	await state.set_state(CourierStates.in_menu.state)


	msg = courier.messages.messages[language]['courier_menu']

	keyboard = courier.keyboards.keyboards[language]['courier_menu']

	await message.answer(text=msg, reply_markup=keyboard)

@dp.callback_query_handler(
	filters.Text(equals="courier_menu"),
	state="*",
)
@decorators.picked_language
async def menu_callback(callback: types.CallbackQuery, state: FSMContext, language= 'eng'):
	await state.reset_data()
	await state.set_state(CourierStates.in_menu.state)
	msg = courier.messages.messages[language]['courier_menu']

	keyboard = courier.keyboards.keyboards[language]['courier_menu']

	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()

@dp.callback_query_handler(
	filters.Text(equals="courier_available_orders"),
	state="*",
)
@decorators.picked_language
async def available_orders_callback(callback: types.CallbackQuery, state: FSMContext, language= 'eng'):
	await state.set_state(CourierStates.available_orders.state)

	msg = '*....*'

	keyboard = await courier.keyboards.get_available_orders_keyboard(callback.message.from_user.id, language)

	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()

@dp.callback_query_handler(
	filters.Text(startswith="courier_pick_order"),
	state="*",
)
@decorators.picked_language
async def available_order_info_callback(callback: types.CallbackQuery, state: FSMContext, language= 'eng'):
	await state.set_state(CourierStates.available_order_info.state)

	order_id = callback.data.split('_')[-1]
	await state.update_data(order_id=order_id)

	msg = await courier.messages.get_order_info(
		callback.from_user.id,
		order_id,
		language,
	)

	keyboard = courier.keyboards.keyboards[language]['order_info']

	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()


@dp.callback_query_handler(
	filters.Text(equals="courier_choose_order"),
	state="*",
)
@decorators.picked_language
async def pick_available_order(callback: types.CallbackQuery, state: FSMContext, language= 'eng'):

	data = await state.get_data()
	msg = await courier.messages.get_chosen_order_info(
		callback.from_user.id,
		data['order_id'],
		language,
	)
	await callback.message.edit_text(text=msg, parse_mode="HTML")
	await callback.answer('Redirect to menu in 3 seconds.')
	await asyncio.sleep(3)
	await menu_msg_handler(callback.message, state)

@dp.callback_query_handler(
	filters.Text(equals="courier_delivered_orders"),
	state="*",
)
@decorators.picked_language
async def delivered_orders_list(callback: types.CallbackQuery, state: FSMContext, language='eng'):

	await state.set_state(CourierStates.delivered_orders.state)

	keyboard = await courier.keyboards.get_delivered_keyboard(callback.from_user.id, language)

	await callback.message.edit_text(text=courier.messages.messages[language]['delivered_orders'], reply_markup=keyboard,parse_mode="HTML")


	await callback.answer()
