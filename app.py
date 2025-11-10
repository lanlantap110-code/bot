from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from flask import Flask

app = Flask(__name__)

# Bot token
TOKEN = "8388534089:AAHD77ts2aVPWfuFy9gBERchAMlPyEJFnNo"

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f"Hello {user_name}! I am a bot. 🤖\n\nNice to meet you!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I received your message! Type /start to begin again.")

@app.route('/')
def home():
    return "Telegram Bot is running!"

if __name__ == '__main__':
    # Bot setup
    application = Application.builder().token(TOKEN).build()
    
    # Handlers add karo
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Bot start karo (polling mode)
    application.run_polling()
    
    # Flask server
    app.run(host='0.0.0.0', port=3000)
