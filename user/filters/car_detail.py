from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import CarDetailStates
from user.keyboards import inline
import asyncio
import logging


@dp.message_handler(state=CarDetailStates.BRAND_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f"2. Write a model", reply_markup=None)
    async with state.proxy() as data:
        data["brand"] = message.text
    await CarDetailStates.MODEL_STATE.set()


@dp.message_handler(state=CarDetailStates.MODEL_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f"3. Write the part type", reply_markup=None)
    async with state.proxy() as data:
        data["model"] = message.text
    await CarDetailStates.DETAIL_TYPE_STATE.set()


@dp.message_handler(state=CarDetailStates.DETAIL_TYPE_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f"4. Write the name of the spare part", reply_markup=None)
    async with state.proxy() as data:
        data["detail_type"] = message.text
    await CarDetailStates.DETAIL_NAME_STATE.set()


@dp.message_handler(state=CarDetailStates.DETAIL_NAME_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f'5. Write the article \n*if it is not there, click "NO🚫"', reply_markup=inline.no_btn())
    async with state.proxy() as data:
        data["detail_name"] = message.text
    await CarDetailStates.ARTICLE_STATE.set()


@dp.callback_query_handler(lambda call: "user_no_filter" == call.data, state=CarDetailStates.ARTICLE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"⚡️Great, your request has been received⚡️\n\nAs soon as there are offers for your request, we will send you to the chatbot.\n\nAfter 25 seconds you will be redirected to the main menu", reply_markup=None)
    async with state.proxy() as data:
        data["article"] = None
        log_message = f"brand: {data['brand']} model: {data['model']} detail_type: {data['detail_type']} detail_name: {data['detail_name']} article: {data['article']}"
        logging.info(log_message)
    await asyncio.sleep(30)
    await state.finish()
    await call.message.answer("You are in the main menu", reply_markup=inline.menu())


@dp.message_handler(state=CarDetailStates.ARTICLE_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f"⚡️Great, your request has been received⚡️\n\nAs soon as there are offers for your request, we will send you to the chatbot.\n\nAfter 25 seconds you will be redirected to the main menu", reply_markup=None)
    async with state.proxy() as data:
        data["article"] = message.text
        log_message = f"brand: {data['brand']} model: {data['model']} detail_type: {data['detail_type']} detail_name: {data['detail_name']} article: {data['article']}"
        logging.info(log_message)
    await asyncio.sleep(30)
    await state.finish()
    await message.answer("You are in the main menu", reply_markup=inline.menu())