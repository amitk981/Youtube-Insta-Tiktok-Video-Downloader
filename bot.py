import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import commands, messages

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set in .env file")
        return

    from aiogram.client.session.aiohttp import AiohttpSession
    from aiohttp import ClientTimeout
    
    # Increase timeout for large file uploads
    # total=None disables the total operation timeout
    # connect=60 gives 60s to establish connection
    # sock_read=600 gives 10 mins for reading data (uploading)
    timeout = ClientTimeout(total=None, connect=60, sock_read=600)
    session = AiohttpSession(timeout=timeout)
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    # Include routers
    dp.include_router(commands.router)
    dp.include_router(messages.router)

    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
