import logging

from utils.requests import make_get_request, make_post_request
from config import SERVER_URL
async def get_shop_information(shop_id):
	url = f'{SERVER_URL}/shop_info/{shop_id}/'

	try:
		data = await make_get_request(url)
		return data
	except Exception as e:
		logging.error(e)
		return {}


async def change_shop_information(shop_id, field, value):
	url = f'{SERVER_URL}/shop_info/{shop_id}/'

	try:
		data = {
			field: value,
		}
		await make_post_request(url, data)
	except Exception as e:
		logging.error(e)
		return