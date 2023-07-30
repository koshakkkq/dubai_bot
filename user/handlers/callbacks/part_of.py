from loader import dp, bot
from aiogram.types import CallbackQuery
from user.keyboards import inline
from user.keyboards import reply
from aiogram.dispatcher import FSMContext
from user.filters.states import ApplicationStates
from user.utils import send_message_of_interest, text_for_order
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
	await call.message.edit_text("We're glad you got it all!\nPlease rate the quality of service ❤️\nSEND NUMBERS FROM 1 TO 5 ⤵️", reply_markup=inline.mark_keyboard(shop_id))


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


@dp.callback_query_handler(lambda call: "mark" in call.data)
async def price_of(call: CallbackQuery, state: FSMContext):
	_, mark, shop_id = call.data.split(":")
	await api.shop_feedback_create(shop_id, mark)
	await call.message.edit_text("Thank you", reply_markup=None)
	await call.message.answer("Main menu", reply_markup=inline.menu())