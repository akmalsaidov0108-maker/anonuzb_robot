import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8862525079:AAHLdUhiaOaSJTU_yDcsCgfhLFbd2YXU5jc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

waiting_users = []
active_chats = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Salom! Bu anonim chat boti.\n\n"
        "Notanish odam bilan suhbat boshlash uchun /search bosing.\n"
        "Suhbatni tugatish uchun /stop bosing."
    )

@dp.message(Command("search"))
async def search(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_chats:
        await message.answer("Siz allaqachon suhbatdasiz. Tugatish uchun /stop bosing.")
        return
    if user_id in waiting_users:
        await message.answer("Juft qidirilmoqda... Kuting.")
        return
    if waiting_users:
        partner_id = waiting_users.pop(0)
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id
        await bot.send_message(user_id, "Juft topildi! Suhbat boshlandi. /stop — tugatish.")
        await bot.send_message(partner_id, "Juft topildi! Suhbat boshlandi. /stop — tugatish.")
    else:
        waiting_users.append(user_id)
        await message.answer("Juft qidirilmoqda... Kuting.")

@dp.message(Command("stop"))
async def stop(message: types.Message):
    user_id = message.from_user.id
    if user_id in waiting_users:
        waiting_users.remove(user_id)
        await message.answer("Qidiruv bekor qilindi.")
        return
    if user_id in active_chats:
        partner_id = active_chats.pop(user_id)
        active_chats.pop(partner_id, None)
        await message.answer("Suhbat tugatildi. Yangi juft uchun /search bosing.")
        await bot.send_message(partner_id, "Suhbatdosh suhbatni tugatdi. Yangi juft uchun /search bosing.")
    else:
        await message.answer("Siz hozir suhbatda emassiz.")

@dp.message()
async def relay(message: types.Message):
    user_id = message.from_user.id
    if user_id not in active_chats:
        await message.answer("Suhbat yo'q. /search bosing.")
        return
    partner_id = active_chats[user_id]
    if message.text:
        await bot.send_message(partner_id, message.text)
    elif message.photo:
        await bot.send_photo(partner_id, message.photo[-1].file_id)
    elif message.voice:
        await bot.send_voice(partner_id, message.voice.file_id)
    elif message.sticker:
        await bot.send_sticker(partner_id, message.sticker.file_id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
