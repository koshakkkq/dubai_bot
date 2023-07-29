from collections import defaultdict

from aiogram.types import InlineKeyboardButton

buttons = defaultdict(lambda: {})
buttons['eng']['shop_menu'] = InlineKeyboardButton(text=f"↩️ Back", callback_data="shop_menu")

buttons['eng']['shop_info_back'] = InlineKeyboardButton(text=f"↩️ Back", callback_data="shop_info")

buttons['eng']['shop_get_brands'] = InlineKeyboardButton(text=f'✅ OK', callback_data="shop_get_brands")


buttons['eng']['pick_all_models'] = InlineKeyboardButton(text=f"Select all models", callback_data="shop_info_pick_all_models_1")
buttons['eng']['unpick_all_models'] = InlineKeyboardButton(text=f"Unselect all models", callback_data="shop_info_pick_all_models_0")

buttons['eng']['pick_page_models'] = InlineKeyboardButton(
	text=f"Select all models on page",
	callback_data="shop_info_pick_page_models_1",
)

buttons['eng']['unpick_page_models'] = InlineKeyboardButton(
	text=f"Unselect all models on page",
	callback_data="shop_info_pick_page_models_0",
)