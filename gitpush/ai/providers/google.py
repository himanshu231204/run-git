"""Google (Gemini) AI provider."""

import json
import urllib.request
import urllib.error
from typing import Optional

from gitpush.ai.providers.base import BaseAIProvider


class GoogleProvider(BaseAIProvider):
    """Google Gemini AI provider."""

    def __init__(self, api_key: str, model: str, base_url: str, timeout: int = 30):
        super().__init__(model, timeout)
        self.api_key = api_key
        # Replace {model} placeholder in base_url
        self.base_url = base_url.format(model=model)

    def generate(self, prompt: str, max_tokens: int = 900, temperature: float = 0.2) -> str:
        """Generate text from a prompt using Google Gemini API."""
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is required for Google provider")

        # Prepare request data for Gemini API
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.8,
                "topK": 10
            }
        }

        # Prepare request
        url = f"{self.base_url}?key={self.api_key}"
        headers = {
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Extract text from Gemini response
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if len(parts) > 0 and 'text' in parts[0]:
                            return parts[0]['text'].strip()
                
                # Fallback if response format is unexpected
                return str(result)
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.read() else str(e)
            raise RuntimeError(f"Google API error ({e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to Google API: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in Google provider: {str(e)}")