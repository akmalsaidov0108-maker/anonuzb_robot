from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🎲 Tasodifiy suhbat")],
        [KeyboardButton(text="👦 Erkak qidirish"), KeyboardButton(text="👧 Ayol qidirish")],
        [KeyboardButton(text="⏹ To'xtatish"), KeyboardButton(text="📊 Statistika")],
    ], resize_keyboard=True)

def gender_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👦 Erkakman", callback_data="gender_male")],
        [InlineKeyboardButton(text="👧 Ayolman", callback_data="gender_female")],
    ])

def stop_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⏹ To'xtatish")],
    ], resize_keyboard=True)
