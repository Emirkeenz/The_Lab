import logging
from dotenv import load_dotenv
import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Загрузка токенов из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Импорт хендлеров
from handlers.menu import start, subject_choice
from handlers.lessons import upload_lesson
from handlers.messages import start_lesson, handle_lesson_message

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("upload_lesson", upload_lesson))
    app.add_handler(CommandHandler("start_lesson", start_lesson))

    app.add_handler(MessageHandler(filters.Document.PDF | filters.Document.DOCX, upload_lesson))

    # Выбор предмета / уровня
    app.add_handler(CallbackQueryHandler(subject_choice, pattern="^subject_"))

    # Сообщения от пользователя
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_lesson_message))

    logging.info("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
