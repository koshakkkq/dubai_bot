from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import config_parse

config = config_parse()

#client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')


API_TOKEN = config['tg_token']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())