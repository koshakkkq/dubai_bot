import logging

from config import SERVER_URL
from utils.requests import make_get_request
from .utils import get_real_page
from shop.constants import car_brands_buttons_on_page, car_models_buttons_on_page
async def get_brands(shop_id, skip, limit):
	url = f'{SERVER_URL}/brands/{shop_id}/{skip}/{limit}'

	try:
		data = await make_get_request(url)
		return data
	except Exception as e:
		return {}


async def get_brands_page(page, shop_id):
	try:
		data = await get_brands(shop_id,0,0)
		cnt = data['cnt']
		return get_real_page(page, car_brands_buttons_on_page, cnt)
	except Exception as e:
		logging.error(e)
		return 1

async def get_models_by_brand(shop_id, brand_id ,skip, limit):
	url = f'{SERVER_URL}/models/{shop_id}/{brand_id}/{skip}/{limit}/'

	try:
		data = await make_get_request(url)
		return data
	except Exception as e:
		logging.error(e)
		return {}


async def get_models_page(shop_id, brand_id, page):
	try:
		data = await get_models_by_brand(shop_id,brand_id, 0, 0)
		cnt = data['cnt']
		return get_real_page(page, car_models_buttons_on_page, cnt)
	except Exception as e:
		logging.error(e)
		return 1

