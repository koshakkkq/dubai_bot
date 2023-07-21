import logging

from config import SERVER_URL
from utils.requests import make_get_request
from .utils import get_real_page
from shop.constants import car_brands_buttons_on_page
async def get_brands(skip, limit):
	url = f'{SERVER_URL}/brands/{skip}/{limit}'

	try:
		data = await make_get_request(url)
		return data
	except Exception as e:
		return {}


async def get_brands_page(page):
	try:
		data = await get_brands(0,0)
		cnt = data['cnt']
		return get_real_page(page, car_brands_buttons_on_page, cnt)
	except Exception as e:
		logging.error(e)
		return 1

async def get_models_by_brand(brand_id ,skip, limit):
	if brand_id == 'Mazda':
		return ['6', 'CX-5', 'CX-4']



async def is_model_picked(model_id, user_id):
	if model_id == 'CX-5':
		return True
	else:
		return False