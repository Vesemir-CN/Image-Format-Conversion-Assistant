---
name: "ai-tool-website"
description: "Builds AI-powered tool websites with Vercel deployment and API integration. Invoke when user wants to create a web tool with AI features."
---

# AI Tool Website Development

This skill helps build AI-powered tool websites using modern web technologies, Vercel deployment, and third-party AI API integration.

## Tech Stack

- **Frontend**: HTML + Tailwind CSS + Vanilla JavaScript
- **Backend**: Python (Vercel Serverless Functions)
- **AI API**: ByteDance Doubao (火山引擎豆包)
- **Deployment**: Vercel + GitHub

## Key Features Implemented

1. **Image Processing**: Canvas API for format conversion, DPI adjustment
2. **AI Integration**: 
   - Vercel Python serverless function (`api/analyze.py`)
   - Doubao API with correct request format (`/api/v3/responses`)
   - Both image analysis and text-only requests
3. **Smart Features**:
   - AI-powered image arrangement
   - Custom user prompts for arrangement logic
   - Auto-generated Figure Legend for scientific publications
4. **Required Pages**: About, Privacy Policy, Terms of Use (for AdSense)

## API Integration Patterns

### Doubao API Request Format

```python
# Image + Text request
payload = {
    'model': ENDPOINT_ID,  # e.g., 'ep-20260221013833-rdjh9'
    'input': [
        {
            'role': 'user',
            'content': [
                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + base64}},
                {'type': 'text', 'text': prompt}
            ]
        }
    ]
}

# Text-only request
payload = {
    'model': ENDPOINT_ID,
    'input': [
        {
            'role': 'user',
            'content': prompt  # Direct string, not object
        }
    ]
}
```

### Vercel Python Serverless Function

```python
import json
import requests

API_KEY = 'your-api-key'
ENDPOINT_ID = 'your-endpoint-id'

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    # Process request...
    return {'statusCode': 200, 'headers': {...}, 'body': json.dumps({...})}
```

### Vercel Configuration (vercel.json)

```json
{
  "version": 2,
  "builds": [
    {"src": "api/analyze.py", "use": "@vercel/python"},
    {"src": "index.html", "use": "@vercel/static"}
  ],
  "routes": [
    {"src": "/api/analyze", "dest": "api/analyze.py"},
    {"src": "/(.*)", "dest": "index.html"}
  ]
}
```

## Common Issues & Solutions

1. **API 400 Bad Request**: Check request format - text-only needs direct string, not object
2. **API Authentication Error**: Verify API key and endpoint ID, ensure model is enabled
3. **Vercel Build Error**: Check vercel.json syntax, remove unsupported fields
4. **CORS Issues**: Use serverless function as proxy for API calls

## File Structure

```
project/
├── index.html          # Main page
├── about.html          # About page
├── privacy.html        # Privacy Policy
├── terms.html          # Terms of Use
├── vercel.json         # Vercel config
├── api/
│   └── analyze.py      # Serverless function
└── local_server.py     # Local testing server
```

## Usage

When user asks to:
- Build AI-powered website → Use this skill
- Add Vercel deployment → Use this skill
- Integrate Doubao/豆包 API → Use this skill
- Create AdSense pages → Use this skill

This skill provides end-to-end guidance for creating production-ready AI tool websites.
