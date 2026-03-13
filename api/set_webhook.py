import requests
import os

def handler(request):
    TG_TOKEN = os.environ.get('TG_TOKEN')
    # Получаем домен вашего сайта на Vercel
    host = request.headers.get('host', '')
    webhook_url = f"https://{host}/api/index"
    
    url = f"https://api.telegram.org/bot{TG_TOKEN}/setWebhook?url={webhook_url}"
    
    response = requests.get(url)
    data = response.json()
    
    return {'statusCode': 200, 'body': json.dumps(data, ensure_ascii=False)}
