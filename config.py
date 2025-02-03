import os

TOKEN = os.getenv("7747675920:AAHRIDxJmbDofxd66weCkpqrmsnQd79g8oc")  # Загружаем токен из переменной окружения

if not TOKEN:
    raise ValueError("🚨 BOT_TOKEN не найден! Проверь Environment Variables.")

print(f"✅ BOT_TOKEN загружен: {TOKEN[:10]}***")  # Выводит часть токена для проверки
