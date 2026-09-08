import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8765104365:AAGEZbHSJ1MMp26tIeyE0Dievbm9-lzgxjM"
user_data_db = {}
ADMIN_USERNAME = "raouf100K"
ADMIN_ID = 8890160605

REQUIRED_TELEGRAM_CHANNEL = "https://t.me/dray_ff_bot"
REQUIRED_YOUTUBE_CHANNEL = "https://youtube.com/@ON_DRAY"

LANGUAGES = {
    "ar": {
        "welcome": "مرحباً بك في بوت الخدمات 🎮",
        "profile": "👤 معلومات الحساب",
        "earn": "🎁 جمع النقاط",
        "store": "🛒 المتجر",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في بوت Free Fire! اختر من الأزرار أدناه:")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()
