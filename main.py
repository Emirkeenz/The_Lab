from telegram.ext import Application, CommandHandler, MessageHandler
from telegram import BotCommand
from handlers.messages import start_lesson, handle_lesson_message
from handlers.commands import start_command, help_command
from handlers.lessons import upload_lesson  # если есть
from telegram.ext import filters
from dotenv import load_dotenv
import os
import logging

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # 🔘 Команды
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start_lesson", start_lesson))
    app.add_handler(CommandHandler("upload_lesson", upload_lesson))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_lesson_message))
    app.add_handler(MessageHandler(filters.Document.PDF | filters.Document.DOCX, upload_lesson))

    # 📋 Установка меню команд
    app.bot.set_my_commands([
        BotCommand("start", "Начать работу с ботом"),
        BotCommand("help", "Помощь и описание команд"),
        BotCommand("upload_lesson", "Загрузить урок"),
        BotCommand("start_lesson", "Начать изучение урока"),
    ])

    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
