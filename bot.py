from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import get_csv
import os

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Uceprotect"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Ok", reply_markup=keyboard)

@dp.message_handler(Text(equals="Uceprotect"))
async def get_spam_base_info(message: types.Message):
    await message.answer("Please waiting...")
    
    get_csv()
    await message.answer("Done!")


def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()