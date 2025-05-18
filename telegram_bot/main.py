import asyncio
from aiogram import Bot, Dispatcher

from bot import handlers
from bot.classifier import FreshClassifier
from bot.config import BOT_TOKEN
from bot.middlewares import ClassifierMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.middleware(
        ClassifierMiddleware(
            FreshClassifier()
        )
    )
    dp.include_router(
        handlers.router,
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
