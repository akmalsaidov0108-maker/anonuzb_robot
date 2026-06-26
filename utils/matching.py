import asyncio
from database.crud import get_waiting_user, set_searching, set_partner, get_user
from aiogram import Bot

async def find_partner(bot: Bot, user_id: int, gender_filter=None):
    await set_searching(user_id, True)
    
    for _ in range(30):
        partner = await get_waiting_user(exclude_id=user_id, gender_filter=gender_filter)
        if partner:
            await set_partner(user_id, partner.telegram_id)
            await set_partner(partner.telegram_id, user_id)
            
            await bot.send_message(user_id, "✅ Suhbatdosh topildi! Yozing...")
            await bot.send_message(partner.telegram_id, "✅ Suhbatdosh topildi! Yozing...")
            return True
        await asyncio.sleep(2)
    
    await set_searching(user_id, False)
    await bot.send_message(user_id, "😔 Suhbatdosh topilmadi. Qayta urinib ko'ring.")
    return False
