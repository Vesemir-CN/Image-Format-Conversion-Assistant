import json
import requests

API_KEY = '483e4f2b-fe23-4ab3-a3f3-ab66c279f748'

def handler(event, context):
    try:
        body = json.loads(event['body'])
        image_base64 = body.get('image')
        prompt = body.get('prompt', 'Analyze this scientific image')
        
        if not image_base64:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No image provided'})
            }
        
        url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }
        
        payload = {
            'model': 'doubao-seed-2.0-lite',
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + image_base64}},
                        {'type': 'text', 'text': prompt}
                    ]
                }
            ],
            'max_tokens': 100
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        text = result.get('choices', [{}])[0].get('message', {}).get('content', 'Scientific figure')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'description': text})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
