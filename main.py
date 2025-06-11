import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن ربات در متغیر محیطی TOKEN تنظیم نشده!")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "ربات آنلاین است 🌐"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فایل، عکس یا ویدیوت رو بفرست تا لینک مستقیم تلگرامش رو بدم.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    if update.message.document:
        file = update.message.document
    elif update.message.video:
        file = update.message.video
    elif update.message.photo:
        file = update.message.photo[-1]
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

async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.PHOTO, handle_file))
    
    print("🤖 ربات در حال اجراست...")
    await application.run_polling()

if __name__ == "__main__":
    # برای اینکه همزمان فلاسک و ربات اجرا بشن
    import threading

    def run_flask():
        app.run(host="0.0.0.0", port=10000)

    threading.Thread(target=run_flask).start()

    asyncio.run(run_bot())
