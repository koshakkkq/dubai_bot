import logging
import sys

from aiogram.utils import executor

import asyncio
from aiogram import executor
from loader import dp, bot
from register_handlers import register_handlers

register_handlers(dp)
async def on_startup(dp):
    me = await bot.get_me()
    logging.error(f'Running {me.username}')

import courier
import shop
import user





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)