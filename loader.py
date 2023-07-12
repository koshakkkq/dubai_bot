from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import config




engine = create_async_engine(
    config.DATABASE_URL,
    #echo=True, #выводит запросы
)
sessions = sessionmaker(bind=engine,class_=AsyncSession,)

info_log = logging.FileHandler(config.BASE_DIR/'log/info.log')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(info_log, console_out), level=logging.INFO,
                    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
#client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')