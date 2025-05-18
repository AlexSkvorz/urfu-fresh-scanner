import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from bot.classifier import FreshClassifier

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!"
                         f" Я умею распознавать свежесть продуктов по фото."
                         f" Пришли мне фото продукта, свежесть которого нужно оценить.")


@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot, classifier: FreshClassifier):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)

    save_dir = "photos"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{photo.file_id}.jpg")

    await bot.download_file(file_info.file_path, destination=file_path)
    result = classifier.predict(file_path)
    os.remove(file_path)

    if result is None:
        await message.answer("Не нашел продуктов на фото :(")
        return

    await message.answer(
        f"На фото обнаружен продукт: {result.name}\n" +
        f"Степень свежести: {result.fresh_percent}%"
    )


@router.message()
async def handle_message(message: Message):
    await message.answer(f"Пришли мне фото продукта, свежесть которого нужно оценить")
