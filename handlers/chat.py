from aiogram import Router, F
from aiogram.types import Message
from database.crud import get_user, disconnect_user
from keyboards.main_kb import main_menu

router = Router()

@router.message(F.text == "⏹ To'xtatish")
async def stop_chat(message: Message, bot):
    user = await get_user(message.from_user.id)
    
    if user.is_searching:
        await disconnect_user(message.from_user.id)
        await message.answer("❌ Qidiruv to'xtatildi.", reply_markup=main_menu())
        return
    
    if user.partner_id:
        partner_id = user.partner_id
        await disconnect_user(message.from_user.id)
        await disconnect_user(partner_id)
        await message.answer("❌ Suhbat tugatildi.", reply_markup=main_menu())
        await bot.send_message(partner_id, "❌ Suhbatdosh chiqib ketdi.", reply_markup=main_menu())
    else:
        await message.answer("Siz hozir hech kim bilan suhbatlashmayapsiz.", reply_markup=main_menu())

@router.message()
async def relay_message(message: Message, bot):
    user = await get_user(message.from_user.id)
    
    if not user or not user.partner_id:
        return
    
    try:
        if message.text:
            await bot.send_message(user.partner_id, f"👤 {message.text}")
        elif message.photo:
            await bot.send_photo(user.partner_id, message.photo[-1].file_id, caption="👤 Rasm")
        elif message.voice:
            await bot.send_voice(user.partner_id, message.voice.file_id)
        elif message.video:
            await bot.send_video(user.partner_id, message.video.file_id)
        elif message.sticker:
            await bot.send_sticker(user.partner_id, message.sticker.file_id)
    except Exception:
        await disconnect_user(message.from_user.id)
        await message.answer("⚠️ Xatolik yuz berdi. Suhbat tugadi.", reply_markup=main_menu())
