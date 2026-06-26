from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.crud import ban_user, get_all_users_count, get_user
from config import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    count = await get_all_users_count()
    await message.answer(
        f"🛡 Admin panel\n\n"
        f"👥 Foydalanuvchilar: {count}\n\n"
        f"Buyruqlar:\n"
        f"/ban [user_id] - Bloklash\n"
        f"/stats - Statistika"
    )

@router.message(Command("ban"))
async def ban_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Foydalanish: /ban [user_id]")
        return
    try:
        target_id = int(args[1])
        await ban_user(target_id)
        await message.answer(f"✅ {target_id} bloklandi.")
    except ValueError:
        await message.answer("❌ Noto'g'ri ID")
