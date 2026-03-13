import json
import requests
import os
from openai import OpenAI

# Настройки
TG_TOKEN = os.environ.get('TG_TOKEN')
QWEN_KEY = os.environ.get('QWEN_KEY')
QWEN_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

# Инициализация клиента Qwen
client = OpenAI(api_key=QWEN_KEY, base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

def handler(request):
    # Vercel передает данные в request.body
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            
            # Проверяем, что это сообщение от пользователя
            if 'message' in body and 'text' in body['message']:
                chat_id = body['message']['chat']['id']
                user_text = body['message']['text']
                
                # Запрос к ИИ Qwen
                response = client.chat.completions.create(
                    model="qwen-turbo",
                    messages=[{"role": "user", "content": user_text}]
                )
                ai_answer = response.choices[0].message.content
                
                # Отправка ответа обратно в Telegram
                tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
                requests.post(tg_url, json={
                    "chat_id": chat_id,
                    "text": ai_answer
                })
                
            return {'statusCode': 200, 'body': 'ok'}
            
        except Exception as e:
            print(f"Error: {e}")
            return {'statusCode': 500, 'body': str(e)}
            
    return {'statusCode': 405, 'body': 'Method Not Allowed'}
