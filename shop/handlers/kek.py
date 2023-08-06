from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp
import shop.logic
from .shop_menu import ShopMenuStates, shop_menu_callback
from utils.api import reset_shop_notifications

import utils.decorators as decorators
import shop.messages
import shop.keyboards.orders




@dp.callback_query_handler(
    filters.Text(equals="shop_my_responses"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def my_responses_begin(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):
    await state.reset_state(with_data=False)

    data = await state.get_data()
    if 'shop_my_responses_page' not in data:
        await state.update_data(shop_my_responses_page=1)
        page = 1
    else:
        page = data['shop_my_responses_page']

    await edit_reply_my_responses_with_page(callback, state, language, shop_id, page, True)



@dp.callback_query_handler(
    filters.Text(startswith='shop_my_response_orders_page'),
    state = "*",
)
@decorators.picked_language
@decorators.is_member
async def my_responses_next_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):
    command = int(callback.data.split('_')[-1])
    data = await state.get_data()

    cur_page = data.get('shop_my_responses_page', 0)
    cur_page += command

    cur_page = shop.logic.get_my_responses_enabled_page(shop_id, cur_page)

    await state.update_data(shop_my_responses_page=cur_page)
    await edit_reply_my_responses_with_page(callback, state, language, shop_id, cur_page)


async def edit_reply_my_responses_with_page(callback: types.CallbackQuery, state: FSMContext, language, shop_id,
                                                page, edit_msg = False):

    keyboard = await shop.keyboards.orders.get_my_response_orders(shop_id, language, page)
    if edit_msg == True:
        msg = shop.messages.messages[language]['shop_my_offers']

        await callback.message.edit_text(text=msg, reply_markup=keyboard)
        await callback.answer()
    else:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()


class MyResponsesStates(StatesGroup):
    offer_info = State()
@dp.callback_query_handler(
    filters.Text(startswith="shop_get_my_response_order_"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def shop_my_responses_info(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):


    order_id = callback.data.split('_')[-1]
    await state.update_data(shop_my_response_order_id=order_id)
    msg = await shop.messages.get_my_response_order_info_message(order_id, shop_id,language)
    keyboard = shop.keyboards.keyboards[language]['my_responses_info']
    await state.set_state(MyResponsesStates.offer_info.state)
    await callback.message.edit_text(text=msg, reply_markup=keyboard, parse_mode='HTML')
    await callback.answer()

@dp.callback_query_handler(
    filters.Text(startswith="cancel_my_offer"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def shop_my_responses_info(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    data = await state.get_data()

    order_id = data['shop_my_response_order_id']
    await shop.logic.cancel_offer(order_id,shop_id)
    await my_responses_begin(callback, state)

@dp.message_handler(
    state=MyResponsesStates.offer_info,
)
@decorators.picked_language
@decorators.is_member
async def shop_my_responses_info(message: types.Message, state: FSMContext, language='eng', shop_id=-1):
    price = 0
    data = await state.get_data()
    order_id = data['shop_my_response_order_id']
    msg_to_add = ''
    try:
        price = message.text
        price.replace(',', '.')
        price = float(price)

        if price >= 36728.98 or price <= 3.67:
            raise Exception()

        await shop.logic.change_offer_price(order_id, shop_id, price)

    except Exception as e:

        msg_to_add = shop.messages.messages[language]['err_in_price']

    msg = await shop.messages.get_my_response_order_info_message(order_id, shop_id,language)
    msg = msg_to_add + msg
    keyboard = shop.keyboards.keyboards[language]['my_responses_info']
    await message.answer(text=msg, reply_markup=keyboard, parse_mode='HTML')
    return
