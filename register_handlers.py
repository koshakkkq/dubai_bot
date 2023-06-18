from aiogram import Dispatcher
import courier
def register_handlers(dp: Dispatcher):
	dp.register_message_handler(courier.handlers.menu_msg_handler, state='*',commands=['courier'])
	courier.register_handlers(dp)
