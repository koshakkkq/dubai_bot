from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent
API_TOKEN = config('BOT_TOKEN', default="", cast=str)
DATABASE_URL = config('DATABASE_URL', default="", cast=str)
print(API_TOKEN)