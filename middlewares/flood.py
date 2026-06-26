from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import time

user_last_message = {}

class FloodMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        user_id = event.from_user.id
        now = time.time()
        last = user_last_message.get(user_id, 0)
        if now - last < 0.5:
            await event.answer("⚠️ Iltimos, sekinroq yozing!")
            return
        user_last_message[user_id] = now
        return await handler(event, data)
