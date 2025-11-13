from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, Forbidden, BadRequest
import asyncio
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return
    
    for member in update.message.new_chat_members:
        try:
            mention = f'<a href="tg://user?id={member.id}">{member.first_name}</a>'
            msg = (
                f"🌸 আসসালামু আলাইকুম 🌸\n\n"
                f"{mention} 💫 🎯 আপনাকে আমাদের গ্রুপে আন্তরিক স্বাগতম 😍\n\n"
                f"এখান থেকে পাবেন:\n"
                f"⚡ আপডেট, সহায়তা ও দরকারি তথ্য\n"
                f"📌 গ্রুপটি পিন করুন\n\n"
                f"🌟 একসাথে শিখি ও এগিয়ে চলি! 🚀\n"
                f"🔔 সব আপডেট পেতে চ্যানেলে যোগ দিন 👇"
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

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))
    app_bot.add_error_handler(error_handler)
    
    logger.info("Bot started successfully!")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
