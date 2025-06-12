import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from flask import Flask
import threading

# محیط اجرای Flask برای جلوگیری از خطای "No open ports"
app_flask = Flask(__name__)

@app_flask.route('/')
def index():
    return "ربات در حال اجراست ✅"

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# راه‌اندازی Flask در یک Thread جدا
threading.Thread(target=run_flask).start()

# دریافت توکن از متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("توکن ربات پیدا نشد! لطفاً متغیر محیطی BOT_TOKEN را تنظیم کنید.")

# تابع دریافت فایل
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio
    if not file:
        await update.message.reply_text("⚠ لطفاً یک فایل ارسال کنید.")
        return

    await update.message.reply_text("✅ فایل دریافت شد. در حال ساخت لینک...")

    file_info = await file.get_file()
    file_path = file_info.file_path
    link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    await update.message.reply_text(
        f"🔗 لینک دانلود مستقیم:\n{link}\n\n"
        f"⚠ اگر لینک باز نشد، لطفاً از VPN استفاده کن."
    )

# پیام شروع
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فایل بفرست تا لینکش رو برات بفرستم.")

# اجرای ربات
application = ApplicationBuilder().token(BOT_TOKEN).build()
file_filter = filters.Document.ALL | filters.VIDEO | filters.AUDIO

application.add_handler(MessageHandler(file_filter, handle_file))
application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/start'), handle_start))

application.run_polling()
