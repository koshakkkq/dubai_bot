import logging

from utils.requests import make_get_request, make_post_request
from config import SERVER_URL
from shop.constants import buttons_on_page
async def get_available_orders(shop_id, skip, limit):
    url = f'{SERVER_URL}/shop_available_orders/{shop_id}/{skip}/{limit}/'

    try:
        data = await make_get_request(url)
        return data
    except Exception as e:
        logging.error(e)
        return []


async def get_active_orders(shop_id, skip, limit):
    url = f'{SERVER_URL}/shop_active_orders/{shop_id}/{skip}/{limit}/'
    try:
        data = await make_get_request(url)
        return data
    except Exception as e:
        logging.error(e)
        return []

async def get_available_orders_enabled_page(shop_id, page):
    if page < 1:
        return 1

    data = await get_available_orders(shop_id, 0, 0)
    cnt = data.get('available_orders_cnt', 0)
    max_page = (cnt + buttons_on_page - 1) // buttons_on_page
    if page > max_page:
        return max_page
    return page



async def get_active_orders_enabled_page(shop_id, page):
    data = await get_available_orders(shop_id, 0, 0)
    cnt = data.get('available_orders_cnt', 0)
    max_page = (cnt + buttons_on_page - 1) // buttons_on_page
    if page > max_page:
        return max_page
    return page

async def get_available_order_info(order_id:int):
    url = f'{SERVER_URL}/shop_order_info/{order_id}'
    try:
        data = await make_get_request(url)
    except Exception as e:
        logging.error(e)
        return {''}
    return data

async def create_order_blacklist(order_id, shop_id):
    url = f'{SERVER_URL}/shop_add_order_blacklist/'
    data = {
        'order_id': order_id,
        'shop_id': shop_id,
    }
    try:
         await make_post_request(url, data)
    except Exception as e:
        logging.error(e)
    return data
async def create_order_offer(shop_id, price, order_id):
    url = f'{SERVER_URL}/shop_create_order_offer/'

    data = {
        'shop_id': shop_id,
        'order_id': order_id,
        'price': price,
    }
    try:
        await make_post_request(url, data)
    except Exception as e:
        logging.error(e)
