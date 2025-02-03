import os

TOKEN = os.getenv("7747675920:AAHRIDxJmbDofxd66weCkpqrmsnQd79g8oc")

if TOKEN is None:
    raise ValueError("🚨 BOT_TOKEN не найден! Проверь Environment Variables.")
