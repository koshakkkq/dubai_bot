import logging
import typing

import aiogram.types.message

from language_selection import get_current_language, bot_start

def picked_language(func):
	async def wrapper(
			event:typing.Union[aiogram.types.message.Message,
			aiogram.types.callback_query.CallbackQuery],
			state
	):
		try:
			user_id = int(event["from"]["id"])

			language = await get_current_language(user_id)
			if language is None:
				if isinstance(event, aiogram.types.message.Message) is False:
					await event.answer()
					event = event.message
				await bot_start(event)
				return
			await func(event, state, language)
		except Exception as e:
			logging.error(e)
	return wrapper




