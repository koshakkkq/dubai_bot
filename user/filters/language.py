from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import LanguageStates
from user.keyboards import inline
from decorators_utils import set_language
from aiogram.dispatcher import filters
from user.handlers.callbacks.strong import to_menu_callback
import asyncio
import logging




@dp.callback_query_handler(
    filters.Text(startswith="pick_language"),
    state="*",
)
async def pick_language(callback: CallbackQuery, state=LanguageStates.MAIN_STATE):
    picked_language = callback.data.split('_')[-1]
    await set_language(callback.from_user.id, picked_language)
    await to_menu_callback(callback, state)

