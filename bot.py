import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Токен Telegram-бота
TOKEN = "7924106666:AAGd-HK2cfXRkNmLtrXVrV1j80HuPpAfSAk"

# API-ключ для NewsAPI
API_KEY = "0d8117b87d1949f9808c47112650cfab"

# Логирование
logging.basicConfig(level=logging.INFO)

# Функция для получения новостей
def get_news():
    URL = f"https://newsapi.org/v2/everything?q=Elon+Musk&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        news_list = []
        for article in articles[:5]:  # Берём 5 последних новостей
            title = article["title"]
            link = article["url"]
            news_list.append(f"🔹 {title}\n{link}")

        return "\n\n".join(news_list) if news_list else "Новостей нет."
    else:
        return "Ошибка при получении новостей."

# Функция обработки команды /news
async def news_command(update: Update, context: CallbackContext) -> None:
    news = get_news()
    await update.message.reply_text(news)

# Создаём бота
app = Application.builder().token(TOKEN).build()

async def start_webhook():
    await app.bot.set_webhook(f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook/{TOKEN}")

# Запуск бота
def main():
    PORT = int(os.environ.get("PORT", 8443))

    # Запускаем webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"webhook/{TOKEN}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_webhook())  # Устанавливаем webhook перед запуском
    main()
