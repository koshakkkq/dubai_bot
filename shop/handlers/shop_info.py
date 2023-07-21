
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp
from .shop_menu import ShopMenuStates, shop_menu_callback

import utils.decorators as decorators
import shop.messages
import shop.keyboards
import shop.logic

class ShopInfoStates(StatesGroup):
	info = State()
	change_location = State()
	change_phone = State()
	brands = State()
	models = State()


@dp.callback_query_handler(
	filters.Text(equals="shop_info"),
	state="*",
)

@decorators.picked_language
@decorators.is_member
async def shop_info_callback(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	await state.reset_data()
	await state.set_state(ShopInfoStates.info.state)

	msg = await shop.messages.get_shop_info_message(shop_id)

	keyboard = shop.keyboards.keyboards[language]['shop_info']

	await callback.message.edit_text(text=msg, reply_markup=keyboard)
	await callback.answer()

@dp.callback_query_handler(
	filters.Text(equals="shop_get_brands"),
	state="*",
)
@decorators.picked_language
@decorators.is_member
async def show_brands_begin(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	data = await state.get_data()
	if "shop_info_brands_page" not in data:
		data['shop_info_brands_page'] = 1
		await state.update_data(shop_info_brands_page=1)

	page = data['shop_info_brands_page']

	await show_brands(callback, state, language, shop_id, page, edit_msg=True)

async def show_brands(callback: types.CallbackQuery, state: FSMContext, language, shop_id, page, edit_msg = False):
	keyboard = await shop.keyboards.get_brands_keyboard(language,page)

	if edit_msg == True:
		msg = shop.messages.messages[language]['shop_info_brands']

		await callback.message.edit_text(text=msg, reply_markup=keyboard)
	else:
		await callback.message.edit_reply_markup(reply_markup=keyboard)
		await callback.answer()

@dp.callback_query_handler(
	filters.Text(startswith="shop_info_brand_orders_page_"),
	state="*",
)
@decorators.picked_language
@decorators.is_member
async def change_done_orders_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	command = int(callback.data.split('_')[-1])
	data = await state.get_data()

	cur_page = data.get('shop_info_brands_page', 0)
	cur_page += command
	await state.update_data(shop_info_brands_page=cur_page)
	print(cur_page)
	await show_brands(callback, state, language, shop_id, cur_page, edit_msg=False)

@dp.callback_query_handler(
	filters.Text(startswith='shop_info_get_brand_'),
	state='*',
)
@decorators.picked_language
async def picked_brand(callback:types.CallbackQuery, state:FSMContext, language='eng', page = 1):
	brand = callback.data.split('_')[-1]
	print(brand)
	await callback.answer(brand)


class ChangeShopInfoStates(StatesGroup):
	pending_value = State()
	empty = State()
@dp.callback_query_handler(
	filters.Text(startswith="shop_change_"),
	state="*",
)
@decorators.picked_language
@decorators.is_member
async def change_shop_information(callback:types.CallbackQuery, state:FSMContext, language='eng', shop_id = -1):
	to_change = callback.data.split('_')[-1]
	await state.set_state(ChangeShopInfoStates.pending_value.state)
	await state.update_data(shop_filed_to_change = to_change)

	msg = shop.messages.messages[language][f'shop_change_{to_change}']
	keyboard = shop.keyboards.keyboards[language]['shop_back_from_change']

	await callback.message.edit_text(text=msg, reply_markup=keyboard)

	await callback.answer()


@dp.message_handler(
	state=ChangeShopInfoStates.pending_value
)
@decorators.picked_language
@decorators.is_member
async def get_value_to_change(message: types.Message, state: FSMContext, language='eng', shop_id = -1):
	value = message.text
	data = await state.get_data()
	await state.reset_state()
	field = data['shop_filed_to_change']
	await shop.logic.change_shop_information(shop_id, field=field, value=value)
	keyboard = shop.keyboards.keyboards[language]['shop_back_from_change']
	msg = shop.messages.messages[language]['ok']
	await message.answer(text=msg, reply_markup=keyboard)



