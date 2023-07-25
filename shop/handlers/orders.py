from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp
import shop.logic
from .shop_menu import ShopMenuStates, shop_menu_callback


import utils.decorators as decorators
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
@decorators.is_member
async def available_orders_begin(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):
    data = await state.get_data()
    if 'shop_available_orders_page' not in data:
        await state.update_data(shop_available_orders_page=1)
        page = 1
    else:
        page = data['shop_available_orders_page']

    await edit_reply_available_orders_with_page(callback, state, language, shop_id, page, True)



@dp.callback_query_handler(
    filters.Text(startswith='shop_available_orders_page'),
    state = "*",
)
@decorators.picked_language
@decorators.is_member
async def available_orders_next_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):
    command = int(callback.data.split('_')[-1])
    data = await state.get_data()


    cur_page = data.get('shop_available_orders_page', 0)
    cur_page += command
    await state.update_data(shop_available_orders_page=cur_page)
    await edit_reply_available_orders_with_page(callback, state, language, shop_id, cur_page)


async def edit_reply_available_orders_with_page(callback: types.CallbackQuery, state: FSMContext, language, shop_id,
                                                page, edit_msg = False):

    keyboard = await shop.keyboards.orders.get_available_orders(shop_id, language, page)
    if edit_msg == True:
        msg = shop.messages.messages[language]['shop_available_orders']

        await callback.message.edit_text(text=msg, reply_markup=keyboard)
        await callback.answer()
    else:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()
@dp.callback_query_handler(
    filters.Text(startswith="shop_get_available_order_"),
    state="*",
)
@decorators.picked_language

async def get_available_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng'):


    order_id = callback.data.split('_')[-1]
    await state.update_data(shop_order_id=order_id)
    msg = await shop.messages.get_available_order_info_message(order_id, language)
    if msg[0] == 'does_not_exist':
        msg = shop.keyboards.keyboards[language]['err_on_server']
        keyboard = shop.keyboards.keyboards[language]['shop_available_order_finish']
        await callback.message.edit_text(msg, keyboard)
        await callback.answer()
        return
    msg = msg[1]
    keyboard = shop.keyboards.keyboards[language]['available_order_info']
    await state.set_state(AvailableOrdersStates.order_info.state)
    await callback.message.edit_text(text=msg, reply_markup=keyboard)
    await callback.answer()

@dp.message_handler(
    state=AvailableOrdersStates.order_info,
)
@decorators.picked_language
@decorators.is_member
async def set_order_price(message: types.Message, state:FSMContext, language='eng', shop_id = -1):

    price = 0
    data = await state.get_data()
    order_id = data['shop_order_id']
    try:
        price = message.text
        price.replace(',', '.')
        price = float(price)

        if price >= 36728.98 or price <= 3.67:
            raise Exception()
    except Exception as e:
        print(e)

        msg_to_add = shop.messages.messages[language]['err_in_price']

        msg = await shop.messages.get_available_order_info_message(order_id, language)

        if msg[0] == 'does_not_exist':
            msg = shop.keyboards.keyboards[language]['err_on_server']
            keyboard = shop.keyboards.keyboards[language]['shop_available_order_finish']
            await message.answer(msg, keyboard)
            return
        msg = msg[1]

        msg = msg_to_add + msg
        keyboard = shop.keyboards.keyboards[language]['shop_available_order_finish']

        await message.answer(text=msg, reply_markup=keyboard)

        return

    order_id = data['shop_order_id']


    await shop.logic.create_order_offer(shop_id=shop_id, price=price, order_id=order_id)

    await state.reset_state(with_data=False)

    msg = shop.messages.messages[language]['shop_available_order_finish']

    keyboard = shop.keyboards.keyboards[language]['shop_available_order_finish']

    await message.answer(text=msg, reply_markup=keyboard)



@dp.callback_query_handler(
    filters.Text(equals='shop_order_decline'),
    state=AvailableOrdersStates.order_info,
)
@decorators.picked_language
@decorators.is_member
async def shop_order_decline(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    data = await state.get_data()
    order_id = data['shop_order_id']

    await shop.logic.create_order_blacklist(shop_id=shop_id, order_id=order_id)

    cur_page = data['shop_available_orders_page']

    await edit_reply_available_orders_with_page(callback, state, language, shop_id, cur_page, True)




@dp.callback_query_handler(
    filters.Text(equals="shop_active_orders"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def show_active_orders_begin(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    data = await state.get_data()
    if "shop_active_orders_page" not in data:
        data['shop_active_orders_page'] = 1
        await state.update_data(shop_active_orders_page=1)

    page = data['shop_active_orders_page']

    await show_active_orders(callback, state, language, shop_id, page, edit_msg=True)


async def show_active_orders(callback: types.CallbackQuery, state: FSMContext, language, shop_id, page, edit_msg = False):
    keyboard = await shop.keyboards.orders.get_active_orders(shop_id, language, page)

    if edit_msg == True:
        msg = shop.messages.messages[language]['shop_active_orders']

        await callback.message.edit_text(text=msg, reply_markup=keyboard)
    else:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()

@dp.callback_query_handler(
    filters.Text(startswith="shop_active_orders_page"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def change_active_orders_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    command = int(callback.data.split('_')[-1])
    data = await state.get_data()

    cur_page = data.get('shop_active_orders_page', 0)
    cur_page += command
    await state.update_data(shop_active_orders_page=cur_page)
    await show_active_orders(callback, state, language, shop_id, cur_page, edit_msg=False)

class ActiveOrdersStates(StatesGroup):
    order_info = State()
    empty_state = State()
@dp.callback_query_handler(
    filters.Text(startswith="shop_get_active_order_"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def get_active_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    order_id = callback.data.split('_')[-1]
    await state.update_data(active_order_id=order_id)
    await state.set_state(ActiveOrdersStates.order_info.state)

    msg = await shop.messages.orders.get_active_order_info(
        order_id,
        language,
    )

    if msg[0] == 'does_not_exist':
        msg = shop.messages.messages[language]['err_on_server']
        keyboard = shop.keyboards.keyboards[language]['to_menu']
        await callback.message.edit_text(msg, keyboard)
        await callback.answer()
        return

    msg = msg[1]
    keyboard = shop.keyboards.keyboards[language]['shop_active_order_info']
    await callback.message.edit_text(text=msg, reply_markup=keyboard,  parse_mode="HTML")
    await callback.answer()

@dp.callback_query_handler(
    filters.Text(startswith='shop_active_order_status_'),
    state=ActiveOrdersStates.order_info,
)
@decorators.picked_language
@decorators.is_member
async def shop_active_order_set_status(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    await state.set_state(ActiveOrdersStates.empty_state.state)

    data = await state.get_data()


    order_id = data['active_order_id']

    command = callback.data.split('_')[-1]

    await shop.logic.set_order_offer_status(order_id, command)

    await show_active_orders_begin(callback, state)


@dp.callback_query_handler(
    filters.Text(equals="shop_done_orders"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def show_done_orders_begin(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    data = await state.get_data()
    if "shop_done_orders_page" not in data:
        data['shop_done_orders_page'] = 1
        await state.update_data(shop_done_orders_page=1)

    page = data['shop_done_orders_page']

    await show_done_orders(callback, state, language, shop_id, page, edit_msg=True)

async def show_done_orders(callback: types.CallbackQuery, state: FSMContext, language, shop_id, page, edit_msg = False):
    keyboard = await shop.keyboards.orders.get_done_orders(shop_id, language, page)

    if edit_msg == True:
        msg = shop.messages.messages[language]['shop_done_orders']

        await callback.message.edit_text(text=msg, reply_markup=keyboard)
    else:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer()

@dp.callback_query_handler(
    filters.Text(startswith="shop_done_orders_page"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def change_done_orders_page(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    command = int(callback.data.split('_')[-1])
    data = await state.get_data()

    cur_page = data.get('shop_done_orders_page', 0)
    cur_page += command
    await state.update_data(shop_done_orders_page=cur_page)
    await show_done_orders(callback, state, language, shop_id, cur_page, edit_msg=False)


@dp.callback_query_handler(
    filters.Text(startswith="shop_get_done_order_"),
    state="*",
)
@decorators.picked_language
@decorators.is_member
async def get_done_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id=-1):
    order_id = callback.data.split('_')[-1]
    await state.update_data(done_order_id=order_id)
    await state.set_state(ActiveOrdersStates.order_info.state)

    msg = await shop.messages.orders.get_done_order_info(
        order_id,
        language,
    )

    if msg[0] == 'does_not_exist':
        msg = shop.messages.messages[language]['err_on_server']
        keyboard = shop.keyboards.keyboards[language]['to_menu']
        await callback.message.edit_text(msg, keyboard)
        await callback.answer()
        return

    msg = msg[1]
    keyboard = shop.keyboards.keyboards[language]['shop_done_order_info']
    await callback.message.edit_text(text=msg, reply_markup=keyboard,  parse_mode="HTML")
    await callback.answer()


