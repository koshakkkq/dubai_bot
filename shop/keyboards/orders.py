import shop.logic
from .buttons import buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_available_orders(user_id, language, page):
    available_orders = await shop.logic.get_available_orders(user_id, (page-1)*10, 10)

    available_orders_buttons = []

    for i in available_orders:
        available_orders_buttons.append([InlineKeyboardButton(text=i, callback_data=f"shop_get_available_order_{i}")])

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
