from http.server import BaseHTTPRequestHandler
import json
import requests
import os

TOKEN = "8388534089:AAHD77ts2aVPWfuFy9gBERchAMlPyEJFnNo"

def send_telegram_message(chat_id, text):
    """Telegram message send karne ka function"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def handler(request):
    """Vercel serverless function handler"""
    
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Telegram Bot is running on Vercel!'
        }
    
    elif request.method == 'POST':
        try:
            # Telegram update data
            update_data = json.loads(request.body)
            
            # Process Telegram update
            if 'message' in update_data:
                chat_id = update_data['message']['chat']['id']
                text = update_data['message'].get('text', '')
                user_name = update_data['message']['from'].get('first_name', 'User')
                
                if text == '/start':
                    response_text = f"Hello {user_name}! I am a bot. 🤖\n\nNice to meet you!"
                    send_telegram_message(chat_id, response_text)
                else:
                    send_telegram_message(chat_id, "I received your message! Type /start to begin again.")
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"status": "success"})
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": str(e)})
            }
