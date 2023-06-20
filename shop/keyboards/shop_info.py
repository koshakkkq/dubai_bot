from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .buttons import buttons
import shop.logic.cars


async def get_brands_keyboard(user_id: int, current_language: str, page = 1):
	all_brands = await shop.logic.cars.get_all_brands(
		skip=(page-1)*10,
		limit=10
	)  # тут id будут {"id":1, "name":mazda"} ну или как - то так

	brands_buttons = []

	for i in all_brands:
		brands_buttons.append([InlineKeyboardButton(text=i, callback_data=f'pick_brand_{i}')])

	brands_buttons.append([buttons[current_language]['back']])

	return InlineKeyboardMarkup(inline_keyboard=brands_buttons)


async def get_models_keyboard(user_id, brand_id, current_language: str, page = 1):
	all_models = await shop.logic.cars.get_models_by_brand(
		brand_id=brand_id,
		skip=(page-1)*10,
		limit=10
	)#по 10 на странице.
	print(all_models)

	models_buttons = []
	for i in all_models:
		model_picked = await shop.logic.cars.is_model_picked(
			model_id=i,
			user_id=user_id,
		)
		if model_picked == True:
				models_buttons.append([
					InlineKeyboardButton(
						text=f'{i}✅', callback_data=f'unpick_model_{i}'
					)
				])
		else:
			models_buttons.append([
				InlineKeyboardButton(
					text=f'{i}❌', callback_data=f'pick_model_{i}'
				)
			])

	models_buttons.append([buttons[current_language]['pick_all_models']])
	models_buttons.append([buttons[current_language]['pick_page_models']])

	models_buttons.append([buttons[current_language]['back']])

	return InlineKeyboardMarkup(inline_keyboard=models_buttons)