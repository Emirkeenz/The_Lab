import os
import logging
from telegram import Update, Document
from telegram.ext import ContextTypes

from utils.parser import extract_text_from_file, split_text_into_chunks

LESSONS_DIR = "uploaded_lessons"

# === Команда /upload_lesson ===
async def upload_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message.document:
        await message.reply_text("⚠️ Пожалуйста, отправь документ (PDF или DOCX) после команды /upload_lesson.")
        return

    document: Document = message.document
    file_name = document.file_name

    # Скачивание файла
    file = await document.get_file()
    file_path = os.path.join(LESSONS_DIR, file_name)
    await file.download_to_drive(file_path)

    # Обработка файла
    try:
        raw_text = extract_text_from_file(file_path)
        chunks = split_text_into_chunks(raw_text)

        # Сохраняем в контексте для этого пользователя
        context.user_data["lesson_chunks"] = chunks
        context.user_data["lesson_index"] = 0

        await message.reply_text(
            f"✅ Урок «{file_name}» успешно загружен.\nГотов начать? Напиши «начать урок» 📖"
        )
    except Exception as e:
        logging.error(f"Ошибка при обработке урока: {e}")
        await message.reply_text("❌ Не удалось обработать файл. Убедись, что это PDF или DOCX.")
