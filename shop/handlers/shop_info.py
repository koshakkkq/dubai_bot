import aiogram.utils.exceptions
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp, bot
from utils.api import set_msg_to_delete
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

	location, info = await shop.messages.get_shop_info_message(shop_id)

	keyboard = shop.keyboards.keyboards[language]['shop_info']

	user_id = callback.from_user.id

	await callback.message.delete()

	msg = await bot.send_location(user_id, **location)
	await set_msg_to_delete(user_id, msg.message_id)

	await bot.send_message(user_id, text=info, reply_markup=keyboard)


	await callback.answer()

@dp.callback_query_handler(
	filters.Text(equals="shop_get_brands"),
	state="*",
)
@decorators.picked_language
@decorators.is_member
@decorators.delete_msg_decorator
async def show_brands_begin(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	data = await state.get_data()
	if "shop_info_brands_page" not in data:
		data['shop_info_brands_page'] = 1

	page = data['shop_info_brands_page']

	page = await shop.logic.get_brands_page(page)

	await state.update_data(shop_info_brands_page=page)

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
	filters.Text(startswith="shop_info_brand_page_"),
	state="*",
)
@decorators.picked_language
@decorators.is_member
async def change_brand_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	command = int(callback.data.split('_')[-1])
	data = await state.get_data()

	cur_page = data.get('shop_info_brands_page', 0)
	cur_page += command

	cur_page = await shop.logic.get_brands_page(cur_page)

	await state.update_data(shop_info_brands_page=cur_page)
	await show_brands(callback, state, language, shop_id, cur_page, edit_msg=False)

@dp.callback_query_handler(
	filters.Text(startswith='shop_info_get_brand_'),
	state='*',
)
@decorators.picked_language
@decorators.is_member
async def pick_brand(callback:types.CallbackQuery, state:FSMContext, language='eng', shop_id=-1):
	brand = callback.data.split('_')[-1]
	await state.update_data(shop_info_brand_id=brand)
	await state.update_data(shop_info_model_page=1)


	await show_models_by_brand(callback=callback, state=state, language=language, shop_id=shop_id, edit_message=True)


async def show_models_by_brand(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1, edit_message=False):
	data = await state.get_data()
	brand_id = data['shop_info_brand_id']
	page = data['shop_info_model_page']

	keyboard = await shop.keyboards.get_models_keyboard(shop_id, brand_id=brand_id, language=language, page=page)
	if edit_message == True:
		msg = shop.messages.messages[language]['shop_info_models']
		await callback.message.edit_text(text=msg, reply_markup=keyboard)
	else:
		try:
			await callback.message.edit_reply_markup(reply_markup=keyboard)
		except aiogram.utils.exceptions.MessageNotModified as e:
			pass
	await callback.answer()
@dp.callback_query_handler(
	filters.Text(startswith='shop_info_model_page_'),
	state='*',
)
@decorators.picked_language
@decorators.is_member
async def change_models_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	data = await state.get_data()
	command = int(callback.data.split('_')[-1])

	page = data.get('shop_info_model_page', 0) + command

	brand_id = data['shop_info_brand_id']

	page = await shop.logic.get_models_page(shop_id, brand_id, page)

	await state.update_data(shop_info_model_page=page)

	await show_models_by_brand(callback, state, language, shop_id, False)



@dp.callback_query_handler(
	filters.Text(startswith='shop_info_pick_model_'),
	state='*',
)
@decorators.picked_language
@decorators.is_member
async def pick_model(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):

	data = [callback.data]

	await shop.logic.change_status_of_models(data, shop_id)

	data = await state.get_data()

	page = data['shop_info_model_page']
	brand_id = data['shop_info_brand_id']

	page = await shop.logic.get_models_page(shop_id, brand_id, page)

	await state.update_data(shop_info_model_page=page)

	await show_models_by_brand(callback, state, language, shop_id, False)

@dp.callback_query_handler(
	filters.Text(startswith='shop_info_pick_all_models_'),
	state='*',
)
@decorators.picked_language
@decorators.is_member
async def pick_all_models(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):

	data = await state.get_data()

	brand_id = data['shop_info_brand_id']

	command = int(callback.data.split('_')[-1])

	await shop.logic.pick_all_models(command, brand_id, shop_id)

	await show_models_by_brand(callback, state, language, shop_id, False)



@dp.callback_query_handler(
	filters.Text(startswith='shop_info_pick_page_models_'),
	state='*',
)
@decorators.picked_language
@decorators.is_member
async def pick_models_on_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
	models = []

	command = callback.data.split('_')[-1]


	for i in callback.message.reply_markup["inline_keyboard"]:
		for j in i:
			if 'pick_model' in j['callback_data']:
				to_add = j['callback_data']
				to_add = to_add[:-1] + command
				models.append(to_add)


	await shop.logic.change_status_of_models(models,shop_id)

	await show_models_by_brand(callback, state, language, shop_id, False)

class ChangeShopInfoStates(StatesGroup):
	pending_value = State()
	pending_coords = State()
	empty = State()
@dp.callback_query_handler(
	filters.Text(startswith="shop_change_"),
	state="*",
)
@decorators.picked_language
@decorators.is_member
@decorators.delete_msg_decorator
async def change_shop_information(callback:types.CallbackQuery, state:FSMContext, language='eng', shop_id = -1):
	to_change = callback.data.split('_')[-1]
	if to_change != 'coords':
		await state.set_state(ChangeShopInfoStates.pending_value.state)
	else:
		await state.set_state(ChangeShopInfoStates.pending_coords.state)
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


@dp.message_handler(
	state=ChangeShopInfoStates.pending_coords,
	content_types=['location'],
)
@decorators.picked_language
@decorators.is_member
async def get_coords_to_change(message: types.Message, state: FSMContext, language='eng', shop_id = -1):
	lat = message.location.latitude
	lon = message.location.longitude

	data = await state.get_data()
	await state.reset_state()
@dp.callback_query_handler(
	filters.Text(equals='shop_info_create_invite'),
	state="*",
)
@decorators.picked_language
@decorators.is_member
@decorators.delete_msg_decorator
async def create_invite_code(callback:types.CallbackQuery, state:FSMContext, language='eng', shop_id = -1):
	code = await shop.logic.create_code(shop_id)

	keyboard = shop.keyboards.keyboards[language]['shop_back_from_change']

	await callback.message.edit_text(text=code, reply_markup=keyboard)

	await callback.answer()

