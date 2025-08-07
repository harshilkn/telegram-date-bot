import re
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8403262990:AAGWFDQQPDRpzYgPvyqLRqNiQE_YdHoyx_Q"
TARGET_CHANNEL_ID = -1002558329310  # Replace with your channel username or numeric ID
CUTOFF_DATE = datetime(2025, 10, 15)

DATE_PATTERN = r'(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})'

def extract_date(text):
    match = re.search(DATE_PATTERN, text)
    if not match:
        return None
    for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y"]:
        try:
            return datetime.strptime(match.group(1), fmt)
        except:
            continue
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message_date = extract_date(update.message.text)
    if message_date and message_date < CUTOFF_DATE:
        await context.bot.forward_message(
            chat_id=TARGET_CHANNEL_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("Bot is running...")
    app.run_polling()
