import shop.logic.orders
async def get_available_order_info_message(user_id, order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)

    if language == 'eng':
        return f'Order info:\n\n' \
               f'Car brand: {order_info["brand"]}\n'\
               f'Car model: {order_info["model"]}\n'\
               f'Part: {order_info["part"]}\n'\
               f'Additional information: {order_info["additional"]}\n'