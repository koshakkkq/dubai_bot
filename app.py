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
        while True:
            notify = await api.get_notifications()

            for user_id, (text, keyboard) in notify.items():
                try:
                    await bot.send_message(user_id, text, reply_markup=keyboard)
                except Exception as e:
                    logging.error(e)
            if len(notify) == 0:
                await asyncio.sleep(wait)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(shop_notify(5*60)) # every 5 min
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)