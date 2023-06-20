import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher

import decorators
import shop.messages
import shop.keyboards


class ShopMenuStates(StatesGroup):
    in_menu = State()


@decorators.picked_language
async def menu_msg_handler(message: types.Message, state: FSMContext, language='eng'):
    await state.reset_data()
    await state.set_state(ShopMenuStates.in_menu.state)

    msg = shop.messages.messages[language]['menu']

    keyboard = shop.keyboards.keyboards[language]['menu']

    await message.answer(text=msg, reply_markup=keyboard)


async def shop_menu_callback(callback: types.CallbackQuery, state: FSMContext, language='eng'):
    await state.reset_data()
    await state.set_state(ShopMenuStates.in_menu.state)

    msg = shop.messages.messages[language]['menu']

    keyboard = shop.keyboards.keyboards[language]['menu']

    await callback.message.edit_text(text=msg, reply_markup=keyboard)
def register_handlers(dp: Dispatcher):
	pass