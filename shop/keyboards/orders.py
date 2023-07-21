import shop.logic
from .buttons import buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shop.constants import order_buttons_on_page


async def get_available_orders(shop_id, language, page):
	page = await shop.logic.get_available_orders_enabled_page(shop_id, page)

	available_orders = await shop.logic.get_available_orders(shop_id, (page - 1) * order_buttons_on_page, order_buttons_on_page)


	orders_cnt = available_orders['cnt']
	available_orders = available_orders['data']

	return get_keyboard_from_orders(
		orders=available_orders,
		orders_cnt=orders_cnt,
		language=language,
		page=page,
		command='available',
	)#available



async def get_active_orders(shop_id, language, page):

	page = await shop.logic.get_active_orders_enabled_page(shop_id, page)

	active_orders = await shop.logic.get_active_orders(shop_id, (page - 1) * order_buttons_on_page, order_buttons_on_page)


	orders_cnt = active_orders['cnt']
	active_orders = active_orders['data']

	return get_keyboard_from_orders(
		orders=active_orders,
		orders_cnt=orders_cnt,
		language=language,
		page=page,
		command='active',
	)

async def get_done_orders(shop_id, language, page):

	page = await shop.logic.get_done_orders_enabled_page(shop_id, page)

	done_orders = await shop.logic.get_done_orders(shop_id, (page - 1) * order_buttons_on_page,
													   order_buttons_on_page)
	cnt = done_orders['cnt']
	done_orders = done_orders['data']
	return get_keyboard_from_orders(
		orders=done_orders,
		orders_cnt=cnt,
		language=language,
		page=page,
		command='done',
	)

def get_keyboard_from_orders(orders,orders_cnt , language, page, command):
	orders_buttons = []

	for i in orders:
		orders_buttons.append(
			[InlineKeyboardButton(text=i['title'], callback_data=f"shop_get_{command}_order_{i['id']}")])

	max_page = (orders_cnt + order_buttons_on_page - 1) // order_buttons_on_page

	btn_page_cnt = InlineKeyboardButton(f'{page}/{max_page}', callback_data='empty_callback')

	btn_forward = InlineKeyboardButton('➡', callback_data=f'shop_{command}_orders_page_1')
	btn_back = InlineKeyboardButton('⬅', callback_data=f'shop_{command}_orders_page_-1')

	if max_page <= 1:
		pass
	elif page == max_page:
		orders_buttons.append([btn_back, btn_page_cnt])
	elif page == 1:
		orders_buttons.append([btn_page_cnt, btn_forward])
	else:
		orders_buttons.append([btn_back, btn_page_cnt, btn_forward])

	orders_buttons.append([buttons[language]['shop_menu']])

	return InlineKeyboardMarkup(inline_keyboard=orders_buttons)