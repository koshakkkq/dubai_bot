import logging

from config import SERVER_URL
from courier.constants import order_buttons_on_page, OrderStatus
from utils.requests import make_get_request, make_post_request


async def get_available_orders(courier_id, skip, limit):
    url = f'{SERVER_URL}/courier_available_orders/{courier_id}/{skip}/{limit}'
    try:
        data = await make_get_request(url)
        return data
    except Exception as e:
        logging.error(e)
        return {}


async def get_couriers_orders(courier_id, status, skip, limit):
    url = f'{SERVER_URL}/courier_available_orders/{courier_id}/{status}/{skip}/{limit}'
    try:
        data = await make_get_request(url)
        return data
    except Exception as e:
        logging.error(e)
        return {}

async def get_available_orders_page(page, courier_id):
    try:
        data = await get_available_orders(courier_id, 0, 0)
        max_page = data['cnt']
        return get_real_page(page, order_buttons_on_page, max_page)
    except Exception as e:
        logging.error(e)
        return 0


async def get_couriers_orders_page(page, status, courier_id):
    try:
        data = await get_couriers_orders(courier_id, status,0, 0)
        max_page = data['cnt']
        return get_real_page(page, order_buttons_on_page, max_page)
    except Exception as e:
        logging.error(e)
        return 0
async def get_order_information(order_id):
    url = f'{SERVER_URL}/courier_order/{order_id}/'
    try:
        data = await make_get_request(url)
        return data
    except Exception as e:
        logging.error(e)
        return None

async def create_order_offer_

async def set_courier_to_order(order_id, courier_id):
    url = f'{SERVER_URL}/courier_order/{order_id}/'

    data = {'courier_id': courier_id}

    try:
        data = await make_post_request(url, data)
        return data
    except Exception as e:
        logging.error(e)
        return None


async def add_to_blacklist(courier_id, order_id):
    url = f'{SERVER_URL}/courier_add_to_blacklist/{order_id}/{courier_id}/'

    try:
        await make_get_request(url)
        return ""
    except Exception as e:
        logging.error(e)
        return None
def get_real_page(page, buttons_on_page, cnt):
    if page < 1:
        return 1

    max_page = (cnt + buttons_on_page - 1) // buttons_on_page
    max_page = max(max_page, 1)
    if page > max_page:
        return max_page
    return page


async def get_active_orders_page(page, courier_id):
    return await get_couriers_orders_page(page, OrderStatus.ACTIVE,courier_id, )
async def get_done_orders_page(page, courier_id):
    return await get_couriers_orders_page(page, OrderStatus.DONE, courier_id, )
