import courier.orders
from courier.logic import *
import courier.messages


async def get_chosen_order_info(user_id, order_id, language):
    pass


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

    route_url = get_google_maps_link(data)

    if language == 'eng':
        msg = f"Shop address info: {data['shop_address']}\n" \
              f'Client address info: {data["client_address"]}\n' \
              f'Price: {data["price"]}\n'\
              f'{data["additional"]}\n'\
              f"<a href='{route_url}'>Route from shop to client</a>"
        return msg


async def set_order_courier_msg(courier_id, order_id, language, prefix='courier_pick_order_prefix'):
    data = await set_courier_to_order(order_id=order_id, courier_id=courier_id)

    data = data['data']


    client_id = data['tg_id']

    prefix_msg = courier.messages.messages[language][prefix]
    if prefix == 'courier_done_order_prefix':
        prefix_msg += data['status']

    route_url = get_google_maps_link(data)

    if language == 'eng':
        msg = f"{prefix_msg}" \
              f"Order from <a href='tg://user?id={client_id}'>CLIENT</a>\n" \
              f'User phone: {data["phone"]}\n' \
              f"Shop address: {data['shop_address']}\n" \
              f'Client address: {data["client_address"]}\n' \
              f'Price: {data["price"]}\n' \
              f'{data["additional"]}\n' \
              f'Order id: {data["id"]}\n'\
              f"<a href='{route_url}'>Route from shop to client</a>"

        return msg


async def get_couriers_order_info_msg(order_id, language, prefix):
    data = await get_order_information(order_id)
    data = data['data']

    client_id = data['tg_id']

    prefix_msg = ''
    if prefix == 'courier_done_order_prefix':
        if data['status'] == 'DONE':
            prefix_msg = courier.messages.messages[language]['courier_done_order_prefix']
        else:
            prefix_msg = courier.messages.messages[language]['courier_cancel_order_prefix']
    else:
        prefix_msg = courier.messages.messages[language][prefix]

    route_url = get_google_maps_link(data)

    if language == 'eng':
        msg = f"{prefix_msg}" \
              f"Order from <a href='tg://user?id={client_id}'>CLIENT</a>\n" \
              f"Shop address information: {data['shop_address']}\n" \
              f'Client address information: {data["client_address"]}\n' \
              f'Order id: {data["id"]}\n' \
              f'Price: {data["price"]}\n'\
              f'{data["additional"]}\n' \
              f"<a href='{route_url}'>Route from shop to client</a>"

        return msg


def get_google_maps_link(data):
    return f'https://www.google.com/maps/dir/?api=1&origin={data["shop_lat"]},{data["shop_lon"]}&destination={data["cred_lat"]},{data["cred_lon"]}'
