import re
import time
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === CONFIGURATION ===
BOT_TOKEN = "8403262990:AAGWFDQQPDRpzYgPvyqLRqNiQE_YdHoyx_Q"
SOURCE_CHANNEL_ID = -1002694911933   # Channel where messages arrive
TARGET_CHANNEL_ID = -1002558329310   # Channel to forward if date matches
CUTOFF_DATE = datetime(2025, 8, 25)

# === DATE EXTRACTION ===
DATE_PATTERN = r'(\d{2}\.\d{2}\.\d{4})'

def extract_date(text):
    match = re.search(DATE_PATTERN, text)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%d.%m.%Y")
    except:
        return None

# === MESSAGE HANDLER ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # Ensure message is only processed if from the correct source channel
    if update.message.chat_id != SOURCE_CHANNEL_ID:
        return

    message_date = extract_date(update.message.text)
    if message_date and message_date < CUTOFF_DATE:
        await context.bot.forward_message(
            chat_id=TARGET_CHANNEL_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )

# === BOT STARTUP ===
def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()

# === DUMMY HTTP SERVER FOR RENDER FREE PLAN ===
import threading
import http.server
import socketserver

def run_dummy_web_server():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Dummy web server running on port", PORT)
        httpd.serve_forever()

# === MAIN ===
if __name__ == "__main__":
    time.sleep(5)  # Delay to avoid conflict
    threading.Thread(target=run_dummy_web_server).start()
    start_bot()
