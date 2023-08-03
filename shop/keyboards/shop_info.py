from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .buttons import buttons
import shop.logic.cars
from shop.constants import car_brands_buttons_on_page, car_models_buttons_on_page

async def get_brands_keyboard(shop_id, language: str, page = 1):


	#page = await shop.logic.get_brands_page(page)

	brands = await shop.logic.get_brands(shop_id, (page - 1) * car_brands_buttons_on_page,
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

	btn_forward = InlineKeyboardButton('➡', callback_data=f'shop_info_{command}_page_1')
	btn_back = InlineKeyboardButton('⬅', callback_data=f'shop_info_{command}_page_-1')

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

async def get_models_keyboard(shop_id, brand_id, language: str, page = 1):
	data = await shop.logic.cars.get_models_by_brand(
		shop_id=shop_id,
		brand_id=brand_id,
		skip=(page-1)*car_models_buttons_on_page,
		limit=car_models_buttons_on_page,
	)
	orders_buttons = []

	vals = data['data']
	cnt = data['cnt']

	for index, i in enumerate(vals):
		orders_buttons.append(
			[InlineKeyboardButton(text=i['title'], callback_data=i['callback_data'])])


	max_page = (cnt + car_models_buttons_on_page - 1) // car_models_buttons_on_page

	btn_page_cnt = InlineKeyboardButton(f'{page}/{max_page}', callback_data='empty_callback')

	btn_forward = InlineKeyboardButton('➡', callback_data=f'shop_info_model_page_1')
	btn_back = InlineKeyboardButton('⬅', callback_data=f'shop_info_model_page_-1')

	if max_page <= 1:
		pass
	elif page == max_page:
		orders_buttons.append([btn_back, btn_page_cnt])
	elif page == 1:
		orders_buttons.append([btn_page_cnt, btn_forward])
	else:
		orders_buttons.append([btn_back, btn_page_cnt, btn_forward])

	orders_buttons.append([buttons[language]['pick_all_models']])
	orders_buttons.append([buttons[language]['unpick_all_models']])
	orders_buttons.append([buttons[language]['pick_page_models']])
	orders_buttons.append([buttons[language]['unpick_page_models']])

	orders_buttons.append([buttons[language]['shop_get_brands']])

	return InlineKeyboardMarkup(inline_keyboard=orders_buttons)

async def get_parts_keyboard(shop_id, language):
	orders_buttons = []

	vals = await shop.logic.get_parts(shop_id)
	vals = vals['data']

	for index, i in enumerate(vals):
		orders_buttons.append(
			[InlineKeyboardButton(text=i['title'], callback_data=i['callback_data'])])

	orders_buttons.append([buttons[language]['shop_info_back']])

	return InlineKeyboardMarkup(inline_keyboard=orders_buttons)