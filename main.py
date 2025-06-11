import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get('PORT', 10000))

# ایجاد اپلیکیشن تلگرام
application = Application.builder().token(TOKEN).build()

# هندلر استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فایل بفرست تا برات لینک بسازم.")

# هندلر پیام
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if file:
        file_info = await context.bot.get_file(file.file_id)
        await update.message.reply_text(f"🔗 لینک فایل:\n{file_info.file_path}")

# افزودن هندلرها
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

# Flask setup
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running"

# تابع async برای اجرای هر دو اپلیکیشن
async def main():
    # اجرای اپ تلگرام در پس‌زمینه
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Flask را با asyncio اجرا کن
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = [f"0.0.0.0:{PORT}"]
    await serve(app, config)

# اجرای اپ
if __name__ == "__main__":
    asyncio.run(main())
