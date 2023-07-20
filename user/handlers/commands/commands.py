from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

import utils.decorators as decorators
from loader import dp
from user.keyboards.inline import *
from user.keyboards.reply import *
from user.filters.states import LanguageStates



@dp.message_handler(
    commands=['start'],
    state='*',
)
@decorators.picked_language
async def bot_menu(message: Message, state, language):
    await message.answer("Main menu", reply_markup=menu())
    await state.finish()