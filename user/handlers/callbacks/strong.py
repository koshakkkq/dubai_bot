from loader import dp
from aiogram.types import CallbackQuery
from user.keyboards.inline import *
from user.keyboards.reply import *
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda call: "to_menu" == call.data)
async def to_menu_callback(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("Main menu", reply_markup=menu())


@dp.callback_query_handler(lambda call: "help" == call.data)
async def help(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("*file how to use the bot*", reply_markup=to_menu())


@dp.callback_query_handler(lambda call: "register_store" == call.data)
async def register_store(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("*shop registration form*", reply_markup=to_menu())


@dp.callback_query_handler(lambda call: "become_courier" == call.data)
async def become_courier(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("*courier registration form*", reply_markup=to_menu())


@dp.callback_query_handler(lambda call: "feedback" == call.data)
async def feedback(call: CallbackQuery, state: FSMContext):
	await call.message.edit_text("Suggestion list for you:", reply_markup=feedback_menu())