from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import ResponseStates
from user.keyboards import inline, reply
from utils import api
from user.keyboards.inline.callbacks import IterCallback
from user.utils import send_message_of_interest


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="back"), state=ResponseStates.PRICE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page - 1

    orders = await api.get_orders(call.message.chat.id, 0)
    pages = len(orders)
    order = orders[current_page]
    async with state.proxy() as data:
        text = order["model"] + '\n' + order["additional"]
        offers = {offer["id"]: f'Price: {offer["price"]}, raiting: {round(offer["raiting"], 2)}' for offer in order["offers"]}
    await call.message.edit_text(text=text, reply_markup=inline.one_page_iter_btns(offers, pages, current_page))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(), state=ResponseStates.PRICE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page
    offer_id = int(callback.action)
    orders = await api.get_orders(call.message.chat.id, 0)
    pages = len(orders)
    order = orders[current_page]
    offer = None
    for i in order["offers"]:
        if i["id"] == offer_id:
            offer = i
    name = offer["shop"]["name"]
    location = offer["shop"]["location"]
    phone = offer["shop"]["phone"]
    async with state.proxy() as data:
        data["offer_id"] = offer_id
        data["name"] = name
        data["location"] = location
        data["phone"] = phone
        data["price"] = offer['price']
        data["order_id"] = order["id"]
    await call.message.edit_text(text=f"{name}\n{location}\n{phone}\n\n{offer['price']}\n\n" + "Choose your next action ⤵️",
        reply_markup=inline.choice_company())


@dp.callback_query_handler(lambda call: "to_delivery_method" == call.data, state=ResponseStates.PRICE_STATE)
async def to_delivery_method(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    name = state_data["name"]
    location = state_data["location"]
    phone = state_data["phone"]
    price = state_data["price"]
    await call.message.edit_text(text=f"Shop name: {name}\nShop location: {location}\nShop phone: {phone}\n{price}\n\n" + "Choose your next action ⤵️", 
        reply_markup=inline.delivery_method())


@dp.callback_query_handler(lambda call: "pickup" == call.data, state=ResponseStates.PRICE_STATE)
async def find_spare_part(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order_id = state_data['order_id']
    offer_id = state_data["offer_id"]
    status = await api.order_update(order_id, offer_id, status=1, is_delivery=False)
    await call.message.edit_text("Congratulations!\n\nAddress: ...\nYour order number: " + str(state_data["order_id"]), 
        reply_markup=None)
    await send_message_of_interest(call.message.chat.id)


@dp.callback_query_handler(lambda call: "delivery" == call.data, state=ResponseStates.PRICE_STATE)
async def price_of(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Write your shipping address", reply_markup=None)
    await ResponseStates.ADDRESS_STATE.set()


@dp.message_handler(state=ResponseStates.ADDRESS_STATE)
async def text_msg(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
    await message.answer(f"Your address: {message.text}\n*purchase*\n\nthrough Stripe", reply_markup=inline.pay_btn())
    await ResponseStates.STRIPE_STATE.set()


@dp.callback_query_handler(lambda call: "paid" == call.data, state=ResponseStates.STRIPE_STATE)
async def price_f(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order_id = state_data['order_id']
    offer_id = state_data["offer_id"]
    address = state_data["address"]
    status = await api.order_update(order_id, offer_id, status=1, address=address, is_delivery=True)
    await call.message.edit_text("Congratulations!\nTomorrow your goods will be delivered to you", reply_markup=None)
    await send_message_of_interest(call.message.chat.id)