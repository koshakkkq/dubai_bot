from loader import dp, bot
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import ResponseStates
from user.keyboards import inline, reply
from utils import api
from user.keyboards.inline.callbacks import IterCallback
#from user.utils import send_message_of_interest
import config
from aiogram import types
from aiogram.types.message import ContentType
from user.utils import text_for_order
from shop.messages import get_shop_info_message
from utils.decorators_utils import delete_msg, edit_msg


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="back"), state=ResponseStates.PRICE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    await delete_msg(call.message.chat.id)
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page - 1

    orders = await api.get_orders(call.message.chat.id, 0)
    pages = len(orders)
    order = orders[current_page]
    async with state.proxy() as data:
        text = order["model"] + '\n' + order["additional"]
        offers = {offer["id"]: f'Price: {offer["price"]} AED, raiting: {round(offer["raiting"], 2)}' for offer in order["offers"]}
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
        data["shop_id"] = offer["shop"]["id"]
        geo, info = await get_shop_info_message(offer["shop"]["id"])
        try:
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        msg = await bot.send_location(call.message.chat.id, **geo)
        await api.set_msg_to_delete(call.message.chat.id, msg.message_id)
    await call.message.answer(text=f"Shop name: {name}\nShop location: {location}\nShop phone: {phone}\nPrice: {offer['price']}\n\n" + "Choose your next action ⤵️",
        reply_markup=inline.choice_company())



@dp.callback_query_handler(lambda call: "to_delivery_method" == call.data, state=[ResponseStates.PRICE_STATE, ResponseStates.SELECT_CORIER_STATE])
async def to_delivery_method(call: CallbackQuery, state: FSMContext):
    await delete_msg(call.message.chat.id)
    state_data = await state.get_data()
    name = state_data["name"]
    location = state_data["location"]
    phone = state_data["phone"]
    price = state_data["price"]
    await ResponseStates.PRICE_STATE.set()
    await call.message.edit_text(text=f"Shop name: {name}\nShop location: {location}\nShop phone: {phone}\nPrice: {price}\n\n" + "Choose your next action ⤵️",
        reply_markup=inline.delivery_method())



@dp.callback_query_handler(lambda call: "pickup" == call.data, state=ResponseStates.PRICE_STATE)
async def find_spare_part(call: CallbackQuery, state: FSMContext):
    await delete_msg(call.message.chat.id)
    state_data = await state.get_data()
    order_id = state_data['order_id']
    offer_id = state_data["offer_id"]
    shop_id = state_data["shop_id"]
    status = await api.order_update(order_id, offer_id, status=1, is_delivery=False)
    geo, info = await get_shop_info_message(shop_id)
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    await bot.send_location(call.message.chat.id, **geo)
    await call.message.answer("Congratulations!\n\nYour order number: " + str(state_data["order_id"]), 
        reply_markup=None)
    #await send_message_of_interest(call.message.chat.id, shop_id, order_id)



@dp.callback_query_handler(lambda call: "delivery" == call.data, state=[ResponseStates.PRICE_STATE, ResponseStates.SELECT_CORIER_STATE, ResponseStates.ADDRESS_STATE])
async def price_of(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order_id = state_data['order_id']
    offers = await api.get_courier_offers(order_id)
    data = {}
    for offer in offers:
        data[offer["id"]] = offer["price"]
    await call.message.edit_text("Select your courier, please", reply_markup=inline.courier_selection_btns(data))
    await ResponseStates.SELECT_CORIER_STATE.set()


@dp.callback_query_handler(lambda call: "order_offer" in call.data, state=ResponseStates.SELECT_CORIER_STATE)
async def price_of(call: CallbackQuery, state: FSMContext):
    _, offer_id = call.data.split(":")
    #offer = await api.get_courier_offer(offer_id)
    async with state.proxy() as data:
        data["courier_offer_id"] = offer_id

    msg = await call.message.edit_text("Send your geolocation, please", reply_markup=inline.back_to_pickup_selecton())
    await api.set_msg_to_edit(call.message.chat.id, msg.message_id)
    await ResponseStates.ADDRESS_STATE.set()



@dp.callback_query_handler(lambda call: "to_delivery_method_addres_state" == call.data, state=[ResponseStates.STRIPE_STATE, ResponseStates.ADDRESS_STATE])
async def find_spare_part(call: CallbackQuery, state: FSMContext):
    await edit_msg(call.message.chat.id)
    await to_delivery_method(call, state)
    await ResponseStates.PRICE_STATE.set()


@dp.message_handler(content_types=['location'], state=ResponseStates.ADDRESS_STATE)
async def text_msg(message: Message, state: FSMContext):
    await edit_msg(message.chat.id)

    lat = message.location.latitude
    lon = message.location.longitude
    async with state.proxy() as data:
        data["lat"] = lat
        data["lon"] = lon
    await ResponseStates.STRIPE_STATE.set()
    msg = await message.answer("Write additional address info for courier, if there is noting write '-' ", reply_markup=inline.back_to_pickup_selecton())
    await api.set_msg_to_edit(message.chat.id, msg.message_id)


@dp.message_handler(state=ResponseStates.STRIPE_STATE)
async def successful(message: types.Message, state: FSMContext):
    await edit_msg(message.chat.id)
    state_data = await state.get_data()
    order_id = state_data['order_id']
    offer_id = state_data["offer_id"]
    address = message.text
    shop_id = state_data["shop_id"]
    lat = state_data["lat"]
    lon = state_data["lon"]
    courier_offer_id = state_data["courier_offer_id"]
    status = await api.order_update(order_id, offer_id, status=1, address=address, is_delivery=True, lat=lat, lon=lon, couirer_offer_id=courier_offer_id)
    await message.answer("Congratulations!\nSoon your goods will be delivered to you\nyou can get information about the order in \n\"💼 My orders\"", reply_markup=inline.my_orders())
    await state.finish()
    #await send_message_of_interest(message.chat.id, order_id, order_id)