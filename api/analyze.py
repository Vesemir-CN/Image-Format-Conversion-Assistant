from http.server import BaseHTTPRequestHandler
import json
import requests

API_KEY = '483e4f2b-fe23-4ab3-a3f3-ab66c279f748'

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            image_base64 = data.get('image')
            prompt = data.get('prompt', 'Analyze this scientific image')
            
            if not image_base64:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No image provided'}).encode())
                return
            
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
            
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                result = response.json()
                
                text = result.get('choices', [{}])[0].get('message', {}).get('content', 'Scientific figure')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'description': text}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
