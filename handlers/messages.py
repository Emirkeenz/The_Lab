from telegram import Update
from telegram.ext import ContextTypes

# === Начало урока (по команде «начать урок» или сообщению) ===
async def start_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data

    if "lesson_chunks" not in user_data:
        await update.message.reply_text(
            "⚠️ Урок не загружен. Попроси репетитора сначала загрузить материал."
        )
        return

    user_data["lesson_index"] = 0
    await send_current_chunk(update, context)


# === Отправка текущей части урока ===
async def send_current_chunk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    idx = user_data.get("lesson_index", 0)
    chunks = user_data.get("lesson_chunks", [])

    if idx >= len(chunks):
        await update.message.reply_text(
            "🎉 Поздравляю! Урок завершён. Если есть вопросы — задавай, иначе можешь перейти к следующему уроку."
        )
        return

    current_text = chunks[idx]
    await update.message.reply_text(current_text)
    await update.message.reply_text(
        "Напиши «объясни проще», если что-то непонятно, или «следующий», чтобы продолжить."
    )


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
