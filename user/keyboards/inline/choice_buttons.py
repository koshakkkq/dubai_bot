from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('🔍 Find a spare part', callback_data=f"find_spare_part")) # strong
	keyboard.row(InlineKeyboardButton('🆘 How to use the bot', callback_data=f"help")) # strong
	keyboard.row(InlineKeyboardButton('🎯 Ваши отклики', callback_data=f"feedback")) # strong
	keyboard.row(InlineKeyboardButton('🔐 Зарегистрировать магазин', callback_data=f"register_store"))
	keyboard.row(InlineKeyboardButton('🚚 Стать курьером', callback_data=f"become_courier"))
	return keyboard


def to_menu():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('↩️ Back to menu', callback_data=f"to_menu"))
	return keyboard


def feedback_menu(): # list pof prices
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('PRICE 1 rating', callback_data=f"price_of"))
	keyboard.row(InlineKeyboardButton('PRICE 2 rating', callback_data=f"price_of"))
	keyboard.row(InlineKeyboardButton('Title 3', callback_data=f"price_of"))
	btn1 = InlineKeyboardButton('More...', callback_data=f"more")
	btn2 = InlineKeyboardButton('⬅️', callback_data=f"to_menu")
	keyboard.row(btn1, btn2)
	return keyboard


def choice_company(): # company onfo
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('✅ Select', callback_data=f"to_delivery_method")) # add id of order
	keyboard.row(InlineKeyboardButton('↩️ Back to selection', callback_data=f"feedback"))
	return keyboard


def delivery_method():
	keyboard = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton('🚚 Delivery', callback_data=f"delivery")
	btn2 = InlineKeyboardButton('📍 Pickup', callback_data=f"pickup")
	keyboard.row(btn1, btn2)
	keyboard.row(InlineKeyboardButton('↩️ Back to selection', callback_data=f"feedback"))
	return keyboard


def pay_btn():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('✅ Paid', callback_data=f"paid"))
	return keyboard


def choice_courier(): # Choose a courier for delivery
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('Courier 1', callback_data=f"courier"))
	keyboard.row(InlineKeyboardButton('Courier 2', callback_data=f"courier"))
	keyboard.row(InlineKeyboardButton('Courier 3', callback_data=f"courier"))
	btn1 = InlineKeyboardButton('More...', callback_data=f"more")
	btn2 = InlineKeyboardButton('⬅️', callback_data=f"to_menu")
	keyboard.row(btn1, btn2)
	return keyboard


def was_deliveried(): # Were you able to pick up your order?
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('✅ Yes', callback_data=f"was_deliveried"))
	keyboard.row(InlineKeyboardButton('❌ No', callback_data=f"wasnt_deliveried"))
	return keyboard


def no_btn(): # Working in filter
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('❌ NO', callback_data=f"user_no_filter"))
	return keyboard


def mark_keyboard():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('5️⃣', callback_data=f"mark"))
	keyboard.row(InlineKeyboardButton('4️⃣', callback_data=f"mark"))
	keyboard.row(InlineKeyboardButton('3️⃣', callback_data=f"mark"))
	keyboard.row(InlineKeyboardButton('2️⃣', callback_data=f"mark"))
	keyboard.row(InlineKeyboardButton('1️⃣', callback_data=f"mark"))
	return keyboard


def language_choice():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('ENG', callback_data=f"eng"))
	keyboard.row(InlineKeyboardButton('RUS', callback_data=f"rus"))
	keyboard.row(InlineKeyboardButton('ARA', callback_data=f"ara"))
	return keyboard