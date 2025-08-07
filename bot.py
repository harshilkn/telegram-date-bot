import re
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Your Telegram Bot Token and Channel ID
BOT_TOKEN = "8403262990:AAGWFDQQPDRpzYgPvyqLRqNiQE_YdHoyx_Q"
TARGET_CHANNEL_ID = -1002558329310  # Replace with your numeric channel ID
CUTOFF_DATE = datetime(2025, 8, 25)

# Regex pattern to match common date formats
DATE_PATTERN = r'(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})'

# Function to extract a date from text
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

# Handler function that checks for a valid date
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

# Start the Telegram bot
def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("Bot is running...")
    app.run_polling()

# Dummy web server for Render's free Web Service requirement
import threading
import http.server
import socketserver

def run_dummy_web_server():
    PORT = 10000  # Any port works
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Dummy web server running on port", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    # Run the dummy server in a background thread
    threading.Thread(target=run_dummy_web_server).start()
    # Start the actual Telegram bot
    start_bot()
