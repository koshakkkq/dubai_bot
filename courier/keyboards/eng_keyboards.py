from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
eng_keyboards = {}
menu_buttons = [[InlineKeyboardButton(text='🚚 Available orders', callback_data='courier_available_orders_begin')],
				[InlineKeyboardButton(text='⚡️ Active orders', callback_data='courier_active_orders_begin')],
				[InlineKeyboardButton(text='✅ Done orders', callback_data='courier_done_orders_begin')],
				[InlineKeyboardButton(text='💼 Your information.', callback_data='courier_info')],
				[InlineKeyboardButton(text='🆘 Help', callback_data='empty_callback')],
				[InlineKeyboardButton(text='️↩️ To main menu', callback_data='to_menu')],
				]

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
eng_keyboards['courier_menu'] = menu_keyboard



order_info_buttons = [
	[InlineKeyboardButton(text='❌ Reject order.', callback_data='courier_available_order_reject')],
	[InlineKeyboardButton(text='↩️ Back', callback_data='courier_available_orders_begin')]]

order_info_keyboard = InlineKeyboardMarkup(inline_keyboard=order_info_buttons)
eng_keyboards['available_order_info'] = order_info_keyboard


to_client_menu = [
	[InlineKeyboardButton(text='↩️ Back', callback_data='to_menu')]]

eng_keyboards['to_client_menu'] = InlineKeyboardMarkup(inline_keyboard=to_client_menu)

code_correct = [
    [InlineKeyboardButton(text='✅Next step.', callback_data='register_courier')]
]

eng_keyboards['code_correct'] = InlineKeyboardMarkup(inline_keyboard=code_correct)


back_to_courier_info = [
	[InlineKeyboardButton(text='↩️ Back', callback_data='courier_info')]
]
eng_keyboards['back_to_courier_info'] = InlineKeyboardMarkup(inline_keyboard=back_to_courier_info)


change_information = [
	[InlineKeyboardButton(text='📋 Name', callback_data='courier_change_name')],
	[InlineKeyboardButton(text='📱 Phone', callback_data='courier_change_phone')],
	[InlineKeyboardButton(text=f"↩️ Back", callback_data=f"courier_menu")],
]
eng_keyboards['change_information'] = InlineKeyboardMarkup(inline_keyboard=change_information)


available_order_finish = [
	[InlineKeyboardButton(text='↩️ To available orders', callback_data='courier_available_orders_begin')],
	[InlineKeyboardButton(text='⚡️ Active orders', callback_data='courier_active_orders_begin')],
]

eng_keyboards['available_order_finish'] = InlineKeyboardMarkup(inline_keyboard=available_order_finish)


active_orders_finish = [
[InlineKeyboardButton(text=f"↩️ Back", callback_data=f"courier_active_orders_begin")],
]
eng_keyboards['active_orders_finish'] = InlineKeyboardMarkup(inline_keyboard=active_orders_finish)


done_orders_finish = [
[InlineKeyboardButton(text=f"↩️ Back", callback_data=f"courier_done_orders_begin")],
]
eng_keyboards['done_orders_finish'] = InlineKeyboardMarkup(inline_keyboard=done_orders_finish)