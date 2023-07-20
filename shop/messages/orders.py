import shop.logic.orders
async def get_available_order_info_message(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']

    if language == 'eng':
        res_msg = f'Order info:\n\n' \
               f'Car model: {order_info["model"]}\n'\
               f'Product: {order_info["product"]}\n'\
               f'Additional information: {order_info["additional"]}\n\n' \
               f'Write your price, if you want to accept the order.'
        return ('info', res_msg)


async def get_active_order_info(user_id, order_id, language):
    pass
    # order_info = await shop.logic.orders.get_available_order_info(order_id)
    #
    # if language == 'eng':
    #     return f'Order №1:\n\n' \
    #            f'Car brand: {order_info["brand"]}\n' \
    #            f'Car model: {order_info["model"]}\n' \
    #            f'Part: {order_info["part"]}\n' \
    #            f'Additional information: {order_info["additional"]}\n'