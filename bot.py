import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import config

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

# Клавиатура выбора типа продукта
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Растения"), KeyboardButton("Косметика"))
keyboard.add(KeyboardButton("Ювелирные изделия"), KeyboardButton("Стекло"))
keyboard.add(KeyboardButton("Фарфор"), KeyboardButton("Изделия из металла"))
keyboard.add(KeyboardButton("Ввести своё"))

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я помогу рассчитать стоимость e-commerce фотографии.\nСколько продуктов вы хотите сфотографировать?", reply_markup=types.ReplyKeyboardRemove())

# Обработчик ввода количества продуктов
@dp.message(lambda message: message.text.isdigit())
async def get_products_count(message: types.Message):
    await message.answer("Сколько фотографий нужно на один продукт?")

# Обработчик ввода количества фото на продукт
@dp.message(lambda message: message.text.isdigit())
async def get_photos_per_product(message: types.Message):
    await message.answer("Выберите тип продукта:", reply_markup=keyboard)

# Функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



