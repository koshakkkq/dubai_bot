import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from utils.requests import make_get_request, make_post_request
from config import SERVER_URL
async def get_current_language(user_id: int):
	url = f'{SERVER_URL}/telegram_user?telegram_id={user_id}'
	data = await make_get_request(url)
	if len(data) == 0:
		return None
	else:
		return data[0]['language']

async def set_language(user_id, language):
	url = f'{SERVER_URL}/set_language/'
	post_data = {
		'tg_id': user_id,
		'language': language,
	}
	try:
		await make_post_request(url, post_data)
	except Exception as e:
		logging.error(e)

async def get_shop_id(tg_id):
	url = f'{SERVER_URL}/shop_member?user__telegram_id={tg_id}'
	try:
		res = await make_get_request(url)
	except Exception as e:
		logging.error(e)
		return None
	if len(res) == 0:
		return None
	return res[0]['shop']

async def get_courier_id(tg_id):
	url = f'{SERVER_URL}/shop_courier/{tg_id}/'
	try:
		res = await make_get_request(url)
		return res.get('courier_id', None)
	except Exception as e:
		logging.error(e)
		return None

async def bot_start(message: Message, state):

	await state.reset_state()
	await message.answer(f"Hello, {message.from_user.full_name}!\nChoose language!", reply_markup=language_choice())




def language_choice():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('ENG', callback_data=f"pick_language_eng"))
	keyboard.row(InlineKeyboardButton('ARA', callback_data=f"pick_language_ara"))
	keyboard.row(InlineKeyboardButton('HIN', callback_data=f"pick_language_hin"))
	return keyboard