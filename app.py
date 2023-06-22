import logging
from aiogram import executor
from loader import dp, bot
from register_handlers import register_handlers
import asyncio
from user import handlers, filters



register_handlers(dp)
async def on_startup(dp):
    me = await bot.get_me()
    logging.error(f'Running {me.username}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)