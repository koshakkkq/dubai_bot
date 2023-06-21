from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

eng_keyboards = {}
menu_buttons = [[InlineKeyboardButton(text='🚚 Customer requests', callback_data='customer_requests')],
				[InlineKeyboardButton(text='📍 Fill out the card', callback_data='delivered_orders')],
				[InlineKeyboardButton(text='✅ Orders', callback_data='orders')],
				[InlineKeyboardButton(text='🔔 Notifications', callback_data='notifications')]]
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
eng_keyboards['shop_menu'] = menu_keyboard

info_keyboard = [
    [
        InlineKeyboardButton(text='📍 Location', callback_data='change_location'),
        InlineKeyboardButton(text='📲 Phone', callback_data='change_phone')
    ],
[
        InlineKeyboardButton(text='🏢 Name', callback_data='change_location'),
        InlineKeyboardButton(text='💬 Information', callback_data='change_phone')
    ],
    [InlineKeyboardButton(text='Brands and models', callback_data='get_brands')],
    [InlineKeyboardButton(text='↩️ Back', callback_data='back')],
]
eng_keyboards['shop_info'] = InlineKeyboardMarkup(inline_keyboard=info_keyboard)


available_order_info_keyboard = [
    [InlineKeyboardButton(text='✅ Accept', callback_data='accept_order')],
    [InlineKeyboardButton(text='❌ Decline', callback_data='decline_order')],
]
eng_keyboards['available_order_info'] = InlineKeyboardMarkup(inline_keyboard=available_order_info_keyboard)


#shop_order_price
back_keyboard = [
    [InlineKeyboardButton(text='↩️Back', callback_data='back')],
]
eng_keyboards['back'] = InlineKeyboardMarkup(inline_keyboard=back_keyboard)

shop_order_finish_keyboard = [
    [InlineKeyboardButton(text='💬 Menu.', callback_data='menu')],
    [InlineKeyboardButton(text='🚚 Customer requests.', callback_data='customer_requests')],
]
eng_keyboards['shop_available_order_finish'] = InlineKeyboardMarkup(inline_keyboard=shop_order_finish_keyboard)