from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
API_TOKEN = '5366990934:AAFAnuzrrZQ5aUjBsjckOrEOiG5oREkCNBI'
#
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
GROUP_DS_55_ID = -1001883554676
SUPER_USER_IDS = [176814724, 29720838]  # Список ID пользователей с немного большими правами, чем у остальных =)
