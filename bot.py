from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Клавиатура выбора типа продукта
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Растения"), KeyboardButton("Косметика"))
keyboard.add(KeyboardButton("Ювелирные изделия"), KeyboardButton("Стекло"))
keyboard.add(KeyboardButton("Фарфор"), KeyboardButton("Изделия из металла"))
keyboard.add(KeyboardButton("Ввести своё"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я помогу рассчитать стоимость e-commerce фотографии.\nСколько продуктов вы хотите сфотографировать?", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text.isdigit())
async def get_products_count(message: types.Message):
    await message.answer("Сколько фотографий нужно на один продукт?")

@dp.message_handler(lambda message: message.text.isdigit())
async def get_photos_per_product(message: types.Message):
    await message.answer("Выберите тип продукта:", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


