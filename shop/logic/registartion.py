import logging

from utils.requests import make_get_request, make_post_request
import config

async def get_shop_member_status(user_id):
	url = f'{config.SERVER_URL}/shop_member_status/{user_id}/'
	try:
		data = await make_get_request(url)
		return data['status']
	except Exception as e:
		logging.error(e)
		raise e

async def is_code_correct(user_id, code):
	url = f'{config.SERVER_URL}/is_code_correct/{user_id}/{code}/'

	try:
		data = await make_get_request(url)
		return data['status']
	except Exception as e:
		logging.error(e)
		raise e


async def create_shop(user_id, data, ):
	url = f'{config.SERVER_URL}/create_shop/'

	data = {
		'tg_id':user_id,
		'name': data['shop_name'],
		'location': data['shop_location'],
		'phone': data['shop_phone'],
		'lon': data['shop_lon'],
		'lat': data['shop_lat'],
	}


	try:
		data = await make_post_request(url, data)
		return data['status']
	except Exception as e:
		logging.error(e)
		raise e