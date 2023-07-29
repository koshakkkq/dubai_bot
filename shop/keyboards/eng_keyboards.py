from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

eng_keyboards = {}
menu_buttons = [[InlineKeyboardButton(text='🚚 Customer requests', callback_data='shop_customer_requests')],
				[InlineKeyboardButton(text='🚗 Active orders', callback_data='shop_active_orders')],
                [InlineKeyboardButton(text='✅ Done orders', callback_data='shop_done_orders')],
                [InlineKeyboardButton(text='📍 Shop information', callback_data='shop_info')],
                [InlineKeyboardButton(text='↩️ To main menu', callback_data='to_menu')],
                ]
menu_keyboard = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
eng_keyboards['shop_menu'] = menu_keyboard

info_keyboard = [
    [
        InlineKeyboardButton(text='📍 Location', callback_data='shop_change_location'),
        InlineKeyboardButton(text='📱 Change geolocation', callback_data='shop_change_coords'),
    ],
    [
        InlineKeyboardButton(text='📲 Phone', callback_data='shop_change_phone'),
        InlineKeyboardButton(text='🏢 Name', callback_data='shop_change_name'),
    ],
    [InlineKeyboardButton(text='🚗 Brands and models', callback_data='shop_get_brands')],
    [InlineKeyboardButton(text='➕ Get invite code for employee', callback_data='shop_info_create_invite')],
    [InlineKeyboardButton(text='↩️ Back', callback_data='shop_menu')],
]
eng_keyboards['shop_info'] = InlineKeyboardMarkup(inline_keyboard=info_keyboard)


available_order_info_keyboard = [
    [InlineKeyboardButton(text='❌ Decline', callback_data='shop_order_decline')],
    [InlineKeyboardButton(text='🚚 Customer requests.', callback_data='shop_customer_requests')],
]
eng_keyboards['available_order_info'] = InlineKeyboardMarkup(inline_keyboard=available_order_info_keyboard)

shop_order_finish_keyboard = [
    [InlineKeyboardButton(text='💬 Menu.', callback_data='shop_menu')],
    [InlineKeyboardButton(text='🚚 Customer requests.', callback_data='shop_customer_requests')],
]
eng_keyboards['shop_available_order_finish'] = InlineKeyboardMarkup(inline_keyboard=shop_order_finish_keyboard)



shop_active_order_info_keyboard = [
    [InlineKeyboardButton(text='✅ Order is completed', callback_data='shop_active_order_status_done')],
    [InlineKeyboardButton(text='❌ Order cancelled', callback_data='shop_active_order_status_cancel')],
    [InlineKeyboardButton(text='↩️ Back', callback_data='shop_active_orders')]
]
eng_keyboards['shop_active_order_info'] = InlineKeyboardMarkup(inline_keyboard=shop_active_order_info_keyboard)

back_to_menu = [
    [InlineKeyboardButton(text='💬 Menu.', callback_data='to_menu')],
]
eng_keyboards['to_client_menu'] = InlineKeyboardMarkup(inline_keyboard=back_to_menu)


code_correct = [
    [InlineKeyboardButton(text='✅Next step.', callback_data='register_store')]
]

eng_keyboards['code_correct'] = InlineKeyboardMarkup(inline_keyboard=code_correct)

code_incorrect = [
    [InlineKeyboardButton(text='↩️Try again.', callback_data='register_store')]
]

eng_keyboards['code_incorrect'] = InlineKeyboardMarkup(inline_keyboard=code_incorrect)


shop_active_order_finish = [
    [InlineKeyboardButton(text='💬 Menu.', callback_data='shop_menu')],
    [InlineKeyboardButton(text='🚗 Active orders', callback_data='shop_active_orders')],
]

eng_keyboards['shop_active_order_finish'] = InlineKeyboardMarkup(inline_keyboard=shop_active_order_finish)

shop_done_order_info_keyboard = [
    [InlineKeyboardButton(text='↩️ Back', callback_data='shop_done_orders')]
]
eng_keyboards['shop_done_order_info'] = InlineKeyboardMarkup(inline_keyboard=shop_done_order_info_keyboard)


shop_back_from_change = [
    [InlineKeyboardButton(text='↩️ Back', callback_data='shop_info')]
]
eng_keyboards['shop_back_from_change'] = InlineKeyboardMarkup(inline_keyboard=shop_back_from_change)


