import courier.handlers
from aiogram import Dispatcher

def register_handlers(dp: Dispatcher):

	courier.handlers.courier_menu.register_handlers(dp)
