import logging
import sys

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.dispatcher import filters
import asyncio
from aiogram import executor, types
from loader import dp, bot
from config import GROUP_ID

@dp.channel_post_handler(
    filters.Text(equals='/get_channel_id')
)
async def get_channel_id(message):
    await message.answer(message.chat.id)



class States(StatesGroup):
    pending = State()
@dp.message_handler(
    commands=['start', 'new'],
    state='*',
)
async def start(message, state):
    await state.set_state(States.pending)
    await message.answer('We are very sorry that while using our bot (@cars_dubai_bot) you have any problems, write your problem and a support employee will contact you in the near future!')

@dp.message_handler(
    state=States.pending,
)
async def send_to_channel(message: types.Message, state):
    msg = f"New issue from <a href='tg://user?id={message.from_user.id}'>USER</a>\n" \
          f"Text from user: {message.text}" \


    await bot.send_message(
        GROUP_ID,
        text=msg,
        parse_mode='HTML',
    )
    await message.answer('Thank you, we will contact you soon. Type /new, if you want to create a new appeal.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)