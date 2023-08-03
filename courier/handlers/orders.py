import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters

import shop.logic
from utils.api import set_msg_to_delete
from .courier_menu import menu_callback
from loader import dp, bot

import courier.keyboards
import courier.messages
import courier.logic
import utils.decorators as decorators

from courier.logic.registration import *


class OrderPaginator:

    def __init__(self, get_keyboard_func, get_real_page_func, prefix, msgs):
        self.get_keyboard = get_keyboard_func
        self.get_real_page = get_real_page_func
        self.prefix = prefix
        self.msgs = msgs

        self.begin_pagination_text = f'{prefix}_begin'
        self.change_page_text = f'{prefix}_page_'

    @decorators.picked_language
    @decorators.is_courier
    @decorators.delete_msg_decorator
    async def begin_pagination(self, callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1):

        await state.reset_state(with_data=False)

        await self.get_current_page(state, courier_id=courier_id)

        await self.show_page(callback, state, language, courier_id, True)

    async def show_page(self, callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1, edit_msg=False):
        state_page_key = f'{self.prefix}_page'

        data = await state.get_data()

        current_page = data[state_page_key]

        keyboard = await self.get_keyboard(courier_id=courier_id,page=current_page,language=language, prefix=self.prefix)

        msg = self.msgs[language]

        if edit_msg is True:
            await callback.message.edit_text(text=msg, reply_markup=keyboard)
        else:
            await callback.message.edit_reply_markup(reply_markup=keyboard)

        await callback.answer()


    @decorators.picked_language
    @decorators.is_courier
    async def change_page(self, callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1, ):
        command = callback.data.split('_')[-1]

        await self.get_current_page(state, int(command), courier_id=courier_id)

        await self.show_page(callback, state, language, courier_id, False)

    async def get_current_page(self, state, command = 0,courier_id=-1):
        state_page_key = f'{self.prefix}_page'

        data = await state.get_data()
        if state_page_key not in data:
            await state.update_data(**{state_page_key:1})
            return


        current_page = data[state_page_key]

        page = await self.get_real_page(current_page+command, courier_id)

        await state.update_data(**{state_page_key:page})
    def register_handlers(self, dp: Dispatcher):

        dp.register_callback_query_handler(
            self.begin_pagination, state='*',text=self.begin_pagination_text,
        )

        dp.register_callback_query_handler(
            self.change_page, state='*', text_startswith=self.change_page_text,
        )


available_orders_paginator = OrderPaginator(
    get_keyboard_func=courier.keyboards.get_available_orders,
    get_real_page_func=courier.logic.get_available_orders_page,
    prefix='courier_available_orders',
    msgs={
        'eng':courier.messages.messages['eng']['available_orders']
    },
)


active_orders_paginator = OrderPaginator(
    get_keyboard_func=courier.keyboards.get_active_orders,
    get_real_page_func=courier.logic.get_active_orders_page,
    prefix='courier_active_orders',
    msgs={
        'eng':courier.messages.messages['eng']['active_orders']
    },
)


done_orders_paginator = OrderPaginator(
    get_keyboard_func=courier.keyboards.get_done_orders,
    get_real_page_func=courier.logic.get_done_orders_page,
    prefix='courier_done_orders',
    msgs={
        'eng':courier.messages.messages['eng']['done_orders']
    },
)

available_orders_paginator.register_handlers(dp)

active_orders_paginator.register_handlers(dp)

done_orders_paginator.register_handlers(dp)

class PickOrderStates(StatesGroup):
    in_order = State()
@dp.callback_query_handler(
	filters.Text(startswith="courier_available_orders_get_"),
	state="*",
)
@decorators.picked_language
@decorators.is_courier
async def available_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1,):
    order_id = callback.data.split('_')[-1]

    msg = await courier.messages.order_info(order_id, language)



    keyboard = courier.keyboards.keyboards[language]['available_order_info']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

    await state.update_data(courier_available_order=order_id)
    await state.set_state(PickOrderStates.in_order.state)

@dp.callback_query_handler(
    filters.Text(startswith='courier_available_order_pick'),
    state=PickOrderStates.in_order,
)
@decorators.picked_language
@decorators.is_courier
@decorators.delete_msg_decorator
async def pick_available_order(callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1,):
    await state.reset_state(with_data=False)

    data = await state.get_data()

    order_id = data['courier_available_order']
    msg = ''

    try:
        msg = await courier.messages.set_order_courier_msg(order_id=order_id, courier_id=courier_id, language=language)
    except Exception as e:
        msg = 'Sorry, error on server.'


    keyboard = courier.keyboards.keyboards[language]['available_order_finish']

    await callback.message.edit_text(text=msg, reply_markup=keyboard, parse_mode="HTML")



@dp.callback_query_handler(
    filters.Text(startswith='courier_available_order_reject'),
    state=PickOrderStates.in_order,
)
@decorators.picked_language
@decorators.is_courier
@decorators.delete_msg_decorator
async def reject_available_order(callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1,):
    await state.reset_state(with_data=False)

    data = await state.get_data()

    order_id = data['courier_available_order']

    await courier.logic.add_to_blacklist(order_id=order_id, courier_id=courier_id)

    await available_orders_paginator.show_page(callback, state, language, courier_id)


@dp.callback_query_handler(
	filters.Text(startswith="courier_active_orders_get_"),
	state="*",
)
@decorators.picked_language
@decorators.is_courier
async def active_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1,):
    order_id = callback.data.split('_')[-1]

    msg = await courier.messages.get_couriers_order_info_msg(order_id, language, 'courier_active_order_prefix')

    keyboard = courier.keyboards.keyboards[language]['active_orders_finish']



    await callback.message.edit_text(text=msg, reply_markup=keyboard, parse_mode="HTML")

    await state.reset_state(with_data=False)


@dp.callback_query_handler(
	filters.Text(startswith="courier_done_orders_get_"),
	state="*",
)
@decorators.picked_language
@decorators.is_courier
async def active_order_info(callback: types.CallbackQuery, state: FSMContext, language='eng', courier_id=-1,):
    order_id = callback.data.split('_')[-1]

    msg = await courier.messages.get_couriers_order_info_msg(order_id, language, 'courier_done_order_prefix')

    keyboard = courier.keyboards.keyboards[language]['done_orders_finish']


    await callback.message.edit_text(text=msg, reply_markup=keyboard, parse_mode="HTML")

    await state.reset_state(with_data=False)

