import shop.handlers
from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    shop.handlers.shop_menu.register_handlers(dp)

    shop.handlers.shop_info.register_handlers(dp)
