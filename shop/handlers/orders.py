from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp
from .shop_menu import ShopMenuStates, shop_menu_callback


import decorators
import shop.messages
import shop.keyboards.orders


class AvailableOrdersStates(StatesGroup):
    orders = State()
    order_info = State()
    order_price = State()
    finish = State()

@dp.callback_query_handler(
    filters.Text(equals="shop_customer_requests"),
    state="*",
)
@decorators.picked_language
async def show_available_orders(callback: types.CallbackQuery, state: FSMContext, language='eng'):
    data = await state.get_data()
    if 'available_orders_page' not in data:
        await state.update_data(available_orders_page=1)
        data['available_orders_page'] = 1

    page = data['available_orders_page']

    keyboard = await shop.keyboards.orders.get_available_orders(callback.from_user.id, language, page)

    msg = shop.messages.messages[language]['shop_available_orders']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

    await callback.answer()

@dp.callback_query_handler(
    filters.Text(startswith="shop_get_available_order_"),
    state="*",
)
@decorators.picked_language

async def get_available_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng'):

    await state.set_state(AvailableOrdersStates.order_info.state)

    order_id = callback.data.split('_')[-1]
    await state.update_data(order_id=order_id)

    msg = await shop.messages.get_available_order_info_message(callback.from_user.id, order_id, language)

    keyboard = shop.keyboards.keyboards[language]['available_order_info']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

@dp.callback_query_handler(
    filters.Text(equals="shop_accept_order"),
    state="*",
)
@decorators.picked_language
async def get_order_price(callback: types.CallbackQuery, state: FSMContext, language='eng'):
    data = await state.get_data()
    order_id = data['order_id']


    await state.set_state(AvailableOrdersStates.order_price.state)

    msg = shop.messages.messages[language]['shop_order_price']

    keyboard = shop.keyboards.orders.get_shop_accept_order_keyboard(order_id=order_id, language=language)

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

@dp.message_handler(
    state=AvailableOrdersStates.order_price,
)
@decorators.picked_language
async def set_order_price(message: types.Message, state:FSMContext, language='eng'):

    await state.set_state(AvailableOrdersStates.finish.state)

    msg = shop.messages.messages[language]['shop_available_order_finish']

    keyboard = shop.keyboards.keyboards[language]['shop_available_order_finish']

    await message.answer(text=msg, reply_markup=keyboard)


@dp.callback_query_handler(
    filters.Text(equals="shop_active_orders"),
    state="*",
)
@decorators.picked_language
async def show_active_orders(callback: types.CallbackQuery, state: FSMContext, language='eng'):
    data = await state.get_data()
    if "active_orders_page" not in data:
        data['active_orders_page'] = 1
        await state.update_data(active_orders_page=1)

    page = data['active_orders_page']
    await state.update_data(active_orders_page=1)

    msg = shop.messages.messages[language]['shop_active_orders']

    keyboard = await shop.keyboards.orders.get_active_orders(callback.from_user.id, language, page)

    await callback.message.edit_text(text=msg, reply_markup=keyboard)


@dp.callback_query_handler(
    filters.Text(startswith="shop_get_active_order_"),
    state="*",
)
@decorators.picked_language
async def get_active_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng'):
    order_id = callback.data.split('_')[-1]

    msg = await shop.messages.orders.get_active_order_info(
        callback.from_user.id,
        order_id,
        language,
    )

    keyboard = shop.keyboards.keyboards[language]['shop_active_order_info']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)
