import utils.decorators as decorators
from loader import dp, bot
from aiogram.types import CallbackQuery
from user.keyboards import inline
from aiogram.dispatcher import FSMContext
from user.filters.states import CarDetailStates, ResponseStates
from utils import api
from user.utils import text_for_order
from utils.decorators_utils import delete_msg
from shop.messages import get_shop_info_message


@dp.callback_query_handler(
    lambda call: "to_menu" == call.data,
    state="*",
)
@decorators.picked_language
async def to_menu_callback(call: CallbackQuery, state: FSMContext, language='eng'):
    await state.finish()
    await delete_msg(call.message.chat.id)
    await call.message.edit_text("Main menu", reply_markup=inline.menu())


@dp.callback_query_handler(lambda call: "help" == call.data, state="*")
async def help(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("*file how to use the bot*", reply_markup=inline.to_menu())


@dp.callback_query_handler(lambda call: "become_courier" == call.data, state="*")
async def become_courier(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("*courier registration form*", reply_markup=inline.to_menu())


@dp.callback_query_handler(lambda call: "my_orders" == call.data, state="*")
async def become_courier(call: CallbackQuery, state: FSMContext):
    await api.reset_user_notifications(call.from_user.id, {'new_couriers':0})
    await state.finish()
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
    if not orders:
        await call.message.edit_text(text="No orders", reply_markup=inline.to_menu())
    else:
        text = await text_for_order(orders[0]['id'])
        if not orders[0]["offer"] is None:
            try:
                await bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            location, info = await get_shop_info_message(orders[0]["offer"]["shop"])
            msg = await bot.send_location(call.message.chat.id, **location)
            await api.set_msg_to_delete(call.message.chat.id, msg.message_id)
        await call.message.answer(text=text, reply_markup=inline.my_order_btns(orders))



@dp.callback_query_handler(lambda call: "feedback" == call.data, state="*")
async def feedback(call: CallbackQuery, state: FSMContext):
    await api.reset_user_notifications(call.from_user.id, {'new_offers':0})

    await delete_msg(call.message.chat.id)
    await state.finish()
    orders = await api.get_orders(call.message.chat.id, 0)
    if orders is None:
        await call.message.edit_text(text="No active orders", reply_markup=inline.to_menu())
    else:
        pages = len(orders)
        order = orders[0]
        text = order["model"] + '\n' + order["additional"]
        offers = {offer["id"]: f'Price: {offer["price"]}, raiting: {round(offer["raiting"], 2)}' for offer in order["offers"]}
        await call.message.edit_text(text=text, reply_markup=inline.one_page_iter_btns(offers, pages))
        await ResponseStates.PRICE_STATE.set()


@dp.callback_query_handler(lambda call: "find_spare_part" == call.data, state="*")
async def feedback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    brands =  {item["name"]: item["id"] for item in await api.get_brands()}
    await call.message.edit_text(text="✅ Great, now I will help you.\n\n1. Write a brand\n*important to write everything in one message", 
                              reply_markup=None)
    await CarDetailStates.BRAND_STATE.set()