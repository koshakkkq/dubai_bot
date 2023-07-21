
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
async def get_brands_callback(callback: types.CallbackQuery, state: FSMContext, language='eng'):
	await state.update_data(brands_page = 1)
	await show_all_brands_callback(
		callback=callback,
		state=state,
		language=language,
	)#для вывода отдельная функция чтобы можно было сделать удобную пагинацию(просто менять brands_page и выводить
	 # в show_all_brands_callback все бренды.

@decorators.picked_language
async def show_all_brands_callback(
		callback: types.CallbackQuery,
		state: FSMContext,
		language = 'eng'
):
	await state.set_state(ShopInfoStates.brands.state)

	data = await state.get_data()

	page = data['brands_page']


	keyboard = await shop.keyboards.get_brands_keyboard(
		user_id=callback.from_user.id,
		current_language=language,
		page=page,
	)


	message = shop.messages.messages[language]['shop_info_brands']

	await callback.message.edit_text(text=message, reply_markup=keyboard)
	await callback.answer()


@dp.callback_query_handler(
	filters.Text(startswith="pick_brand_"),
	state="*",
)
@decorators.picked_language
async def pick_brand(callback:types.CallbackQuery, state: FSMContext, language='eng'):
	brand_id = callback.data.split('_')[-1]
	await state.update_data(brand_id=brand_id)
	await state.update_data(model_page = 1)
	await show_models(callback=callback, state=state, language=language,page=1)#тоже самое что и get_brands_callback


@decorators.picked_language
async def show_models(callback:types.CallbackQuery, state:FSMContext, language='eng', page = 1):
	await state.set_state(ShopInfoStates.models.state)


	data = await state.get_data()
	brand_id = data['brand_id']

	message = shop.messages.messages[language]['shop_info_models']

	keyboard = await shop.keyboards.get_models_keyboard(
		user_id=callback.from_user.id,
		brand_id=brand_id,
		current_language=language,
		page=page,
	)

	await callback.message.edit_text(text=message, reply_markup=keyboard)
	await callback.answer()


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



