import os
import logging
from telegram import Update, Document
from telegram.ext import ContextTypes

from utils.parser import extract_text_from_file, split_text_into_chunks, save_chunks_to_json

LESSONS_DIR = "uploaded_lessons"

# === Команда /upload_lesson ===
async def upload_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("⚠️ Пожалуйста, отправь документ (PDF или DOCX) после команды /upload_lesson.")
        return

    document = update.message.document
    file = await document.get_file()
    file_path = os.path.join("uploaded_lessons", document.file_name)
    os.makedirs("uploaded_lessons", exist_ok=True)
    await file.download_to_drive(file_path)

    try:
        text = extract_text_from_file(file_path)
        chunks = split_text_into_chunks(text)
        save_chunks_to_json(chunks, document.file_name, subject="math")

        await update.message.reply_text(
            f"✅ Урок «{document.file_name}» успешно загружен.\nГотов начать? Напиши «начать урок» 📖")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при обработке файла: {str(e)}")
