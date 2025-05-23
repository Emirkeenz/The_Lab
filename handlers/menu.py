from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Математика", callback_data="subject_math")],
        [InlineKeyboardButton("🔬 Физика", callback_data="subject_physics")],
        [InlineKeyboardButton("🧪 Химия", callback_data="subject_chemistry")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! 👋\nВыбери предмет 👇", reply_markup=reply_markup)

# === Выбор предмета ===
async def subject_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = query.data.split("_")[1]
    context.user_data["subject"] = subject

    await query.edit_message_text(
        text=f"✅ Ты выбрал предмет: {subject.capitalize()}.\n\nТеперь можешь загрузить урок с помощью /upload_lesson или просто написать свой вопрос 📩"
    )
