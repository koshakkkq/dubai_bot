from loader import bot
from user.keyboards import inline
from utils import api
from user.constants import VERBOSE_ORDER_TYPE


# async def send_message_of_interest(user_id, shop_id, order_id):
# 	message = "Good afternoon.\nWere you able to pick up your order?"
# 	await bot.send_message(user_id, message, reply_markup=inline.was_deliveried(shop_id, order_id))


async def text_for_order(order_id):

	order = await api.get_order(order_id)
	shop = order['offer']['shop']
	additional = '\n\nDelivery type : Pickup from from shop.'
	if order['status'] == 1:
		if order['credential']['is_delivery'] is True:
			if order['credential']['courier'] is not None:
				courier_phone = order['credential']['courier']['phone']
				courier_tg_id = order['credential']['courier']['telegram_user']['telegram_id']

				additional = f'Courier will contact you soon.\n' \
							 f'Courier contacts:\n' \
							 f'Phone: {courier_phone}\n' \
							 f"TELEGRAM: <a href='tg://user?id={courier_tg_id}'>CLICK</a>\n"
			else:
				additional = 'Waiting for the courier to take care of your order'

	shop_tg_id = order['shop_tg_id']

	text = f"""id: {order_id}
status: {VERBOSE_ORDER_TYPE[order['status']][1]}
{order['additional']}
Shop name: {shop['name']}
Shop location: <a href='https://www.google.com/maps/dir/{shop['lat']},{shop['lon']}'>CLICK</a> - {shop['location']}
Shop phone: {shop['phone']}
Shop telegram: <a href='tg://user?id={shop_tg_id}'>CLICK</a>
Price: {order['offer']['price']}

"""
	text += additional
	return text