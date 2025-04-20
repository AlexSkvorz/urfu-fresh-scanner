import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message()
async def handle_message(message: types.Message):
    await message.answer(f"Я пока не знаю такую команду :(")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
