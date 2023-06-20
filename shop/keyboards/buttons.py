from collections import defaultdict

from aiogram.types import InlineKeyboardButton

buttons = defaultdict(lambda: {})
buttons['eng']['back'] = InlineKeyboardButton(text=f"↩️ Back", callback_data=f"back")

buttons['eng']['pick_all_models'] = InlineKeyboardButton(text=f"Select all models", callback_data="pick_all_models")
buttons['eng']['pick_page_models'] = InlineKeyboardButton(
	text=f"Select all models on page",
	callback_data="pick_page_models",
)
