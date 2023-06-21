from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from .shop_menu import ShopMenuStates, shop_menu_callback


import decorators
import shop.messages
import shop.keyboards.orders


class AvailableOrdersStates(StatesGroup):
    orders = State()
    order_info = State()
    order_price = State()
    finish = State()
@decorators.picked_language
async def show_available_orders(callback: types.CallbackQuery, state: FSMContext, language='eng'):
    await state.set_state(AvailableOrdersStates.orders.state)

    data = await state.get_data()
    if 'available_orders_page' not in data:
        await state.update_data(available_orders_page=1)
        data['available_orders_page'] = 1

    page = data['available_orders_page']

    keyboard = await shop.keyboards.orders.get_available_orders(callback.from_user.id, language, page)

    msg = shop.messages.messages[language]['shop_available_orders']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

    await callback.answer()

@decorators.picked_language
async def get_available_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng'):

    await state.set_state(AvailableOrdersStates.order_info.state)

    order_id = callback.data.split('_')[-1]
    await state.update_data(order_id=order_id)

    msg = await shop.messages.get_available_order_info_message(callback.from_user.id, order_id, language)

    keyboard = shop.keyboards.keyboards[language]['available_order_info']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)


@decorators.picked_language
async def get_order_price(callback: types.CallbackQuery, state: FSMContext, language='eng'):

    await state.set_state(AvailableOrdersStates.order_price.state)

    msg = shop.messages.messages[language]['shop_order_price']

    keyboard = shop.keyboards.keyboards[language]['back']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

@decorators.picked_language
async def set_order_price(message: types.Message, state:FSMContext, language='eng'):

    await state.set_state(AvailableOrdersStates.finish.state)

    msg = shop.messages.messages[language]['shop_available_order_finish']

    keyboard = shop.keyboards.keyboards[language]['shop_available_order_finish']

    await message.answer(text=msg, reply_markup=keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_available_orders,
        state=ShopMenuStates.in_menu,
        text='customer_requests',
    )

    dp.register_callback_query_handler(
        shop_menu_callback,
        state=AvailableOrdersStates.orders,
        text='back',
    )

    dp.register_callback_query_handler(
        get_available_order_info,
        state=AvailableOrdersStates.orders,
        text_startswith='get_order_',
    )

    dp.register_callback_query_handler(
        get_order_price,
        state=AvailableOrdersStates.order_info,
        text='accept_order',
    )


    dp.register_callback_query_handler(
        show_available_orders,
        state=AvailableOrdersStates.order_info,
        text='decline_order',
    )

    dp.register_callback_query_handler(
        get_available_order_info,
        state=AvailableOrdersStates.order_price.state,
        text='back',
    )

    dp.register_message_handler(
        set_order_price,
        state=AvailableOrdersStates.order_price
    )

    dp.register_callback_query_handler(
        shop_menu_callback,
        state=AvailableOrdersStates.finish,
        text='menu',
    )

    dp.register_callback_query_handler(
        show_available_orders,
        state=AvailableOrdersStates.finish,
        text='customer_requests',
    )