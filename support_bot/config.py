from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent
API_TOKEN = config('BOT_TOKEN', default="", cast=str)
GROUP_ID = config('GROUP_ID', default="", cast=int)