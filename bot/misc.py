"""
Connecting to a bot by configuration
"""
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from configs.bot import BotConfig

storage = MemoryStorage()
bot = Bot(token=BotConfig().api_token.get_secret_value())
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
