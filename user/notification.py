from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_notification_msg(data):

	msg = ''
	buttons_to_send = [
	]

	if data['new_offers']:
		msg += 'Your have new unwatched offers from shops, please check <🎯 Your responses>\n\n'
		buttons_to_send.append([InlineKeyboardButton('🎯 Your responses', callback_data=f"feedback")])

	if data['new_couriers']:
		msg += 'Couriers are ready to deliver your order! Please check <💼 My orders>'
		buttons_to_send.append([InlineKeyboardButton('💼 My orders', callback_data=f"my_orders")])

	buttons_to_send.append([InlineKeyboardButton('💬 Menu', callback_data=f"to_menu")])

	return msg, InlineKeyboardMarkup(inline_keyboard=buttons_to_send)