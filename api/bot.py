from http.server import BaseHTTPRequestHandler
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# Bot token
TOKEN = "8388534089:AAHD77ts2aVPWfuFy9gBERchAMlPyEJFnNo"

# Global application variable
application = None

def initialize_bot():
    global application
    if application is None:
        application = Application.builder().token(TOKEN).build()
        
        # Handlers add karo
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f"Hello {user_name}! I am a bot. 🤖\n\nNice to meet you!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I received your message! Type /start to begin again.")

async def process_update(update_data):
    """Process Telegram update asynchronously"""
    initialize_bot()
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Telegram Bot is running on Vercel!')
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update_data = json.loads(post_data.decode('utf-8'))
        
        # Process update asynchronously
        asyncio.run(process_update(update_data))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "ok"})
        self.wfile.write(response.encode())

def main(request):
    if request.method == 'GET':
        return {'statusCode': 200, 'body': 'Telegram Bot is running on Vercel!'}
    elif request.method == 'POST':
        update_data = json.loads(request.body)
        asyncio.run(process_update(update_data))
        return {'statusCode': 200, 'body': json.dumps({"status": "ok"})}
