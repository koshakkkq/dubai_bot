import shop.logic
from .buttons import buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_available_orders(user_id, language, page):
    available_orders = await shop.logic.get_available_orders(user_id, (page-1)*10, 10)

    available_orders_buttons = []

    for i in available_orders:
        available_orders_buttons.append([InlineKeyboardButton(text=i, callback_data=f"get_order_{i}")])

    available_orders_buttons.append([buttons[language]['back']])


    return InlineKeyboardMarkup(inline_keyboard=available_orders_buttons)
