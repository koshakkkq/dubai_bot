from collections import defaultdict

from aiogram.types import InlineKeyboardButton

buttons = defaultdict(lambda :{})
buttons['eng']['back'] = InlineKeyboardButton(text=f"↩️ Back", callback_data=f"back" )

buttons['eng']['courier_menu'] = InlineKeyboardButton(text=f"↩️ Back", callback_data=f"courier_menu" )

buttons['eng']['receive_orders'] = InlineKeyboardButton(text=f"Receive orders ✅", callback_data="receive_orders")
buttons['eng']['decline_orders'] = InlineKeyboardButton(text=f"Don't receive orders ❌", callback_data="decline_orders")