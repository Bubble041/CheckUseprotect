from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import get_csv
import os

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):

    start_buttons = ["Uceprotect", "SpamHouse"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Выберите спам-базу", reply_markup=keyboard)

@dp.message_handler(commands="help")
async def start(message: types.Message):

    start_buttons = ["Uceprotect", "SpamHouse"]
    await message.answer("Выберите спам-базу, затем в каком диапазоне адресов вы хотите получить информацию.")

@dp.message_handler(Text(equals="Uceprotect"))
async def range_selection(message: types.Message):

    pool_buttons = ["ASN", "IP"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*pool_buttons)
    await message.answer("Выберите диапазон:", reply_markup=keyboard)

@dp.message_handler(Text(equals="ASN"))
async def set_asn(message: types.Message):

    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Please waiting...")
    get_csv('Uceprotect', 'ASN', '9123')
    await message.answer("Done!")

    pool_buttons = ["/start"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*pool_buttons)
    await message.answer("Нажмите /start, чтобы повторить:", reply_markup=keyboard)

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()