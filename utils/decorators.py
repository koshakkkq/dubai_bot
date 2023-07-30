import logging
import typing

import aiogram.types.message

from .decorators_utils import get_current_language, bot_start, get_shop_id, get_courier_id, delete_msg

def picked_language(func):
	async def wrapper(
			*args,
			state=None,
	):
		try:
			event = None
			real_args = []
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
				elif isinstance(i, aiogram.dispatcher.storage.FSMContext):
					state = i
				else:
					real_args.append(i)
			user_id = int(event["from"]["id"])

			language = await get_current_language(user_id)
			if language is None:
				if isinstance(event, aiogram.types.message.Message) is False:
					await event.answer()
					event = event.message
				await bot_start(event, state)
				return
		except Exception as e:
			logging.error(e)
			return
		await func(*real_args,event, state=state, language=language)
	return wrapper



def is_member(func):
	async def wrapper(
			*args,
			state=None,
			language=None
	):
		try:
			real_args = []
			event = None
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
				elif isinstance(i, aiogram.dispatcher.storage.FSMContext):
					state = i
				else:
					real_args.append(i)

			event = None
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
					break

			user_id = int(event['from']['id'])
			shop_id = await get_shop_id(user_id)
			if shop_id is None:
				return
		except Exception as e:
			logging.error(e)
			return
		await func(*real_args,event,state, language=language, shop_id=shop_id)

	return wrapper


def delete_msg_decorator(func):
	async def wrapper(
			*args,
			state=None,
			language=None,
			**kwargs,
	):
		try:
			real_args = []
			event = None
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
				elif isinstance(i, aiogram.dispatcher.storage.FSMContext):
					state = i
				else:
					real_args.append(i)

			event = None
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
					break

			user_id = int(event['from']['id'])
			await delete_msg(tg_id=user_id)
		except Exception as e:
			logging.error(e)
			return
		await func(*real_args,event,state, language, **kwargs)

	return wrapper


def is_courier(func):
	async def wrapper(
			*args,
			state=None,
			language=None
	):
		try:
			real_args = []
			event = None
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
				elif isinstance(i, aiogram.dispatcher.storage.FSMContext):
					state = i
				else:
					real_args.append(i)

			event = None
			for i in args:
				if isinstance(i, aiogram.types.CallbackQuery) or isinstance(i, aiogram.types.Message):
					event = i
					break

			user_id = int(event['from']['id'])
			courier_id = await get_courier_id(user_id)
			if courier_id is None:
				return
		except Exception as e:
			logging.error(e)
			return
		await func(*real_args,event,state, language=language, courier_id=courier_id)

	return wrapper
