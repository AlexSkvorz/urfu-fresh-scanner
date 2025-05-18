from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.classifier import FreshClassifier

class ClassifierMiddleware(BaseMiddleware):
    def __init__(self, classifier: FreshClassifier):
        self.classifier = classifier

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["classifier"] = self.classifier
        return await handler(event, data)
