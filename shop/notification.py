from aiogram.types import InlineKeyboardMarkup

from .keyboards.buttons import buttons
def get_notification_msg(data, language='eng'):
	if language == 'eng':
		msg = ''
		buttons_to_send = [

		]


		if data['new_available_orders']:
			msg += 'Your shop has new available orders, please check <🚚 Customer requests>\n\n'
			buttons_to_send.append(buttons[language]['notification_to_customer_requests'])
		if data['new_active_orders']:
			msg += 'Your offers were picked by users, please check <🚗 Active orders>\n\n'
			buttons_to_send.append(buttons[language]['notification_to_active_orders'])

		buttons_to_send.append(buttons[language]['notification_to_menu'])

		return msg, InlineKeyboardMarkup(inline_keyboard=buttons_to_send)