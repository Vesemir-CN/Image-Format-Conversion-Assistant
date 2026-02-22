import json
import os
import requests

API_KEY = os.environ.get('ARK_API_KEY', '483e4f2b-fe23-4ab3-a3f3-ab66c279f748')
ENDPOINT_ID = 'ep-20260221013833-rdjh9'

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        image_base64 = body.get('image', '')
        prompt = body.get('prompt', 'Describe this image')
        
        url = 'https://ark.cn-beijing.volces.com/api/v3/responses'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }
        
        if image_base64:
            # Try two payload formats
            success = False
            last_error = ""
            
            # Format 1: messages array
            try:
                payload1 = {
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
                }
                response = requests.post(url, json=payload1, headers=headers, timeout=55)
                
                if response.status_code == 200:
                    result = response.json()
                    text = ''
                    if 'output' in result:
                        for item in result['output']:
                            if 'content' in item:
                                for c in item['content']:
                                    if c.get('type') == 'output_text':
                                        text += c.get('text', '')
                    
                    if not text:
                        text = str(result)
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'description': text})
                    }
                else:
                    last_error = f"Format1: {response.status_code} - {response.text[:200]}"
            except Exception as e:
                last_error = f"Format1 error: {str(e)}"
            
            # Format 2: input_image type
            try:
                payload2 = {
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
                response = requests.post(url, json=payload2, headers=headers, timeout=55)
                
                if response.status_code == 200:
                    result = response.json()
                    text = ''
                    if 'output' in result:
                        for item in result['output']:
                            if 'content' in item:
                                for c in item['content']:
                                    if c.get('type') == 'output_text':
                                        text += c.get('text', '')
                    
                    if not text:
                        text = str(result)
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'description': text})
                    }
                else:
                    last_error = f"Format2: {response.status_code} - {response.text[:200]}"
            except Exception as e:
                last_error = f"Format2 error: {str(e)}"
            
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': last_error})
            }
        else:
            # Text-only request
            payload = {
                'model': ENDPOINT_ID,
                'input': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=55)
            
            if response.status_code != 200:
                return {
                    'statusCode': response.status_code,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': f"Text: {response.status_code} - {response.text[:200]}"})
                }
            
            result = response.json()
            text = ''
            if 'output' in result:
                for item in result['output']:
                    if 'content' in item:
                        for c in item['content']:
                            if c.get('type') == 'output_text':
                                text += c.get('text', '')
            
            if not text:
                text = str(result)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'description': text})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f"Exception: {str(e)}"})
        }
