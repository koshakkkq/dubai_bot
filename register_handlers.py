from aiogram import Dispatcher
import courier
import shop
def register_handlers(dp: Dispatcher):
	dp.register_message_handler(courier.handlers.menu_msg_handler, state='*',commands=['courier'])
	dp.register_message_handler(shop.handlers.menu_msg_handler, state='*', commands=['account'])
	courier.register_handlers(dp)
	shop.register_handlers(dp)

