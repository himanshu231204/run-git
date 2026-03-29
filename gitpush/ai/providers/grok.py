"""Grok (xAI) AI provider."""

import json
import urllib.request
import urllib.error
from typing import Optional

from gitpush.ai.providers.base import BaseAIProvider


class GrokProvider(BaseAIProvider):
    """Grok (xAI) AI provider."""

    def __init__(self, api_key: str, model: str, base_url: str, timeout: int = 30):
        super().__init__(model, timeout)
        self.api_key = api_key
        self.base_url = base_url

    def generate(self, prompt: str, max_tokens: int = 900, temperature: float = 0.2) -> str:
        """Generate text from a prompt using Grok API."""
        if not self.api_key:
            raise ValueError("GROK_API_KEY is required for Grok provider")

        # Prepare request data for Grok API (OpenAI-compatible)
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }

        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Extract text from Grok response (OpenAI-compatible format)
                if 'choices' in result and len(result['choices']) > 0:
                    message = result['choices'][0].get('message', {})
                    if 'content' in message:
                        return message['content'].strip()
                
                # Fallback if response format is unexpected
                return str(result)
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.read() else str(e)
            raise RuntimeError(f"Grok API error ({e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to Grok API: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in Grok provider: {str(e)}")