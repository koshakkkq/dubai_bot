from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import LanguageStates
from user.keyboards import inline
import asyncio
import logging


@dp.callback_query_handler(lambda call: "eng" == call.data, state=LanguageStates.MAIN_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Main menu", reply_markup=inline.menu())
    await state.finish()