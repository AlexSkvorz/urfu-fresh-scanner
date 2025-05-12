import asyncio
from aiogram import Bot, Dispatcher

from bot import handlers
from bot.config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(
        handlers.router,
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
