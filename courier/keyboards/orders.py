from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .buttons import buttons

async def get_available_orders_keyboard(user_id: int, current_language: str):
	order_buttons = []

	order_buttons.append([buttons[current_language]['receive_orders']])#todo получать статус курьера(работает или нет)

	order_buttons.append([InlineKeyboardButton(text=f"06.06.2023 Aleksandr", callback_data=f"courier_pick_order_aleksandr")])
	order_buttons.append([buttons[current_language]['courier_menu']])
	return InlineKeyboardMarkup(inline_keyboard=order_buttons)

async def get_delivered_keyboard(user_id:int, current_language: str):
	delivered_buttons = [[InlineKeyboardButton(text=f"06.06.2023 Aleksandr", callback_data=f"pick_delivery_aleksandr")]]

	delivered_buttons.append([buttons[current_language]['courier_menu']])
	return InlineKeyboardMarkup(inline_keyboard=delivered_buttons)
