import logging
import typing

import aiogram.types.message

from .decorators_utils import get_current_language, bot_start, get_shop_id

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
		except Exception as e:
			logging.error(e)
		await func(event, state, language)

	return wrapper



def is_member(func):
	async def wrapper(
			event: typing.Union[aiogram.types.message.Message,
			aiogram.types.callback_query.CallbackQuery],
			state,
			language,
	):
		try:
			user_id = int(event['from']['id'])
			shop_id = await get_shop_id(user_id)
			if shop_id is None:
				return
		except Exception as e:
			logging.error(e)
		await func(event, state, language, shop_id)

	return wrapper
