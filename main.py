from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "توکن ربات خودت"

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

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فایل بفرست تا لینکش رو برات بفرستم.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# ✅ بدون ایمپورت جداگانه از filters.py
file_filter = filters.Document.ALL | filters.VIDEO | filters.Audio

app.add_handler(MessageHandler(file_filter, handle_file))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/start'), handle_start))

app.run_polling()
