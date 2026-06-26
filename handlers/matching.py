from aiogram import Router, F
from aiogram.types import Message
from database.crud import get_user, set_searching
from utils.matching import find_partner
from keyboards.main_kb import stop_kb
import asyncio

router = Router()

@router.message(F.text == "🎲 Tasodifiy suhbat")
async def random_chat(message: Message, bot):
    user = await get_user(message.from_user.id)
    if user.partner_id:
        await message.answer("⚠️ Siz allaqachon suhbatdasiz. Avval ⏹ To'xtatish tugmasini bosing.")
        return
    
    await message.answer("🔍 Suhbatdosh qidiryapman...", reply_markup=stop_kb())
    asyncio.create_task(find_partner(bot, message.from_user.id))

@router.message(F.text == "👦 Erkak qidirish")
async def find_male(message: Message, bot):
    user = await get_user(message.from_user.id)
    if user.partner_id:
        await message.answer("⚠️ Avval joriy suhbatni tugatng.")
        return
    await message.answer("🔍 Erkak suhbatdosh qidiryapman...", reply_markup=stop_kb())
    asyncio.create_task(find_partner(bot, message.from_user.id, gender_filter="male"))

@router.message(F.text == "👧 Ayol qidirish")
async def find_female(message: Message, bot):
    user = await get_user(message.from_user.id)
    if user.partner_id:
        await message.answer("⚠️ Avval joriy suhbatni tugatng.")
        return
    await message.answer("🔍 Ayol suhbatdosh qidiryapman...", reply_markup=stop_kb())
    asyncio.create_task(find_partner(bot, message.from_user.id, gender_filter="female"))
