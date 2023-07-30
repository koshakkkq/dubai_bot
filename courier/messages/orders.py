import courier.orders
from courier.logic import *
import courier.messages


async def get_chosen_order_info(user_id, order_id, language):
    info = await courier.orders.get_order_info(order_id, user_id)
    if language == "eng":
        msg = f"Order from <a href='tg://user?id=5501657490'>CLIENT</a>\n\n" \
              f"Adress: {info['address']}\n\n" \
              f"Client comment: {info['comment']}\n\n" \
              f"Shop address: {info['shop_address']}\n\n" \
              f"Product:{info['product']}"
    return msg


async def get_picked_courier_msg(courier_id, language):
    if language == "eng":
        msg = f"You order is picked by this [courier](tg://user?id={courier_id}\n"
    return msg


async def get_courier_info_msg(tg_id, language):
    data = await get_courier_info(tg_id)

    if language == 'eng':
        msg = f"Your name: {data['name']}\n" \
              f"Your phone: {data['phone']}\n" \
              f"If you want to change information, click on buttons below."
        return msg



async def order_info(order_id, language):
    data = await get_order_information(order_id)
    data = data['data']

    location = {
        'latitude': data['lat'],
        'longitude': data['lon'],
    }

    if language == 'eng':

        msg = f'↑ Shop Geolocation ↑\n\n'\
              f"Shop address info: {data['shop_address']}\n" \
              f'Client address: {data["client_address"]}\n'
        return location, msg


async def set_order_courier_msg(courier_id,order_id ,language, prefix='courier_pick_order_prefix'):

    data = await set_courier_to_order(order_id=order_id, courier_id=courier_id)

    data = data['data']

    location = {
        'latitude': data['lat'],
        'longitude': data['lon'],
    }

    client_id = data['tg_id']

    prefix_msg = courier.messages.messages[language][prefix]
    if prefix == 'courier_done_order_prefix':
        prefix_msg += data['status']

    if language == 'eng':

        msg = f'↑ Shop Geolocation ↑\n\n'\
              f"{prefix_msg}" \
              f"Order from <a href='tg://user?id={client_id}'>CLIENT</a>\n" \
              f'User phone: {data["phone"]}\n' \
              f"Shop address: {data['shop_address']}\n" \
              f'Client address: {data["client_address"]}'

        return location, msg

async def get_couriers_order_info_msg(order_id, language, prefix):
    data = await get_order_information(order_id)
    data = data['data']

    location = {
        'latitude': data['lat'],
        'longitude': data['lon'],
    }

    client_id = data['tg_id']

    prefix_msg = ''

    if prefix == 'courier_done_order_prefix':
        if data['status'] == 'done':
            prefix_msg = courier.messages.messages[language]['courier_done_order_prefix']
        else:
            prefix_msg = courier.messages.messages[language]['courier_cancel_order_prefix']
    else:
        prefix_msg = courier.messages.messages[language][prefix]

    if language == 'eng':

        msg = f'↑ Shop Geolocation ↑\n\n'\
              f"{prefix_msg}" \
              f"Order from <a href='tg://user?id={client_id}'>CLIENT</a>\n" \
              f'User phone: {data["phone"]}\n' \
              f"Shop address: {data['shop_address']}\n" \
              f'Client address: {data["client_address"]}\n'\
              f'Order id: {data["id"]}'

        return location, msg
