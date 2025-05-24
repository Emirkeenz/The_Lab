from telegram import Update
from telegram.ext import ContextTypes
import json
import os

# === Начало урока (по команде «начать урок» или сообщению) ===
async def start_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data

    if not context.args:
        await update.message.reply_text("❗ Укажи название урока: /start_lesson <название>")
        return

    lesson_name = context.args[0]
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in lesson_name)
    file_path = f"lesson_chunks/math/{safe_name}.json"

    if not os.path.exists(file_path):
        await update.message.reply_text(
            f"⚠️ Урок «{lesson_name}» не найден. Убедись, что он загружен."
        )
        return

    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        user_data["lesson_chunks"] = chunks
        user_data["lesson_index"] = 0

    await send_current_chunk(update, context)


# === Отправка текущей части урока ===
async def send_current_chunk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = context.user_data

    if "lesson_chunks" not in user_data or "lesson_index" not in user_data:
        await update.message.reply_text("⚠️ Урок не загружен.")
        return

    chunks = user_data["lesson_chunks"]
    index = user_data["lesson_index"]

    if index >= len(chunks):
        await update.message.reply_text("✅ Урок завершён!")
        return

    current_text = chunks[index].strip()

    if not current_text:
        await update.message.reply_text("⚠️ Текущий фрагмент урока пустой.")
        return

    # 🚨 Разбиваем длинный текст
    MAX_LENGTH = 4096
    for i in range(0, len(current_text), MAX_LENGTH):
        await update.message.reply_text(current_text[i:i + MAX_LENGTH])


# === Обработка сообщений ученика во время урока ===
async def handle_lesson_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    text = update.message.text.lower()

    if "lesson_chunks" not in user_data:
        await update.message.reply_text(
            "⚠️ Урок не загружен. Попроси репетитора сначала загрузить материал."
        )
        return

    idx = user_data.get("lesson_index", 0)
    chunks = user_data.get("lesson_chunks", [])

    if idx >= len(chunks):
        # Урок уже закончен
        if "вопрос" in text:
            await update.message.reply_text("Задай свой вопрос, я постараюсь помочь!")
        else:
            await update.message.reply_text("Урок уже завершён. Чтобы начать новый, попроси загрузить материал.")
        return

    if "объясни проще" in text:
        # Логика упрощения — здесь можно запросить AI с подсказкой "объясни проще"
        simplified_text = await get_simplified_text(chunks[idx])
        await update.message.reply_text(simplified_text)

    elif "следующий" in text:
        user_data["lesson_index"] = idx + 1
        await send_current_chunk(update, context)

    else:
        # Любой другой ответ — можно проверить, закрепить материал, задать вопрос и т.п.
        await update.message.reply_text(
            "Если хочешь объяснений — напиши «объясни проще», "
            "если готов продолжать — «следующий»."
        )


# === Функция для запроса упрощённого текста у AI ===
async def get_simplified_text(text: str) -> str:
    # Тут будет вызов Ollama через utils/ollama_client.py (позже сделаем)
    prompt = f"Объясни проще этот текст:\n\n{text}"
    # Заглушка пока:
    return f"Упрощённая версия:\n{prompt}"
