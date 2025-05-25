from telegram import Update
from telegram.ext import ContextTypes

# 👋 /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я AI-репетитор по математике.\n\n"
        "Напиши /help чтобы узнать, как использовать бота."
    )

# ℹ️ /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 Что я умею:\n"
        "Этот бот помогает изучать уроки по математике с помощью ИИ.\n\n"
        "📚 Команды:\n"
        "/upload_lesson – Загрузить PDF или DOCX файл урока\n"
        "/start_lesson <название> – Начать изучение урока\n"
        "после чего можно задавать вопросы по содержанию.\n\n"
        "Напиши 'всё понятно', чтобы завершить урок."
    )
