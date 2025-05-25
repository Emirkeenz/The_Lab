import os
from telegram import Update
from telegram.ext import ContextTypes

from utils.parser import extract_text_from_file, split_text_into_chunks, save_chunks_to_json, build_rag_index
from utils.ollama_client import summarize_text

LESSONS_DIR = "uploaded_lessons"

# === Команда /upload_lesson ===
async def upload_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text("⚠️ Пожалуйста, отправь документ (PDF или DOCX) после команды /upload_lesson.")
        return

    document = update.message.document
    file = await document.get_file()
    os.makedirs(LESSONS_DIR, exist_ok=True)
    file_path = os.path.join(LESSONS_DIR, document.file_name)
    await file.download_to_drive(file_path)

    try:
        text = extract_text_from_file(file_path)
        chunks = split_text_into_chunks(text)
        save_chunks_to_json(chunks, "math", document.file_name)
        build_rag_index(chunks, "math", document.file_name)  # 💡 создаём RAG-индекс сразу

        await update.message.reply_text(
            f"✅ Урок «{document.file_name}» успешно загружен и проиндексирован.\nНапиши /start_lesson {document.file_name.split('.')[0]} 📖"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при обработке файла: {str(e)}")
