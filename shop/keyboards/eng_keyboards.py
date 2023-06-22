from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

eng_keyboards = {}
menu_buttons = [[InlineKeyboardButton(text='🚚 Customer requests', callback_data='shop_customer_requests')],
				[InlineKeyboardButton(text='📍 Fill out the card', callback_data='shop_info')],
				[InlineKeyboardButton(text='✅ Orders', callback_data='shop_orders')],
				[InlineKeyboardButton(text='🔔 Notifications', callback_data='shop_notifications')]]
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
eng_keyboards['shop_menu'] = menu_keyboard

info_keyboard = [
    [
        InlineKeyboardButton(text='📍 Location', callback_data='shop_change_location'),
        InlineKeyboardButton(text='📲 Phone', callback_data='shop_change_phone')
    ],
[
        InlineKeyboardButton(text='🏢 Name', callback_data='shop_change_location'),
        InlineKeyboardButton(text='💬 Information', callback_data='shop_change_phone')
    ],
    [InlineKeyboardButton(text='Brands and models', callback_data='shop_get_brands')],
    [InlineKeyboardButton(text='↩️ Back', callback_data='shop_menu')],
]
eng_keyboards['shop_info'] = InlineKeyboardMarkup(inline_keyboard=info_keyboard)


available_order_info_keyboard = [
    [InlineKeyboardButton(text='✅ Accept', callback_data='shop_accept_order')],
    [InlineKeyboardButton(text='❌ Decline', callback_data='shop_customer_requests')],
]
eng_keyboards['available_order_info'] = InlineKeyboardMarkup(inline_keyboard=available_order_info_keyboard)

shop_order_finish_keyboard = [
    [InlineKeyboardButton(text='💬 Menu.', callback_data='shop_menu')],
    [InlineKeyboardButton(text='🚚 Customer requests.', callback_data='shop_customer_requests')],
]
eng_keyboards['shop_available_order_finish'] = InlineKeyboardMarkup(inline_keyboard=shop_order_finish_keyboard)