from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
eng_keyboards = {}
menu_buttons = [[InlineKeyboardButton(text='🚚 Available orders', callback_data='courier_available_orders')],
				[InlineKeyboardButton(text='⚡️ Delivered orders', callback_data='courier_delivered_orders')],
				[InlineKeyboardButton(text='🆘 Help', callback_data='empty_callback')],
				[InlineKeyboardButton(text='️↩️ To main menu', callback_data='to_menu')]]

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
eng_keyboards['courier_menu'] = menu_keyboard



order_info_buttons = [
	[InlineKeyboardButton(text='✅ Take order', callback_data='courier_choose_order')],
	[InlineKeyboardButton(text='↩️ Back', callback_data='courier_available_orders')]]

order_info_keyboard = InlineKeyboardMarkup(inline_keyboard=order_info_buttons)
eng_keyboards['order_info'] = order_info_keyboard


to_client_menu = [
	[InlineKeyboardButton(text='↩️ Back', callback_data='to_menu')]]

eng_keyboards['to_client_menu'] = InlineKeyboardMarkup(inline_keyboard=to_client_menu)

code_correct = [
    [InlineKeyboardButton(text='✅Next step.', callback_data='register_courier')]
]

eng_keyboards['code_correct'] = InlineKeyboardMarkup(inline_keyboard=code_correct)