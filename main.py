import os
import asyncio
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

# گرفتن توکن از متغیر محیطی
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن ربات در متغیر محیطی TOKEN تنظیم نشده!")

# ایجاد اپ Flask برای وضعیت سرور
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ربات آنلاین است 🌐"

# هندلر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فایل، عکس یا ویدیوت رو بفرست تا لینک مستقیم تلگرامش رو بدم.")

# هندلر فایل/عکس/ویدیو
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    if update.message.document:
        file = update.message.document
    elif update.message.video:
        file = update.message.video
    elif update.message.photo:
        file = update.message.photo[-1]  # بهترین کیفیت عکس
    else:
        await update.message.reply_text("⚠️ فقط فایل، ویدیو یا عکس پشتیبانی می‌شود.")
        return

    telegram_file = await file.get_file()
    file_url = telegram_file.file_path
    direct_link = f"https://api.telegram.org/file/bot{TOKEN}/{file_url}"

    await update.message.reply_text(
        f"✅ لینک مستقیم آماده شد:\n📎 {direct_link}\n\n"
        "📌 اگر تلگرام فیلتر است، ممکن است نیاز به فیلترشکن باشد."
    )

# اجرای ربات تلگرام در یک thread جدا
def run_telegram_bot():
    async def _run():
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.PHOTO, handle_file))
        print("🤖 ربات در حال اجراست...")
        await application.run_polling(close_loop=False, stop_signals=None)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())

# اجرای Flask و Telegram bot با هم
if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=10000)
