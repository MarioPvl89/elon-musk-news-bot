import logging
import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import nest_asyncio

# Применяем патч для предотвращения ошибки "RuntimeError: This event loop is already running"
nest_asyncio.apply()

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = f"https://elon-musk-news-bot.onrender.com/{TOKEN}/"

# Проверка наличия токена
if not TOKEN:
    logger.error("❌ Токен бота не найден! Убедитесь, что переменная окружения TELEGRAM_TOKEN установлена.")
    exit(1)

# Функция для команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я бот новостей про Илона Маска 🚀.")

# Основная асинхронная функция
async def main():
    try:
        # Создаем приложение Telegram бота
        app = Application.builder().token(TOKEN).build()

        # Добавляем обработчики команд
        app.add_handler(CommandHandler("start", start))

        # Устанавливаем webhook
        await app.bot.set_webhook(WEBHOOK_URL)
        logger.info(f"✅ Webhook установлен: {WEBHOOK_URL}")

        # Запуск бота через webhook
        await app.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=TOKEN,
            webhook_url=WEBHOOK_URL,
        )

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}", exc_info=True)

# Запуск бота
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(main())  # Если event loop уже запущен
    else:
        asyncio.run(main())  # Если event loop не запущен
