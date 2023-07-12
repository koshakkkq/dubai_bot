import typing

import aiogram.types.message

from language_selection import get_current_language, bot_start

def picked_language(func):
	async def wrapper(
			event:typing.Union[aiogram.types.message.Message,
			aiogram.types.callback_query.CallbackQuery],
			state
	):#todo а как это можено написать нормально,сделать массив с разрешёнными kwargs?
		user_id = event["from"]["id"]

		language = await get_current_language(user_id)
		if language is None:
			if isinstance(event, aiogram.types.message.Message) is False:
				await event.answer()
				event = event.message
			await bot_start(event)
			return
		await func(event, state, language)
	return wrapper




