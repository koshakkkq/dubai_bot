from loader import bot
from user.keyboards import inline


async def send_message_of_interest(user_id, shop_id):
	message = "Good afternoon.\nWere you able to pick up your order?"
	await bot.send_message(user_id, message, reply_markup=inline.was_deliveried(shop_id))