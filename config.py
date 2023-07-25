from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent
API_TOKEN = config('BOT_TOKEN', default="", cast=str)
SERVER_URL = config('SERVER_URL', default="", cast=str)
PAYMENT_TOKEN = config('PAYMENT_TOKEN', default="", cast=str)