from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbacks import IterCallback


def menu():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('🔍 Find a spare part', callback_data=f"find_spare_part")) # strong
	keyboard.row(InlineKeyboardButton('🆘 How to use the bot', callback_data=f"help")) # strong
	keyboard.row(InlineKeyboardButton('🎯 Your responses', callback_data=f"feedback")) # strong
	keyboard.row(InlineKeyboardButton('💼 My orders', callback_data=f"my_orders")) # strong
	keyboard.row(InlineKeyboardButton('🔐 Store menu.', callback_data=f"register_store"))
	keyboard.row(InlineKeyboardButton('🚚 Courier menu.', callback_data=f"register_courier"))
	return keyboard


def to_menu():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('↩️ Back to menu', callback_data=f"to_menu"))
	return keyboard


def feedback_menu(): # list pof prices
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('PRICE 1 rating', callback_data=f"price_of"))
	keyboard.row(InlineKeyboardButton('PRICE 2 rating', callback_data=f"price_of"))
	keyboard.row(InlineKeyboardButton('Title 3', callback_data=f"price_of"))
	btn1 = InlineKeyboardButton('More...', callback_data=f"more")
	btn2 = InlineKeyboardButton('↩️', callback_data=f"to_menu")
	keyboard.row(btn1, btn2)
	return keyboard


def choice_company(): # company onfo
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('✅ Select', callback_data=f"to_delivery_method")) # add id of order
	keyboard.row(InlineKeyboardButton('↩️ Back to selection', callback_data=f"feedback"))
	return keyboard


def delivery_method():
	keyboard = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton('🚚 Delivery', callback_data=f"delivery")
	btn2 = InlineKeyboardButton('📍 Pickup', callback_data=f"pickup")
	keyboard.row(btn1, btn2)
	keyboard.row(InlineKeyboardButton('↩️ Back to selection', callback_data=f"feedback"))
	return keyboard


def pay_btn():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('✅ Paid', callback_data=f"paid"))
	return keyboard


def choice_courier(): # Choose a courier for delivery
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('Courier 1', callback_data=f"courier"))
	keyboard.row(InlineKeyboardButton('Courier 2', callback_data=f"courier"))
	keyboard.row(InlineKeyboardButton('Courier 3', callback_data=f"courier"))
	btn1 = InlineKeyboardButton('More...', callback_data=f"more")
	btn2 = InlineKeyboardButton('↩️', callback_data=f"to_menu")
	keyboard.row(btn1, btn2)
	return keyboard


def was_deliveried(shop_id, order_id): # Were you able to pick up your order?
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('✅ Yes', callback_data=f"was_deliveried:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('❌ No', callback_data=f"wasnt_deliveried:{shop_id}:{order_id}"))
	return keyboard


def no_btn(): # Working in filter
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('❌ NO', callback_data=f"user_no_filter"))
	callback_data = IterCallback(current_page=0, action="previous_state").pack()
	keyboard.row(InlineKeyboardButton("↩️ Back", callback_data=callback_data))
	return keyboard


def mark_keyboard(shop_id, order_id):
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('5️⃣', callback_data=f"mark:5:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('4️⃣', callback_data=f"mark:4:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('3️⃣', callback_data=f"mark:3:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('2️⃣', callback_data=f"mark:2:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('1️⃣', callback_data=f"mark:1:{shop_id}:{order_id}"))
	return keyboard

def courier_mark_keyboard(shop_id, order_id):
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('5️⃣', callback_data=f"courier_mark:5:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('4️⃣', callback_data=f"courier_mark:4:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('3️⃣', callback_data=f"courier_mark:3:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('2️⃣', callback_data=f"courier_mark:2:{shop_id}:{order_id}"))
	keyboard.row(InlineKeyboardButton('1️⃣', callback_data=f"courier_mark:1:{shop_id}:{order_id}"))


	return keyboard



def language_choice():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('ENG', callback_data=f"pick_language_eng"))
	keyboard.row(InlineKeyboardButton('RUS', callback_data=f"pick_language_rus"))
	keyboard.row(InlineKeyboardButton('ARA', callback_data=f"pick_language_ara"))
	return keyboard


def iter_btns(items, current_page=0, pagination=27): # paggination % 3 == 0 !
	keyboard = InlineKeyboardMarkup()
	length = len(items)
	pages = length // pagination + bool(length % pagination) # if this value > 0 than return 1 else 0
	btns = []
	data = []
	for i, (key, val) in enumerate(items.items(), 0):
		callback_data = IterCallback(current_page=current_page, action=val).pack()
		btns.append(InlineKeyboardButton(key, callback_data=callback_data))
		if i % pagination == pagination - 1:
			data.append(btns)
			btns = []
	if length % pagination != pagination - 1:
		data.append(btns)
		btns = []
	keyboard.add(*data[current_page])
	if current_page > 0:
		callback_data = IterCallback(current_page=current_page, action="back").pack()
		btns.append(InlineKeyboardButton('⬅️', callback_data=callback_data))
	callback_data = IterCallback(current_page=1, action="back").pack()
	if pages > 1:
		btns.append(InlineKeyboardButton(f'{current_page+1}/{pages}', callback_data=callback_data)) # Pages 10/12
	if current_page != pages - 1:
		callback_data = IterCallback(current_page=current_page+2, action="back").pack()
		btns.append(InlineKeyboardButton('➡️', callback_data=callback_data))
	keyboard.add(*btns)
	callback_data = IterCallback(current_page=current_page, action="previous_state").pack()
	keyboard.row(InlineKeyboardButton("↩️ Back", callback_data=callback_data))
	return keyboard


def tuple_btns(tuple):
	keyboard = InlineKeyboardMarkup()
	for i in tuple:
		callback_data = IterCallback(current_page=0, action=i).pack()
		keyboard.row(InlineKeyboardButton(i, callback_data=callback_data))
	callback_data = IterCallback(current_page=0, action="previous_state").pack()
	keyboard.row(InlineKeyboardButton("↩️ Back", callback_data=callback_data))
	return keyboard


def one_page_iter_btns(dct, pages, current_page=0):
	keyboard = InlineKeyboardMarkup()
	btns = []
	for offer_id, string in dct.items():
		callback_data = IterCallback(current_page=current_page, action=str(offer_id)).pack()
		keyboard.row(InlineKeyboardButton(string, callback_data=callback_data))

	if current_page > 0:
		callback_data = IterCallback(current_page=current_page, action="back").pack()
		btns.append(InlineKeyboardButton("⬅️", callback_data=callback_data))
	if pages > 1:
		callback_data = IterCallback(current_page=1, action="back").pack()
		btns.append(InlineKeyboardButton(f'{current_page+1}/{pages}', callback_data=callback_data)) # Pages 10/12
	if current_page != pages - 1:
		callback_data = IterCallback(current_page=current_page+2, action="back").pack()
		btns.append(InlineKeyboardButton("➡️", callback_data=callback_data))
	keyboard.add(*btns)
	keyboard.row(InlineKeyboardButton('↩️ Back to menu', callback_data=f"to_menu"))
	return keyboard


def my_order_btns(orders, current_page=0):
	pages = len(orders)
	order = orders[current_page]
	shop_id = order['offer']["shop"]
	keyboard = InlineKeyboardMarkup()
	print(order)
	if order['status']['id'] == 1:
		if order['can_pick_courier'] == False:
			keyboard.row(InlineKeyboardButton("✅ received", callback_data=f"was_deliveried:{shop_id}:{order['id']}"))
		if order['can_pick_courier'] is True:
			keyboard.row(InlineKeyboardButton('Offers from couriers', callback_data=f'courier_offers:{order["id"]}'))

	btns = []
	if current_page > 0:
		btns.append(InlineKeyboardButton("⬅️", callback_data=f"myorder_back:{current_page}"))
	if pages > 1:
		btns.append(InlineKeyboardButton(f'{current_page+1}/{pages}', callback_data=f'myorder_back:1')) # Pages 10/12
	if current_page != pages - 1:
		btns.append(InlineKeyboardButton("➡️", callback_data=f'myorder_back:{current_page+2}'))
	keyboard.add(*btns)
	keyboard.row(InlineKeyboardButton('↩️ Back to menu', callback_data=f"to_menu"))
	return keyboard


def back_to_pickup_selecton():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('↩️ Back', callback_data=f"to_delivery_method_addres_state"))
	return keyboard


def my_orders():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('💼 My orders', callback_data=f"my_orders")) # strong
	keyboard.row(InlineKeyboardButton('↩️ Back to menu', callback_data=f"to_menu"))
	return keyboard



def courier_selection_btns(data):
	keyboard = InlineKeyboardMarkup()
	for key, val in data.items():
		keyboard.row(InlineKeyboardButton(f'{val}', callback_data=f"order_offer_pick:{key}"))
	keyboard.row(InlineKeyboardButton('↩️ Back', callback_data=f"my_orders"))
	return keyboard