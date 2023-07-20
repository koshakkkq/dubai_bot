import shop.logic
from .buttons import buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from shop.constants import buttons_on_page


async def get_available_orders(shop_id, language, page):
	page = await shop.logic.get_available_orders_enabled_page(shop_id, page)

	available_orders = await shop.logic.get_available_orders(shop_id, (page - 1) * buttons_on_page, buttons_on_page)

	print(available_orders)

	orders_cnt = available_orders['available_orders_cnt']
	available_orders = available_orders['data']

	available_orders_buttons = []

	for i in available_orders:
		available_orders_buttons.append([InlineKeyboardButton(text=i['title'], callback_data=f"shop_get_available_order_{i['id']}")])

	max_page = (orders_cnt+buttons_on_page-1) // buttons_on_page

	btn_page_cnt = InlineKeyboardButton(f'{page}/{max_page}', callback_data='empty_callback')

	btn_forward = InlineKeyboardButton('➡', callback_data='shop_available_orders_page_1')
	btn_back = InlineKeyboardButton('⬅', callback_data='shop_available_orders_page_-1')

	if max_page <= 1:
		pass
	elif page == max_page:
		available_orders_buttons.append([btn_back, btn_page_cnt])
	elif page == 1:
		available_orders_buttons.append([btn_page_cnt, btn_forward])
	else:
		available_orders_buttons.append([btn_back, btn_page_cnt, btn_forward])

	available_orders_buttons.append([buttons[language]['shop_menu']])

	return InlineKeyboardMarkup(inline_keyboard=available_orders_buttons)


def get_shop_accept_order_keyboard(order_id, language):
	text = ""
	if language == 'eng':
		text = '↩️Back'

	return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
		text=text,
		callback_data=f"shop_get_available_order_{order_id}")]]
	)


async def get_active_orders(user_id, language, page):
	active_orders = await shop.logic.get_active_orders(user_id, (page - 1) * 10, 10)

	active_orders_buttons = []

	for i in active_orders:
		active_orders_buttons.append([InlineKeyboardButton(text=i, callback_data=f"shop_get_active_order_{i}")])

	active_orders_buttons.append([buttons[language]['shop_menu']])

	return InlineKeyboardMarkup(inline_keyboard=active_orders_buttons)
