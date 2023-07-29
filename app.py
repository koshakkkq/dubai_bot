import logging
import sys

from aiogram.utils import executor

import asyncio
from aiogram import executor
from loader import dp, bot
from register_handlers import register_handlers
from utils import api


register_handlers(dp)
async def on_startup(dp):
    me = await bot.get_me()
    logging.error(f'Running {me.username}')

import courier
import shop
import user


async def shop_notify(wait):
    while True:
        notify = await api.get_notifications()
        for user_id, text in notify.items():
            await bot.send_message(user_id, text)
        await asyncio.sleep(wait)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(shop_notify(60*60)) # every hour
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)