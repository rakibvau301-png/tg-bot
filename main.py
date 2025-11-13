from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, Forbidden, BadRequest
from flask import Flask
import asyncio
import os
import logging
import threading

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online and working perfectly on Render (Free Plan)!")

# ✅ Welcome message
async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return
    
    for member in update.message.new_chat_members:
        try:
            mention = f'<a href="tg://user?id={member.id}">{member.first_name}</a>'
            msg = (
                f"🌸 আসসালামু আলাইকুম 🌸\n\n"
                f"{mention} 💫 আপনাকে আমাদের গ্রুপে স্বাগতম!\n\n"
                f"📢 চ্যানেলে যোগ দিন 👇"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/CardArenaOfficial")]
            ])
            
            sent_msg = await update.message.reply_html(msg, reply_markup=keyboard)
            await asyncio.sleep(60)
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=sent_msg.message_id
            )
        except Exception as e:
            logger.error(f"Error: {e}")

# ✅ Flask server (Render এর জন্য দরকার)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot running on Render free Web Service!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ✅ Telegram bot main
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    threading.Thread(target=run_flask).start()  # Flask চালাবে ব্যাকগ্রাউন্ডে

    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))
    app_bot.run_polling()

if __name__ == "__main__":
    main()
