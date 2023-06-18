from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
eng_keyboards = {}
menu_buttons = [[InlineKeyboardButton(text='🚚 Available orders', callback_data='available_orders')],
				[InlineKeyboardButton(text='⚡️ Delivered orders', callback_data='delivered_orders')],
				[InlineKeyboardButton(text='🆘 Help', callback_data='empty_callback')]]
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
eng_keyboards['menu'] = menu_keyboard



order_info_buttons = [
	[InlineKeyboardButton(text='✅ Take order', callback_data='pick_order')],
	[InlineKeyboardButton(text='↩️ Back', callback_data='back')]]

order_info_keyboard = InlineKeyboardMarkup(inline_keyboard=order_info_buttons)
eng_keyboards['order_info'] = order_info_keyboard
