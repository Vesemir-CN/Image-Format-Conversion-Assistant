---
name: "openai-integration"
description: "Integrates OpenAI GPT API into websites via Vercel serverless functions. Invoke when user wants to add OpenAI/ChatGPT to their web tool."
---

# OpenAI API Integration

This skill provides code patterns for integrating OpenAI's GPT API into web applications using Vercel serverless functions.

## OpenAI API Request Format

```python
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Your question here"}
    ],
    max_tokens=500
)

result = response.choices[0].message.content
```

## Vercel Serverless Function

```python
import json
import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    user_message = body.get('message', '')
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    result = response.choices[0].message.content
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'response': result})
    }
```

## Vercel Configuration

```json
{
  "version": 2,
  "builds": [
    {"src": "api/chat.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/api/chat", "dest": "api/chat.py"}
  ]
}
```

## Requirements

```
openai>=1.0.0
```

## Common Issues

1. **API Key**: Store in environment variables, never in code
2. **Rate Limits**: Add retry logic for rate limit errors
3. **Timeout**: Increase timeout for long responses
4. **Streaming**: Use streaming for real-time responses

## Usage

Invoke this skill when user wants to:
- Add OpenAI/ChatGPT to website
- Create AI chatbot
- Integrate GPT-4 vision capabilities
- Build AI-powered web tools
