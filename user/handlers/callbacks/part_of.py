from loader import dp, bot
from aiogram.types import CallbackQuery
from user.keyboards import inline
from user.keyboards import reply
from aiogram.dispatcher import FSMContext, filters
from user.filters.states import ApplicationStates
from user.utils import text_for_order
from user.handlers.callbacks.strong import my_orders_call
from utils import api
from utils.decorators_utils import delete_msg
from shop.messages import get_shop_info_message


@dp.callback_query_handler(lambda call: "price_of" == call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Company information:\n\n\nCompany name:\n\n📍 Location:\n\n📲 Phone:\n\n!PRICE!\n\nChoose your next action ⤵️", 
        reply_markup=inline.choice_company())


@dp.callback_query_handler(lambda call: "to_delivery_method" == call.data)
async def to_delivery_method(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Company information:\n\n\nCompany name:\n\n📍 Location:\n\n📲 Phone:\n\n!PRICE!\n\nChoose your next action ⤵️", 
        reply_markup=inline.delivery_method())


@dp.callback_query_handler(lambda call: "was_deliveried" in call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
	await delete_msg(call.message.chat.id)
	_, shop_id, order_id = call.data.split(":")
	await api.order_status_increase(order_id)
	await call.message.edit_text("We're glad you got it all!\nPlease rate shop quality ❤️\nSEND NUMBERS FROM 1 TO 5 ⤵️", reply_markup=inline.mark_keyboard(shop_id, order_id))


async def rate_courier(call: CallbackQuery, state: FSMContext):
    pass


@dp.callback_query_handler(lambda call: 'courier_offers' in call.data)
async def courier_offers(call: CallbackQuery, state: FSMContext):
    order_id = call.data.split(':')[-1]
    await delete_msg(call.message.chat.id)
    offers = await api.get_courier_offers(order_id)
    data = {}
    for offer in offers:
        data[offer["id"]] = offer["price"]
    await call.message.edit_text("Select your courier, please", reply_markup=inline.courier_selection_btns(data))



@dp.callback_query_handler(lambda call: 'order_offer_pick' in call.data)
async def courier_offer_pick(call: CallbackQuery, state: FSMContext):
    _, offer_id = call.data.split(':')

    await api.pick_courier_offer(offer_id)

    await my_orders_call(call, state)
@dp.callback_query_handler(lambda call: "wasnt_deliveried" in call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Can you please tell me what is the problem?", reply_markup=None)
    await ApplicationStates.MAIN_STATE.set()


@dp.callback_query_handler(lambda call: "myorder_back" in call.data)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    _, current_page = call.data.split(":")
    current_page = int(current_page) - 1
    await delete_msg(call.message.chat.id)

    orders = []
    delta = await api.get_orders(call.message.chat.id, 1)
    if not delta is None:
        orders += delta
    delta = await api.get_orders(call.message.chat.id, 2)
    if not delta is None:
        orders += delta
    delta = await api.get_orders(call.message.chat.id, 3)
    if not delta is None:
        orders += delta

    if not orders[current_page]["offer"] is None:
        try:
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        location, info = await get_shop_info_message(orders[current_page]["offer"]["shop"])
        msg = await bot.send_location(call.message.chat.id, **location)
        await api.set_msg_to_delete(call.message.chat.id, msg.message_id)

    text = await text_for_order(orders[current_page]["id"])
    await call.message.answer(text=text, reply_markup=inline.my_order_btns(orders, current_page), parse_mode='HTML')



@dp.callback_query_handler(filters.Text(startswith="mark"))
async def price_of(call: CallbackQuery, state: FSMContext):
    _, mark, shop_id, order_id = call.data.split(":")
    await api.shop_feedback_create(shop_id, mark, order_id)

    order_info = await api.get_order(order_id)

    if order_info['credential']['is_delivery'] == False:

        await call.message.edit_text("Thank you", reply_markup=None)
        await call.message.answer("Main menu", reply_markup=inline.menu())
    else:


        await call.message.edit_text('Please rate courier quality ❤️\nSEND NUMBERS FROM 1 TO 5 ⤵️', reply_markup=inline.courier_mark_keyboard(shop_id, order_id))

@dp.callback_query_handler(filters.Text(startswith="courier_mark"))
async def courier_mark(call: CallbackQuery, state: FSMContext):
    _, mark, shop_id, order_id = call.data.split(':')

    await api.courier_feedback_create(order_id, mark)

    await call.message.edit_text("Thank you", reply_markup=None)
    await call.message.answer("Main menu", reply_markup=inline.menu())