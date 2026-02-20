import json
import os

API_KEY = os.environ.get('ARK_API_KEY', '483e4f2b-fe23-4ab3-a3f3-ab66c279f748')
ENDPOINT_ID = 'ep-20260221013833-rdjh9'

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
        
        url = 'https://ark.cn-beijing.volces.com/api/v3/responses'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }
        
        # Try both payload formats
        payloads = [
            {
                'model': ENDPOINT_ID,
                'input': {
                    'messages': [
                        {
                            'role': 'user',
                            'content': [
                                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + image_base64}},
                                {'type': 'text', 'text': prompt}
                            ]
                        }
                    ]
                }
            },
            {
                'model': ENDPOINT_ID,
                'input': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'input_image', 'image_url': 'data:image/jpeg;base64,' + image_base64},
                            {'type': 'input_text', 'text': prompt}
                        ]
                    }
                ]
            }
        ]
        
        for payload in payloads:
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    text = ''
                    if 'output' in result:
                        output = result['output']
                        if isinstance(output, list) and len(output) > 0:
                            for item in output:
                                if 'content' in item:
                                    for content_item in item['content']:
                                        if content_item.get('type') == 'output_text':
                                            text += content_item.get('text', '')
                    
                    if not text:
                        text = str(result)
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'description': text})
                    }
            except Exception as e:
                continue
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'API call failed'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
