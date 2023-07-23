import logging

from config import SERVER_URL
from utils.requests import make_get_request, make_post_request

async def shop_get_courier_status(user_id):
    url = f'{SERVER_URL}/courier_status/{user_id}/'
    try:
        data = await make_get_request(url)
        return data['status']
    except Exception as e:
        logging.error(e)
        return ''

async def is_code_correct(user_id, code):
    url = f'{SERVER_URL}/courier_code/{user_id}/{code}'
    try:
        data = await make_get_request(url)
        return data['status']
    except Exception as e:
        logging.error(e)
        return False

async def create_courier(user_id, phone, name):
    url = f'{SERVER_URL}/create_courier/'
    data = {
        'user_id': user_id,
        'phone': phone,
        'name': name,
    }
    try:
        await make_post_request(url, data)
    except Exception as e:
        logging.error(e)
        return False