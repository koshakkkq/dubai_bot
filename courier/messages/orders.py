import courier.orders
async def get_order_info(user_id, order_id, language):
    info = await courier.orders.get_order_info(order_id, user_id)
    if language == "eng":
        msg = f"Order:\n\n" \
              f"Adress: {info['address']}\n\n" \
              f"Client comment: {info['comment']}\n\n" \
              f"Shop address: {info['shop_address']}\n\n" \
              f"Product:{info['product']}"

    return msg



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