from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .buttons import buttons
import shop.logic.cars
from shop.constants import car_brands_buttons_on_page

async def get_brands_keyboard( language: str, page = 1):


	page = await shop.logic.get_brands_page(page)

	brands = await shop.logic.get_brands((page - 1) * car_brands_buttons_on_page,
													   car_brands_buttons_on_page)

	cnt = brands['cnt']
	brands = brands['data']

	return get_keyboard(
		vals=brands,
		orders_cnt=cnt,
		language=language,
		page=page,
		command='brand',
	)



def get_keyboard(vals,orders_cnt , language, page, command):
	orders_buttons = []

	for index, i in enumerate(vals):
		if index%2!=0:
			continue
		if index + 1 == len(vals):
			orders_buttons.append(
				[InlineKeyboardButton(text=i['title'], callback_data=f"shop_info_get_{command}_{i['id']}")])
		else:
			to_append = []
			to_append.append(
				InlineKeyboardButton(text=i['title'], callback_data=f"shop_info_get_{command}_{i['id']}"))
			i = vals[index+1]
			to_append.append(
				InlineKeyboardButton(text=i['title'], callback_data=f"shop_info_get_{command}_{i['id']}"))
			orders_buttons.append(to_append)

	max_page = (orders_cnt + car_brands_buttons_on_page - 1) // car_brands_buttons_on_page

	btn_page_cnt = InlineKeyboardButton(f'{page}/{max_page}', callback_data='empty_callback')

	btn_forward = InlineKeyboardButton('➡', callback_data=f'shop_info_{command}_orders_page_1')
	btn_back = InlineKeyboardButton('⬅', callback_data=f'shop_info_{command}_orders_page_-1')

	if max_page <= 1:
		pass
	elif page == max_page:
		orders_buttons.append([btn_back, btn_page_cnt])
	elif page == 1:
		orders_buttons.append([btn_page_cnt, btn_forward])
	else:
		orders_buttons.append([btn_back, btn_page_cnt, btn_forward])

	orders_buttons.append([buttons[language]['shop_info_back']])

	return InlineKeyboardMarkup(inline_keyboard=orders_buttons)

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

	models_buttons.append([buttons[current_language]['shop_get_brands']])

	return InlineKeyboardMarkup(inline_keyboard=models_buttons)