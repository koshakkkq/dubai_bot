import utils.decorators as decorators
from loader import dp
from aiogram.types import CallbackQuery
from user.keyboards.inline import *
from user.keyboards.reply import *
from aiogram.dispatcher import FSMContext
from user.filters.states import CarDetailStates


@dp.callback_query_handler(
    lambda call: "to_menu" == call.data,
    state="*",
)
@decorators.picked_language
async def to_menu_callback(call: CallbackQuery, state: FSMContext, language='eng'):
    await call.message.edit_text("Main menu", reply_markup=menu())


@dp.callback_query_handler(lambda call: "help" == call.data)
async def help(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("*file how to use the bot*", reply_markup=to_menu())


@dp.callback_query_handler(lambda call: "become_courier" == call.data)
async def become_courier(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("*courier registration form*", reply_markup=to_menu())


@dp.callback_query_handler(lambda call: "feedback" == call.data)
async def feedback(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Suggestion list for you:", reply_markup=feedback_menu())


@dp.callback_query_handler(lambda call: "find_spare_part" == call.data)
async def feedback(call: CallbackQuery, state: FSMContext):
    await call.message.answer("✅ Great, now I will help you.\n\n1. Write a brand\n*important to write everything in one message", reply_markup=None)
    await CarDetailStates.BRAND_STATE.set()