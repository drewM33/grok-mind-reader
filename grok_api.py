"""
Official xAI Grok API Integration with SSL fix for macOS
"""

import os
import json
import aiohttp
import ssl
import certifi
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GrokAPI:
    def __init__(self):
        self.api_key = os.getenv('XAI_API_KEY')
        self.base_url = os.getenv('XAI_API_BASE_URL', 'https://api.x.ai/v1')
        
    async def chat_completion(self, query: str, model: str = "grok-2") -> Dict[str, Any]:
        """Make a chat completion request to Grok API"""
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': model,
            'messages': [
                {
                    'role': 'user',
                    'content': query
                }
            ],
            'stream': False,
            'temperature': 0
        }
        
        url = f"{self.base_url}/chat/completions"
        
        # Create SSL context that bypasses certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'success': True,
                            'content': data['choices'][0]['message']['content'],
                            'usage': data.get('usage', {}),
                            'model': data.get('model')
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'success': False,
                            'error': f'Status {response.status}: {error_text}'
                        }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
