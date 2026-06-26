from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database.crud import get_or_create_user, get_user, set_gender, get_all_users_count
from keyboards.main_kb import main_menu, gender_kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or ""
    )
    
    if not user.gender:
        await message.answer(
            "👋 AnonUzb ga xush kelibsiz!\n\n"
            "Bu yerda siz anonim ravishda begona odamlar bilan suhbatlasha olasiz.\n\n"
            "Avval jinsingizni tanlang:",
            reply_markup=gender_kb()
        )
    else:
        await message.answer(
            f"👋 Qaytib keldingiz!\n\nAsosiy menyu:",
            reply_markup=main_menu()
        )

@router.callback_query(F.data.startswith("gender_"))
async def set_gender_handler(call: CallbackQuery):
    gender = "male" if call.data == "gender_male" else "female"
    await set_gender(call.from_user.id, gender)
    await call.message.edit_text("✅ Saqlandi!")
    await call.message.answer("Asosiy menyu:", reply_markup=main_menu())

@router.message(F.text == "📊 Statistika")
async def stats(message: Message):
    count = await get_all_users_count()
    await message.answer(f"📊 Jami foydalanuvchilar: {count} ta")
