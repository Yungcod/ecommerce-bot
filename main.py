import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загружаем переменные из Railway
TOKEN = os.getenv("TOKEN")
NOTIFICATION_USER_ID = int(os.getenv("NOTIFICATION_USER_ID"))

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура выбора типа продукта
product_buttons = [
    [KeyboardButton(text="Растения"), KeyboardButton(text="Косметика")],
    [KeyboardButton(text="Ювелирные изделия"), KeyboardButton(text="Стекло")],
    [KeyboardButton(text="Фарфор"), KeyboardButton(text="Изделия из металла")],
    [KeyboardButton(text="Ввести своё")]
]
product_keyboard = ReplyKeyboardMarkup(keyboard=product_buttons, resize_keyboard=True)

# Классификация материалов
MATERIAL_CATEGORIES = {
    "Растения": "обычный",
    "Косметика": "обычный",
    "Ювелирные изделия": "сложный",
    "Стекло": "сложный",
    "Фарфор": "обычный",
    "Изделия из металла": "сложный",
}

# Хранилище данных пользователей (без базы)
user_data = {}

# Хендлер старта
@dp.message(CommandStart())
async def start_command(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Привет! Сколько продуктов вы хотите сфотографировать?")

# Получаем количество продуктов
@dp.message(lambda message: message.text.isdigit())
async def process_product_count(message: types.Message):
    user_data[message.from_user.id]["products"] = int(message.text)
    await message.answer("Сколько фотографий нужно на один продукт?")

# Получаем количество фотографий
@dp.message(lambda message: message.text.isdigit())
async def process_photo_count(message: types.Message):
    user_data[message.from_user.id]["photos_per_product"] = int(message.text)
    await message.answer("Выберите тип продукта или введите свой:", reply_markup=product_keyboard)

# Обрабатываем выбор типа продукта
@dp.message()
async def process_product_type(message: types.Message):
    user_id = message.from_user.id
    product_type = message.text
    
    if product_type in MATERIAL_CATEGORIES:
        material_type = MATERIAL_CATEGORIES[product_type]
    else:
        material_type = "сложный" if any(word in product_type.lower() for word in ["стекло", "металл", "золото", "серебро"]) else "обычный"
    
    user_data[user_id]["material"] = material_type
    
    # Рассчитываем стоимость
    products = user_data[user_id]["products"]
    photos_per_product = user_data[user_id]["photos_per_product"]
    
    shoot_speed = 5 if material_type == "обычный" else 2.5
    processing_cost = 250 if material_type == "обычный" else 500
    hourly_rate = 1500
    
    hours_needed = (products / shoot_speed)
    shoot_cost = hours_needed * hourly_rate
    processing_cost_total = products * photos_per_product * processing_cost
    total_cost = shoot_cost + processing_cost_total
    
    response = (f"Примерная стоимость вашего проекта: {int(total_cost)} Kč.\n"
                "Пожалуйста, примите во внимание, что расчёт автоматический и может измениться.")
    
    await message.answer(response)
    
    # Отправка уведомления девушке
    notification_message = (f"Поступил новый заказ!\n"
                             f"Продукты: {products}\n"
                             f"Фото на продукт: {photos_per_product}\n"
                             f"Материал: {material_type}\n"
                             f"Оценочная стоимость: {int(total_cost)} Kč.")
    await bot.send_message(NOTIFICATION_USER_ID, notification_message)

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

