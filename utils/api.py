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


async def get_orders(user_id, payed=False):
    url = f'{SERVER_URL}/order/'
    data = await make_get_request(url)
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