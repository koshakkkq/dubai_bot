from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def iter_btns(cars):
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	for car in cars:
		keyboard.row(KeyboardButton(car))
	return keyboard