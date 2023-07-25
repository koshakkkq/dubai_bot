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