import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Получаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 8443))

# Создаем объект приложения
app = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я бот для новостей про Илона Маска 🚀")

# Добавляем обработчик команд
app.add_handler(CommandHandler("start", start))

# Запуск вебхука
async def main():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}/"
    logging.info(f"✅ Webhook установлен: {webhook_url}")
    
    await app.bot.set_webhook(url=webhook_url)
    
    # Определяем event loop и запускаем вебхук
    loop = asyncio.get_running_loop()
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    asyncio.run(main())  # Render поддерживает asyncio.run()
