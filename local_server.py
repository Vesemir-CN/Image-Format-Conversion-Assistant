from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

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
        
        url = 'https://ark.cn-beijing.volces.com/api/v3/responses'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + API_KEY
        }
        
        # Always use array format for input
        if image_base64:
            # Image + text request
            payloads = [
                {
                    'model': ENDPOINT_ID,
                    'input': [
                        {
                            'role': 'user',
                            'content': [
                                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + image_base64}},
                                {'type': 'text', 'text': prompt}
                            ]
                        }
                    ]
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
                        
                        return jsonify({'description': text})
                except Exception as e:
                    continue
            
            return jsonify({'error': 'API call failed'}), 400
        else:
            # Text-only request - use array format
            payload = {
                'model': ENDPOINT_ID,
                'input': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            }
            
            print('Text-only request:', prompt[:100])
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            print('Response status:', response.status_code)
            print('Response body:', response.text[:200])
            
            if response.status_code != 200:
                return jsonify({'error': 'API error', 'details': response.text}), response.status_code
            
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
            
            return jsonify({'description': text})
        
    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('Starting server at http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
