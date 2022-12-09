from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '530934:AAFAnuzrrZQ5aUjBsjckOrEOiG5oREkCNBI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
GROUP_DS_55_ID = -1001883554676
