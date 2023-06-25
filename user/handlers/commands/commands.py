from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from loader import dp
from user.keyboards.inline import *
from user.keyboards.reply import *
from user.filters.states import LanguageStates


@dp.message_handler(
    CommandStart(),
    state="*"
)
async def bot_start(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!\nChoose language!", reply_markup=language_choice())
    await LanguageStates.MAIN_STATE.set()