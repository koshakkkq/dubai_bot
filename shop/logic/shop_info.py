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

async def change_status_of_models(models, shop_id):
	data = {
		'type': 'specify',
		'data': [],
	}
	for i in models:
		splited = i.split('_')
		model_id = splited[-2]
		status = splited[-1]
		data['data'].append({
			'model_id': model_id,
			'status': status,
		})

	url = f'{SERVER_URL}/pick_models/{shop_id}/'
	try:
		await make_post_request(url, data)
		return
	except Exception as e:
		return

async def pick_all_models(status, brand_id, shop_id):
	data = {
		'type': 'all',
		'status': status,
		'brand_id': brand_id,
	}
	url = f'{SERVER_URL}/pick_models/{shop_id}/'
	try:
		await make_post_request(url, data)
		return
	except Exception as e:
		logging.error(e)
		return

async def change_shop_information(shop_id, data):
	url = f'{SERVER_URL}/shop_info/{shop_id}/'

	try:
		await make_post_request(url, data)
	except Exception as e:
		logging.error(e)
		return

async def create_code(shop_id):
	url = f'{SERVER_URL}/create_invite_code/{shop_id}'
	try:
		data = await make_get_request(url)
		return data['code']
	except Exception as e:
		logging.error(e)
		return 'Error'