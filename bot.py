import os
import logging
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# 🔹 Настройки токенов (загружаются из переменных окружения)
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("NEWS_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://elon-musk-news-bot.onrender.com")

# 🔹 Логирование (выводит информацию в консоль Render)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Функция для получения новостей про Илона Маска
def get_news():
    url = f"https://newsapi.org/v2/everything?q=Elon+Musk&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        news_list = [f"🔹 {a['title']}\n{a['url']}" for a in articles[:5]]
        return "\n\n".join(news_list) if news_list else "🔸 Свежих новостей нет."
    else:
        return "❌ Ошибка при получении новостей."

# 🔹 Функция обработки команды /news
async def news_command(update: Update, context: CallbackContext) -> None:
    news = get_news()
    await update.message.reply_text(news)

# 🔹 Функция обработки команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот новостей про Илона Маска.\n\nНапиши /news, чтобы узнать свежие новости.")

# 🔹 Инициализация бота
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("news", news_command))

# 🔹 Функция для установки вебхука
async def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}/"
    await app.bot.set_webhook(webhook_url)
    logger.info(f"✅ Webhook установлен: {webhook_url}")

# 🔹 Запуск бота (работает и в локальном режиме, и на Render)
async def main():
    await set_webhook()
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}/"
    )

# 🔹 Запуск в зависимости от среды выполнения
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
