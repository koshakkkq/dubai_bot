from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import courier.logic
from .buttons import buttons
from courier.constants import order_buttons_on_page, OrderStatus




async def get_available_orders(courier_id, page, language, prefix):
	page = await courier.logic.get_available_orders_page(page, courier_id)

	done_orders = await courier.logic.get_available_orders(courier_id, (page - 1) * order_buttons_on_page,
												   order_buttons_on_page)
	cnt = done_orders['cnt']
	done_orders = done_orders['data']
	return get_keyboard_from_orders(
		orders=done_orders,
		orders_cnt=cnt,
		language=language,
		page=page,
		prefix=prefix,
	)

async def get_active_orders(courier_id, page, language, prefix):
	page = await courier.logic.get_couriers_orders_page(page, OrderStatus.ACTIVE, courier_id)

	orders = await courier.logic.get_couriers_orders(courier_id, OrderStatus.ACTIVE, (page - 1) * order_buttons_on_page,
												   order_buttons_on_page)

	cnt = orders['cnt']
	done_orders = orders['data']

	return get_keyboard_from_orders(
		orders=done_orders,
		orders_cnt=cnt,
		language=language,
		page=page,
		prefix=prefix,
	)

async def get_done_orders(courier_id, page, language, prefix):
	page = await courier.logic.get_couriers_orders_page(page, OrderStatus.DONE, courier_id)

	orders = await courier.logic.get_couriers_orders(courier_id, OrderStatus.DONE, (page - 1) * order_buttons_on_page,
												   order_buttons_on_page)

	cnt = orders['cnt']
	done_orders = orders['data']

	return get_keyboard_from_orders(
		orders=done_orders,
		orders_cnt=cnt,
		language=language,
		page=page,
		prefix=prefix,
	)

def get_keyboard_from_orders(orders,orders_cnt , language, page, prefix):
	orders_buttons = []

	for i in orders:
		orders_buttons.append(
			[InlineKeyboardButton(text=i['title'], callback_data=f"{prefix}_get_{i['id']}")])

	max_page = (orders_cnt + order_buttons_on_page - 1) // order_buttons_on_page

	btn_page_cnt = InlineKeyboardButton(f'{page}/{max_page}', callback_data='empty_callback')

	btn_forward = InlineKeyboardButton('➡', callback_data=f'{prefix}_page_1')
	btn_back = InlineKeyboardButton('⬅', callback_data=f'{prefix}_page_-1')

	if max_page <= 1:
		pass
	elif page == max_page:
		orders_buttons.append([btn_back, btn_page_cnt])
	elif page == 1:
		orders_buttons.append([btn_page_cnt, btn_forward])
	else:
		orders_buttons.append([btn_back, btn_page_cnt, btn_forward])

	orders_buttons.append([buttons[language]['courier_menu']])

	return InlineKeyboardMarkup(inline_keyboard=orders_buttons)


