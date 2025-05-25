import os
import json
from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import load_or_build_index
from utils.ollama_client import summarize_text, query_ollama
from llama_index.core.settings import Settings

CHUNKS_DIR = "lesson_chunks"

# === Команда /start_lesson <имя> ===
async def start_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        available = list_available_lessons()
        msg = "⚠️ Укажи название урока: /start_lesson <название>\n\nДоступные уроки:\n" + "\n".join(available)
        await update.message.reply_text(msg)
        return

    lesson_name = args[0].split('.')[0]  # убираем расширение
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in lesson_name)
    file_path = f"{CHUNKS_DIR}/math/{safe_name}.json"

    if not os.path.exists(file_path):
        await update.message.reply_text(f"⚠️ Урок «{lesson_name}» не найден. Загрузите его через /upload_lesson.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    context.user_data.update({
        "lesson_name": safe_name,
        "lesson_chunks": chunks,
        "lesson_index": 0,
        "lesson_index_obj": load_or_build_index(chunks, "math", lesson_name),
    })

    # 🔍 Саммари
    summary = summarize_text("\n".join(chunks[:5]))  # первые 5 кусков — обычно ввод
    await update.message.reply_text(f"📘 Саммари урока «{lesson_name}»:\n\n{summary}\n\nГотов задать вопрос или пиши «всё понятно» для завершения.")

# === Обработка сообщений ученика ===
async def handle_lesson_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_data = context.user_data

    if "lesson_chunks" not in user_data or "lesson_index_obj" not in user_data:
        await update.message.reply_text("⚠️ Урок не загружен. Напиши /start_lesson <имя_урока>")
        return

    if "всё понятно" in text:
        await update.message.reply_text("🎉 Отлично! Урок завершён. Если хочешь продолжить — выбери другой файл.")
        context.user_data.clear()
        return

    Settings.llm = None

    index = user_data["lesson_index_obj"]
    query_engine = index.as_query_engine()
    response = query_engine.query(text)
    await update.message.reply_text(f"🤖 Ответ:\n{response}")

# === Показать список доступных уроков ===
def list_available_lessons():
    folder = os.path.join(CHUNKS_DIR, "math")
    if not os.path.exists(folder):
        return []
    return [f.replace(".json", "") for f in os.listdir(folder) if f.endswith(".json")]
