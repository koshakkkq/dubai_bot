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
from user.keyboards.inline.callbacks import IterCallback


@dp.message_handler(state=CarDetailStates.DETAIL_NAME_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f'6. Write the article \n*if it is not there, click "NO🚫"', reply_markup=inline.no_btn())
    async with state.proxy() as data:
        data["detail_name"] = message.text
    await CarDetailStates.ARTICLE_STATE.set()


@dp.message_handler(state=CarDetailStates.ARTICLE_STATE)
async def text_msg(message: Message, state: FSMContext):
    await message.answer(f"⚡️Great, your request has been received⚡️\n\nAs soon as there are offers for your request, we will send you to the chatbot.\n\nAfter 5 seconds you will be redirected to the main menu", reply_markup=None)
    async with state.proxy() as data:
        data["article"] = message.text
        additional = f"Detail info: {data['detail_name']}\nDetail type: {data['detail_type']}\nArticle: {data['article']}"
        data = await api.order_create(message.chat.id, data["model_id"], additional)
    await asyncio.sleep(5)
    await state.finish()
    await message.answer("You are in the main menu", reply_markup=inline.menu())


# Callbacks
@dp.callback_query_handler(lambda call: "user_no_filter" == call.data, state=CarDetailStates.ARTICLE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f"⚡️Great, your request has been received⚡️\n\nAs soon as there are offers for your request, we will send you to the chatbot.\n\nAfter 5 seconds you will be redirected to the main menu", reply_markup=None)
    async with state.proxy() as data:
        data["article"] = None
        additional = f"Detail info: {data['detail_name']}\nDetail type: {data['detail_type']}\nArticle: {data['article']}"
        data = await api.order_create(call.message.chat.id, data["model_id"], additional)
    await asyncio.sleep(5)
    await state.finish()
    await call.message.answer("You are in the main menu", reply_markup=inline.menu())


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="previous_state"), state=CarDetailStates._states)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    callback = IterCallback.unpack(call.data)
    current_state = await CarDetailStates.previous()
    if current_state is None:
        await call.message.edit_text(text="Main menu", reply_markup=inline.menu())
    elif current_state == CarDetailStates.BRAND_STATE.state:
        brands =  {item["name"]: item["id"] for item in await api.get_brands()}
        await call.message.edit_text(text="✅ Great, now I will help you.\n\n1. Write a brand\n*important to write everything in one message", 
                                  reply_markup=inline.iter_btns(brands))
    elif current_state == CarDetailStates.MODEL_STATE.state:
        models = await api.get_models(state_data["brand_id"])
        models = {model["name"]: model["name"] for model in models}
        await call.message.edit_text(text=f"2. Select a car model", reply_markup=inline.iter_btns(models))
    elif current_state == CarDetailStates.YEAR_STATE.state:
        state_data = await state.get_data()
        years = await api.get_years(state_data["brand_id"], state_data["model"])
        years = {f'{car["production_start"]} - {car["production_end"]}': car["id"] for car in years}
        await CarDetailStates.YEAR_STATE.set()
        await call.message.edit_text(text=f"3. Select the year of your model", reply_markup=inline.iter_btns(years))
    elif current_state == CarDetailStates.DETAIL_TYPE_STATE.state:
        await call.message.edit_text(text=f"Select the part type", reply_markup=inline.tuple_btns(PART_TYPES))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="back"), state=CarDetailStates.BRAND_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page - 1
    brands =  {item["name"]: item["id"] for item in await api.get_brands()}
    await call.message.edit_text(text="✅ Great, now I will help you.\n\n1. Write a brand\n*important to write everything in one message", 
                              reply_markup=inline.iter_btns(brands, current_page))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(), state=CarDetailStates.BRAND_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    brand_id = callback.action
    async with state.proxy() as data:
        data["brand_id"] = brand_id
    await CarDetailStates.MODEL_STATE.set()

    models = await api.get_models(brand_id)
    models = {model["name"]: model["name"] for model in models}
    await call.message.edit_text(text=f"2. Select a car model", reply_markup=inline.iter_btns(models))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="back"), state=CarDetailStates.MODEL_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page - 1
    state_data = await state.get_data()

    models = await api.get_models(state_data["brand_id"])
    models = {model["name"]: model["name"] for model in models} 
    await call.message.edit_text(text=f"2. Select a car model", reply_markup=inline.iter_btns(models, current_page))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(), state=CarDetailStates.MODEL_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    model = callback.action
    async with state.proxy() as data:
        data["model"] = model
    await CarDetailStates.YEAR_STATE.set()

    state_data = await state.get_data()
    years = await api.get_years(state_data["brand_id"], state_data["model"])
    years = {f'{car["production_start"]} - {car["production_end"]}': car["id"] for car in years}
    await CarDetailStates.YEAR_STATE.set()
    await call.message.edit_text(text=f"3. Select the year of your model", reply_markup=inline.iter_btns(years))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(action="back"), state=CarDetailStates.YEAR_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    current_page = callback.current_page - 1
    state_data = await state.get_data()

    state_data = await state.get_data()
    years = await api.get_years(state_data["brand_id"], state_data["model"])
    years = {f'{car["production_start"]} - {car["production_end"]}': car["id"] for car in years}
    await CarDetailStates.YEAR_STATE.set()
    await call.message.edit_text(text=f"3. Select the year of your model", reply_markup=inline.iter_btns(years, current_page))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(), state=CarDetailStates.YEAR_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    model_id = int(callback.action)
    async with state.proxy() as data:
        data["model_id"] = model_id
    await CarDetailStates.DETAIL_TYPE_STATE.set()
    await call.message.edit_text(text=f"Select the part type", reply_markup=inline.tuple_btns(PART_TYPES))


@dp.callback_query_handler(lambda call: IterCallback.unpack(call.data).filter(), state=CarDetailStates.DETAIL_TYPE_STATE)
async def user_no_filter(call: CallbackQuery, state: FSMContext):
    callback = IterCallback.unpack(call.data)
    async with state.proxy() as data:
        data["detail_type"] = callback.action
    await call.message.edit_text(text="5. Write spare part information", reply_markup=inline.tuple_btns([]))
    await CarDetailStates.DETAIL_NAME_STATE.set()