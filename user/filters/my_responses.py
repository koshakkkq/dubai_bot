from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import ResponseStates, AddressStates
from user.keyboards import inline, reply
from utils import api
from user.keyboards.inline.callbacks import IterCallback


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="back"), state=ResponseStates.PRICE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page - 1

    orders = await api.get_orders(call.message.chat.id, 0)
    pages = len(orders)
    order = orders[current_page]
    text = order["model"] + '\n' + order["additional"]
    offers = {offer["id"]: f'{offer["price"]} {round(offer["raiting"], 2)}' for offer in order["offers"]}
    await call.message.edit_text(text=text, reply_markup=inline.one_page_iter_btns(offers, pages, current_page))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(), state=ResponseStates.PRICE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page
    offer_id = int(callback.action)
    async with state.proxy() as data:
        data["offer_id"] = offer_id
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
    await call.message.edit_text(text=f"{name}\n{location}\n{phone}\n\n{offer['price']}\n\n" + "Choose your next action ⤵️",
        reply_markup=inline.choice_company())


@dp.callback_query_handler(lambda call: "to_delivery_method" == call.data, state=ResponseStates.PRICE_STATE)
async def to_delivery_method(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    name = state_data["name"]
    location = state_data["location"]
    phone = state_data["phone"]
    price = state_data["price"]
    await call.message.edit_text(text=f"{name}\n{location}\n{phone}\n\n{price}\n\n" + "Choose your next action ⤵️", 
        reply_markup=inline.delivery_method())


@dp.callback_query_handler(lambda call: "pickup" == call.data, state=ResponseStates.PRICE_STATE)
async def find_spare_part(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Congratulations!\n\nAddress: ...\nYour order number: ,..", reply_markup=None)
    await send_message_of_interest(call.message.chat.id)


@dp.callback_query_handler(lambda call: "delivery" == call.data, state=ResponseStates.PRICE_STATE)
async def price_of(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Write your shipping address", reply_markup=None)
    await AddressStates.ADDRESS_STATE.set()