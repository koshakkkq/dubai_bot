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
@decorators.picked_language
@decorators.is_member
@decorators.delete_msg_decorator
async def shop_menu_callback(callback: types.CallbackQuery, state: FSMContext, language='eng', shop_id = -1):
    await state.reset_data()
    await state.set_state(ShopMenuStates.in_menu.state)
    msg = shop.messages.messages[language]['shop_menu']

    keyboard = shop.keyboards.keyboards[language]['shop_menu']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)

