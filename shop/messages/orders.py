import shop.logic.orders
async def get_available_order_info_message(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']

    if language == 'eng':
        res_msg = f'Order info:\n\n ' \
               f'Car model: {order_info["model"]}\n '\
               f'Additional information: {order_info["additional"]}\n\n '\
               f'Write your price, if you want to accept the order.'
        return ('info', res_msg)


async def get_active_order_info(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']

    if language == 'eng':
        res_msg = f"Order from <a href='tg://user?id={order_info['customer_id']}'>CLIENT</a>: \n\n" \
                  f'Car model: {order_info["model"]}\n' \
                  f'Additional information: {order_info["additional"]}\n '\
                  f'Your suggested price: {order_info["price"]}'
        return ('info', res_msg)


async def get_done_order_info(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']

    if language == 'eng':
        res_msg = f"Order from <a href='tg://user?id={order_info['customer_id']}'>CLIENT</a>: \n\n" \
                  f'Car model: {order_info["model"]}\n' \
                  f'Additional information: {order_info["additional"]}\n '\
                  f'Your suggested price: {order_info["price"]}\n'\
                  f'Status: {order_info["status"]}'
        return ('info', res_msg)