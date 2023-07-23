import logging

from config import SERVER_URL
from utils.requests import make_get_request, make_post_request


async def get_courier_info(tg_id):
	url = f'{SERVER_URL}/shop_courier/{tg_id}/'
	try:
		data = await make_get_request(url)
		return data
	except Exception as e:
		logging.error(e)
		return {'status':False}

async def change_courier_info(couried_id, field, value):
	url = f'{SERVER_URL}/shop_courier/{couried_id}/'
	data = {
		'field': field,
		'value': value,
	}

	try:
		await make_post_request(url, data)
	except Exception as e:
		logging.error(e)