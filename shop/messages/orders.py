import shop.logic.orders
async def get_available_order_info_message(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']

    if language == 'eng':
        res_msg = f'Order info:\n\n' \
               f'Car model: {order_info["model"]}\n'\
               f'{order_info["additional"]}\n\n'\
               f'Write your price, if you want to accept the order.'
        return ('info', res_msg)




async def get_my_response_order_info_message(order_id, shop_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    order_offer = await shop.logic.orders.get_offer(order_id, shop_id)

    order_info = order_info['data']
    price = order_offer['price']


    if language == 'eng':
        res_msg = f"Order from <a href='tg://user?id={order_info['customer_id']}'>CLIENT</a>:\n\n" \
                  f'Car model: {order_info["model"]}\n' \
                  f'{order_info["additional"]}\n' \
                  f'Order id: {order_info["id"]}\n'\
                  f'Your suggested price: {price} \n'\
                  'if you want to cancel offer use button below, if you want to set new price, enter new value.'
        return res_msg



async def get_active_order_info(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']



    if language == 'eng':
        res_msg = f"Order from <a href='tg://user?id={order_info['customer_id']}'>CLIENT</a>:\n\n" \
                  f'Car model: {order_info["model"]}\n' \
                  f'{order_info["additional"]}\n'\
                  f'Your suggested price: {order_info["price"]}\n'\
                  f'Order id: {order_info["id"]}'
        return ('info', res_msg)


async def get_done_order_info(order_id, language):
    order_info = await shop.logic.orders.get_available_order_info(order_id)
    if order_info['status'] == 'does_not_exist':
        return ('does_not_exist', '')

    order_info = order_info['data']


    if language == 'eng':
        res_msg = f"Order from <a href='tg://user?id={order_info['customer_id']}'>CLIENT</a>:\n\n" \
                  f'Car model: {order_info["model"]}\n' \
                  f'{order_info["additional"]}\n'\
                  f'Your suggested price: {order_info["price"]}\n'\
                  f'Status: {order_info["status"]}\n'\
                  f'Order id: {order_info["id"]}'
        return ('info', res_msg)