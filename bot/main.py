import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from database.crud import init_db
from middlewares.flood import FloodMiddleware
from handlers import start, matching, chat, admin

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    dp.message.middleware(FloodMiddleware())
    
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(matching.router)
    dp.include_router(chat.router)
    
    await init_db()
    
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
