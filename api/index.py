# api/index.py
import json
import requests
import os
from openai import OpenAI

# Глобальная инициализация (выполняется один раз при "холодном старте")
TG_TOKEN = os.environ.get('TG_TOKEN')
QWEN_KEY = os.environ.get('QWEN_KEY')

client = OpenAI(
    api_key=QWEN_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

def handler(request, context=None):
    """
    Vercel Serverless Function Handler
    request: объект запроса от Vercel
    context: дополнительный контекст (опционально)
    """
    # Разрешаем CORS для предварительных запросов
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method Not Allowed'}
    
    try:
        # Парсим тело запроса от Telegram
        if hasattr(request, 'body') and request.body:
            body = json.loads(request.body) if isinstance(request.body, str) else request.body
        else:
            body = json.loads(request.get_data(as_text=True))
        
        # Проверяем, что это сообщение от пользователя
        if 'message' not in body or 'text' not in body.get('message', {}):
            return {'statusCode': 200, 'body': 'ok'}  # Игнорируем другие обновления
        
        chat_id = body['message']['chat']['id']
        user_text = body['message']['text']
        message_id = body['message'].get('message_id')
        
        # Запрос к ИИ Qwen
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        ai_answer = response.choices[0].message.content
        
        # Отправка ответа в Telegram
        tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        requests.post(tg_url, json={
            "chat_id": chat_id,
            "text": ai_answer,
            "reply_to_message_id": message_id
        }, timeout=10)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'status': 'success'})
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
