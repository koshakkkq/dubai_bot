import logging

from .requests import make_get_request, make_post_request
from config import SERVER_URL


def get_payed_orders(user_id):
    pass


async def get_cars():
    url = f'{SERVER_URL}/car_model/'
    data = await make_get_request(url)
    if len(data) == 0:
        return None
    else:
        return data


async def get_brands():
    url = f'{SERVER_URL}/car_brand/'
    data = await make_get_request(url)
    data.sort(key=lambda x: x["name"])
    if len(data) == 0:
        return None
    else:
        return data


async def get_models(brand_id):
    data = await get_cars()
    data.sort(key=lambda x: x["name"])
    cars = list(filter(lambda x: int(x["brand"]["id"]) == int(brand_id), data))
    return cars

async def set_msg_to_delete(tg_id, msg_id):
    data = {
        'msg_id':msg_id
    }
    url = f'{SERVER_URL}/msg_to_delete/{tg_id}/'
    try:
        res = await make_post_request(url, data)
    except Exception as e:
        return

async def get_years(brand_id, model): #cars
    data = await get_cars()
    data.sort(key=lambda x: x["production_start"])
    cars = list(filter(lambda x: int(x["brand"]["id"]) == int(brand_id) and x["name"] == model, data))
    return cars


async def get_orders(user_id, status=0): # status 0, 1, 2
    url = f'{SERVER_URL}/extended/order/'
    post_data = {
        'telegram_user_id': user_id,
        'status': status,
    }
    data = await make_post_request(url, post_data)
    if len(data) == 0:
        return None
    else:
        return data

async def reset_user_notifications(tg_id, data):
    data['tg_id'] = tg_id
    url = f'{SERVER_URL}/reset_user_notifications/'
    try:
        await make_post_request(url, data)
    except Exception as e:
        logging.error(e)
        return


async def reset_shop_notifications(shop_id, data):
    data['shop_id'] = shop_id
    url = f'{SERVER_URL}/reset_user_notifications/'
    try:
       await make_post_request(url, data)
    except Exception as e:
        logging.error(e)
        pass

async def order_create(user_id, model_id, additional):
    url = f"{SERVER_URL}/order/create/"
    post_data = {
        'telegram_user_id': user_id,
        'model_id': model_id,
        'additional': additional,
    }
    data = await make_post_request(url, post_data)
    return data


async def order_update(order_id, offer_id, status, is_delivery=False, address=None):
    url = f"{SERVER_URL}/order/update/"
    post_data = {
        'order_id': order_id,
        'offer_id': offer_id,
        "address": address,
        "status": status,
        "is_delivery": is_delivery,
    }
    data = await make_post_request(url, post_data)
    return data


async def shop_feedback_create(shop_id, mark, comment=None): # Кто убил Марка???
    if comment is None:
        comment = f"Mark: {mark}"
    url = f"{SERVER_URL}/shop/feedback/create/"
    post_data = {
        'shop_id': shop_id,
        'mark': mark,
        "comment": comment,
    }
    data = await make_post_request(url, post_data)
    return data


async def get_order(order_id):
    url = f"{SERVER_URL}/order/{order_id}/"
    data = await make_get_request(url)
    if len(data) == 0:
        return None
    else:
        return data


async def order_status_increase(order_id): # rec
    url = f"{SERVER_URL}/order/increase/{order_id}/"
    data = await make_get_request(url)


async def get_brand(id):
    id = int(id)
    brands = {item["name"]: item["id"] for item in await get_brands()}
    for key, val in brands.items():
        if val == id:
            return key
    return None


async def get_year(id, brand_id):
    for i in await get_models(brand_id):
        if i["id"] == id:
            return f"{i['production_start']} - {i['production_end']}"
    return None


async def get_notifications():
    url = f"{SERVER_URL}/notifications/"
    data = await make_get_request(url)
    result = {}
    for i in data["data"]:
        if i["type"] == "shop":
            result[i["user_id"]] = f"New available orders: {i['new_available_orders']}\nNew active orders: {i['new_active_orders']}"
        elif i["type"] == "user":
            result[i["user_id"]] = f"New offers: {i['new_offers']}\nNew couriers: {i['new_couriers']}"
    return result
