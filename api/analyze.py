import json
import os

API_KEY = os.environ.get('ARK_API_KEY', '483e4f2b-fe23-4ab3-a3f3-ab66c279f748')

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        image_base64 = body.get('image', '')
        prompt = body.get('prompt', 'Describe this image')
        
        if not image_base64:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No image provided'})
            }
        
        import requests
        
        # Try different model names
        models_to_try = [
            'doubao-seed-2.0-lite',
            'doubao-lite-32k',
            'doubao-pro-32k'
        ]
        
        url = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }
        
        last_error = None
        
        for model in models_to_try:
            try:
                payload = {
                    'model': model,
                    'messages': [
                        {
                            'role': 'user',
                            'content': [
                                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + image_base64}},
                                {'type': 'text', 'text': prompt}
                            ]
                        }
                    ],
                    'max_tokens': 200
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    text = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'description': text, 'model': model})
                    }
                else:
                    last_error = response.text
            except Exception as e:
                last_error = str(e)
                continue
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'All models failed', 'details': last_error})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
