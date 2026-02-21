---
name: "claude-integration"
description: "Integrates Anthropic Claude API into websites via Vercel. Invoke when user wants to add Claude AI to their web tool."
---

# Claude API Integration

This skill provides code patterns for integrating Anthropic's Claude API into web applications using Vercel serverless functions.

## Claude API Request Format

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Your message here"}
    ]
)

result = message.content[0].text
```

## Vercel Serverless Function

```python
import json
import os
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    user_message = body.get('message', '')
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    result = message.content[0].text
    
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
    {"src": "api/claude.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/api/claude", "dest": "api/claude.py"}
  ]
}
```

## Requirements

```
anthropic>=0.25.0
```

## Claude Vision (Image Analysis)

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64_image_data
                    }
                },
                {"type": "text", "text": "Describe this image"}
            ]
        }
    ]
)
```

## Common Issues

1. **API Key**: Use ANTHROPIC_API_KEY environment variable
2. **Model Name**: Use correct model ID (claude-3-5-sonnet-20241022)
3. **Image Size**: Claude has image size limits, compress if needed
4. **Rate Limits**: Check Anthropic API rate limits

## Usage

Invoke this skill when user wants to:
- Add Claude AI to website
- Use Claude for text generation
- Integrate Claude Vision for image analysis
- Build AI-powered tools with Claude
