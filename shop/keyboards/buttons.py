from collections import defaultdict

from aiogram.types import InlineKeyboardButton

buttons = defaultdict(lambda: {})
buttons['eng']['shop_menu'] = InlineKeyboardButton(text=f"↩️ Back", callback_data="shop_menu")

buttons['eng']['shop_info_back'] = InlineKeyboardButton(text=f"↩️ Back", callback_data="shop_info")

buttons['eng']['shop_get_brands'] = InlineKeyboardButton(text=f"↩️ Back", callback_data="shop_get_brands")


buttons['eng']['pick_all_models'] = InlineKeyboardButton(text=f"Select all models", callback_data="pick_all_models")
buttons['eng']['pick_page_models'] = InlineKeyboardButton(
	text=f"Select all models on page",
	callback_data="pick_page_models",
)
