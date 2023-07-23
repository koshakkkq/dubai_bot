from aiogram import Dispatcher
from courier.handlers.register import courier_registration_proceed
from shop.handlers.shop_creation import shop_begin_registration
def register_handlers(dp: Dispatcher):
	dp.register_message_handler(courier_registration_proceed, state='*',commands=['courier'])
	dp.register_message_handler(shop_begin_registration, state='*', commands=['account'])
