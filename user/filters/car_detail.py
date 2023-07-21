from loader import dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from .states import CarDetailStates
from user.keyboards import inline, reply
import asyncio
import logging
from utils import api
from utils.constants import PART_TYPES


@dp.message_handler(state=CarDetailStates.BRAND_STATE)
async def text_msg(message: Message, state: FSMContext):
    cars = await api.get_cars()
    brands = set()
    for car in cars:
        if car["brand"]["name"].lower() == message.text.lower():
            async with state.proxy() as data:
                data["brand"] = car["brand"]["name"]
                data["brand_id"] = car["brand"]["id"]
            await CarDetailStates.MODEL_STATE.set()
            await message.answer(f"2. Write a model", reply_markup=None)
            return
        elif message.text.lower() in car["brand"]["name"].lower():
            brands.add(car["brand"]["name"])
    if brands:
        await message.answer("Please, select brand", reply_markup=reply.iter_btns(brands))
    else:
        await message.answer("Please, enter brand name", reply_markup=None)


@dp.message_handler(state=CarDetailStates.MODEL_STATE)
async def text_msg(message: Message, state: FSMContext):
    cars = await api.get_cars()
    state_data = await state.get_data()
    brand = state_data["brand"]
    cars = list(filter(lambda x: x["brand"]["name"] == brand, cars))
    car_names = set()
    for car in cars:
        if car["name"].lower() == message.text.lower():
            async with state.proxy() as data:
                data["model"] = car["name"]
            model = car["name"]
            year_cars = list(filter(lambda x: x["brand"]["name"] == brand and x["name"] == model, await api.get_cars()))
            years_set = set(map(lambda x: f'{x["production_start"]} - {x["production_end"]}', year_cars))
            await CarDetailStates.YEAR_STATE.set()
            await message.answer(f"3. Select the year of your model", reply_markup=reply.iter_btns(years_set))
            return
        elif message.text.lower() in car["name"].lower():
            car_names.add(car["name"])
    if car_names:
        await message.answer("Please, select a car model", reply_markup=reply.iter_btns(car_names))
    else:
        await message.answer(f"2. Write a model", reply_markup=None)


@dp.message_handler(state=CarDetailStates.YEAR_STATE)
async def text_msg(message: Message, state: FSMContext):
    state_data = await state.get_data()
    brand = state_data["brand"]
    model = state_data["model"]
    cars = await api.get_cars()
    cars = list(filter(lambda x: x["brand"]["name"] == brand and x["name"] == model, cars))
    for car in cars:
        years = f'{car["production_start"]} - {car["production_end"]}'
        if message.text.replace(" ", "") == years.replace(" ", ""):
            async with state.proxy() as data:
                data["years"] = years
                data["model_id"] = car["id"]
            await CarDetailStates.DETAIL_TYPE_STATE.set()
            await message.answer(f"Select the part type", reply_markup=reply.iter_btns(PART_TYPES))
            return
    years_set = set(map(lambda x: f'{x["production_start"]} - {x["production_end"]}', cars))
    await message.answer("Select the years of your model", reply_markup=reply.iter_btns(years_set))


@dp.message_handler(state=CarDetailStates.DETAIL_TYPE_STATE)
async def text_msg(message: Message, state: FSMContext):
    if message.text in PART_TYPES:
        async with state.proxy() as data:
            data["detail_type"] = message.text
        await CarDetailStates.DETAIL_NAME_STATE.set()
        await message.answer(f"5. Write the name of the spare part", reply_markup=None)
    else:
        await message.answer(f"Select the part type", reply_markup=reply.iter_btns(PART_TYPES))


@dp.message_handler(state=CarDetailStates.DETAIL_NAME_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f'6. Write the article \n*if it is not there, click "NO🚫"', reply_markup=inline.no_btn())
    async with state.proxy() as data:
        data["detail_name"] = message.text
    await CarDetailStates.ARTICLE_STATE.set()


@dp.callback_query_handler(lambda call: "user_no_filter" == call.data, state=CarDetailStates.ARTICLE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"⚡️Great, your request has been received⚡️\n\nAs soon as there are offers for your request, we will send you to the chatbot.\n\nAfter 25 seconds you will be redirected to the main menu", reply_markup=None)
    async with state.proxy() as data:
        data["article"] = None
        additional = f"Detail name: {data['detail_name']}\n Detail type: {data['detail_type']}\nArticle: {data['article']}"
        data = await api.order_create(call.message.chat.id, data["model_id"], additional)
    await asyncio.sleep(30)
    await state.finish()
    await call.message.answer("You are in the main menu", reply_markup=inline.menu())


@dp.message_handler(state=CarDetailStates.ARTICLE_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f"⚡️Great, your request has been received⚡️\n\nAs soon as there are offers for your request, we will send you to the chatbot.\n\nAfter 25 seconds you will be redirected to the main menu", reply_markup=None)
    async with state.proxy() as data:
        data["article"] = message.text
        additional = f"Detail name: {data['detail_name']}\n Detail type: {data['detail_type']}\nArticle: {data['article']}"
        data = await api.order_create(message.chat.id, data["model_id"], additional)
    await asyncio.sleep(30)
    await state.finish()
    await message.answer("You are in the main menu", reply_markup=inline.menu())