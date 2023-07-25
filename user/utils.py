from loader import bot
from user.keyboards import inline
from utils import api
from user.constants import VERBOSE_ORDER_TYPE


async def send_message_of_interest(user_id, shop_id, order_id):
	message = "Good afternoon.\nWere you able to pick up your order?"
	await bot.send_message(user_id, message, reply_markup=inline.was_deliveried(shop_id, order_id))


async def text_for_order(order_id):
	order = await api.get_order(order_id)
	shop = order['offer']['shop']
	text = f"""id: {order_id}
status: {VERBOSE_ORDER_TYPE[order['status']][1]}
{order['additional']}
Shop name: {shop['name']}
Shop location: {shop['location']}
Shop phone: {shop['phone']}
Price: {order['offer']['price']}"""
	return text