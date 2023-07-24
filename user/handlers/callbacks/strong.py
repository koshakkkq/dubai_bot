import utils.decorators as decorators
from loader import dp
from aiogram.types import CallbackQuery
from user.keyboards import inline
from aiogram.dispatcher import FSMContext
from user.filters.states import CarDetailStates, ResponseStates
from utils import api


@dp.callback_query_handler(
    lambda call: "to_menu" == call.data,
    state="*",
)
@decorators.picked_language
async def to_menu_callback(call: CallbackQuery, state: FSMContext, language='eng'):
    await state.finish()
    await call.message.edit_text("Main menu", reply_markup=inline.menu())


@dp.callback_query_handler(lambda call: "help" == call.data, state="*")
async def help(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("*file how to use the bot*", reply_markup=inline.to_menu())


@dp.callback_query_handler(lambda call: "become_courier" == call.data, state="*")
async def become_courier(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("*courier registration form*", reply_markup=inline.to_menu())


@dp.callback_query_handler(lambda call: "feedback" == call.data, state="*")
async def feedback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    orders = await api.get_orders(call.message.chat.id, 0)
    pages = len(orders)
    order = orders[0]
    text = order["model"] + '\n' + order["additional"]
    offers = {offer["id"]: f'{offer["price"]} {round(offer["raiting"], 2)}' for offer in order["offers"]}
    await call.message.edit_text(text=text, reply_markup=inline.one_page_iter_btns(offers, pages))
    await ResponseStates.PRICE_STATE.set()


@dp.callback_query_handler(lambda call: "find_spare_part" == call.data, state="*")
async def feedback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    brands =  {item["name"]: item["id"] for item in await api.get_brands()}
    await call.message.edit_text(text="✅ Great, now I will help you.\n\n1. Write a brand\n*important to write everything in one message", 
                              reply_markup=inline.iter_btns(brands))
    await CarDetailStates.BRAND_STATE.set()