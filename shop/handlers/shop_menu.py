import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from loader import dp


import utils.decorators as decorators
import shop.messages
import shop.keyboards

class ShopMenuStates(StatesGroup):
    in_menu = State()


@decorators.subscribe_needed
@decorators.picked_language
@decorators.is_member
async def menu_msg_handler(message: types.Message, state: FSMContext, language='eng', shop_id = -1):
    await state.reset_data()
    await state.set_state(ShopMenuStates.in_menu.state)

    msg = shop.messages.messages[language]['shop_menu']

    keyboard = shop.keyboards.keyboards[language]['shop_menu']

    await message.answer(text=msg, reply_markup=keyboard)



@dp.callback_query_handler(
    filters.Text(equals="shop_menu"),
    state="*",
)
@decorators.subscribe_needed
@decorators.picked_language
@decorators.is_member
@decorators.delete_msg_decorator
async def shop_menu_callback(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):
    await state.reset_data()

    await state.set_state(ShopMenuStates.in_menu.state)
    msg = shop.messages.messages[language]['shop_menu']

    keyboard = shop.keyboards.keyboards[language]['shop_menu']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)


@dp.callback_query_handler(
    filters.Text(equals='shop_help'),
    state='*',
)
@decorators.subscribe_needed
@decorators.picked_language
@decorators.is_member
@decorators.delete_msg_decorator
async def shop_help_callback(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):

    await state.set_state(ShopMenuStates.in_menu.state)
    msg = '''Customer request - active requests from users to search for spare parts. Select an order send a price to respond

Active orders - orders in which you have been selected as a seller. You can select an order and contact the customer. You can immediately change the order status to completed or rejected.

My offers - active orders that you have responded to, but you have not yet been selected as a seller. Here you can cancel your offer . The order will appear again in the Customer request section

Finished orders - your completed orders

Shop information - detailed information about your store. Fill in all the data so that users can find you.'''

    keyboard = shop.keyboards.keyboards[language]['back_to_shop_menu']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)