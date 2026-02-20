from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__, static_folder='.')
CORS(app)

API_KEY = os.environ.get('ARK_API_KEY', '483e4f2b-fe23-4ab3-a3f3-ab66c279f748')
ENDPOINT_ID = 'ep-20260221013833-rdjh9'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    try:
        data = request.json
        image_base64 = data.get('image', '')
        prompt = data.get('prompt', 'Describe this image')
        
        if not image_base64:
            return jsonify({'error': 'No image provided'}), 400
        
        url = 'https://ark.cn-beijing.volces.com/api/v3/responses'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }
        
        # Try different payload formats
        payloads = [
            # Format 1: with image_url object
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
            # Format 2: with input_image type
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
        
        print('Trying API call with model:', ENDPOINT_ID)
        
        for i, payload in enumerate(payloads):
            print(f'Trying payload format {i+1}...')
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                print(f'Format {i+1} - Response status:', response.status_code)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Try to extract text from response
                    text = ''
                    if 'output' in result:
                        output = result['output']
                        if isinstance(output, list) and len(output) > 0:
                            for item in output:
                                if isinstance(item, dict):
                                    if 'content' in item:
                                        for content_item in item['content']:
                                            if isinstance(content_item, dict):
                                                if content_item.get('type') == 'output_text':
                                                    text += content_item.get('text', '')
                                            
                                            elif isinstance(content_item, str):
                                                text += content_item
                                            
                                    elif 'text' in item:
                                        text += item['text']
                    
                    if not text:
                        text = str(result)
                    
                    print('Success! Response:', text[:100])
                    return jsonify({'description': text})
                else:
                    print(f'Format {i+1} failed:', response.text[:200])
            except Exception as e:
                print(f'Format {i+1} error:', str(e))
        
        # If all fail, return the last error
        return jsonify({'error': 'API call failed', 'details': response.text}), 400
        
    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('Starting server at http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
