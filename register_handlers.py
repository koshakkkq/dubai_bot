from aiogram import Dispatcher
from courier.handlers.courier_menu import menu_msg_handler as courier_menu
from shop.handlers.shop_menu import menu_msg_handler
def register_handlers(dp: Dispatcher):
	dp.register_message_handler(courier_menu, state='*',commands=['courier'])
	dp.register_message_handler(menu_msg_handler, state='*', commands=['account'])
