import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import dashscope
from dashscope import Generation

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

dashscope.api_key = DASHSCOPE_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на базе Qwen. Напиши мне что-нибудь 👇")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id
    logger.info(f"User {user_id} sent: {user_text}")

    try:
        # Вызов Qwen (можно выбрать qwen-turbo / qwen-plus / qwen-max)
        response = Generation.call(
            model="qwen-turbo",  # или "qwen-plus", "qwen-max"
            prompt=user_text
        )
        answer = response.output.text.strip()
    except Exception as e:
        logger.error(f"Ошибка DashScope: {e}")
        answer = "⚠️ Ошибка при генерации ответа. Попробуйте позже."

    await update.message.reply_text(answer)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()