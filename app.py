import logging
import sys

from aiogram.utils import executor

import db
import asyncio
from aiogram import executor
from loader import dp, bot, engine
from register_handlers import register_handlers


async def db_init_models(kek: str = None):
    await db.init_models(engine=engine)
    print('inited_models')
    await asyncio.sleep(3)




register_handlers(dp)
async def on_startup(dp):
    me = await bot.get_me()
    logging.error(f'Running {me.username}')






if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init_models':
        loop = asyncio.new_event_loop()
        loop.run_until_complete(db_init_models())
    else:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)