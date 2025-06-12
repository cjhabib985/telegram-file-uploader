import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# دریافت توکن از متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("توکن ربات پیدا نشد! لطفاً متغیر محیطی BOT_TOKEN را تنظیم کنید.")

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

file_filter = filters.Document.ALL | filters.VIDEO | filters.AUDIO

app.add_handler(MessageHandler(file_filter, handle_file))
app.add_handler(CommandHandler("start", handle_start))

app.run_polling()
