import logging

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from db.sessions import get_session
from sqlalchemy import select
from db.models import User
from sqlalchemy.orm.exc import NoResultFound

async def get_current_language(user_id: str):
	async with get_session() as async_session:
		stmt = select(User).where(User.telegram_id == user_id)
		try:
			res = await async_session.execute(stmt)
		except Exception as e:
			logging.error(e)
			return None

		language = None
		try:
			user = res.scalar_one()

			language = user.language
		except NoResultFound:
			async_session.add_all([
				User(telegram_id=user_id, language=None)
			])


		try:
			await async_session.commit()
		except Exception as e:
			logging.error(e)
		return language

async def set_language(user_id, language):
	async with get_session() as async_session:
		stmt = select(User).where(User.telegram_id == user_id)
		try:
			res = await async_session.execute(stmt)
		except Exception as e:
			logging.error(e)


		try:
			user = res.scalar_one()
			user.language = language
		except NoResultFound:
			async_session.add(User(telegram_id=user_id, language=language))

		try:
			await async_session.commit()
		except Exception as e:
			logging.error(e)


async def bot_start(message: Message):

	await message.answer(f"Hello, {message.from_user.full_name}!\nChoose language!", reply_markup=language_choice())


def language_choice():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('ENG', callback_data=f"pick_language_eng"))
	keyboard.row(InlineKeyboardButton('RUS', callback_data=f"pick_language_rus"))
	keyboard.row(InlineKeyboardButton('ARA', callback_data=f"pick_language_ara"))
	return keyboard