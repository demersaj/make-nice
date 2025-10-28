"""
Handles communication with LLM APIs.
Supports multiple response formats for flexibility.
"""
import requests
from typing import Dict, Any


class LLMHandler:
    def __init__(self, config: Dict[str, Any]):
        self.endpoint = config.get('endpoint')
        self.api_key = config.get('apiKey')
        self.model = config.get('model', 'default')
        self.max_tokens = config.get('maxTokens', 500)
        self.api_type = config.get('apiType', 'openai')
    
    def transform_message(self, original_message: str) -> str:
        """
        Transform a message using the configured LLM.
        
        Args:
            original_message: The original message to transform
            
        Returns:
            The transformed, work-appropriate message
            
        Raises:
            ValueError: If the endpoint is not configured
            requests.RequestException: If the API request fails
        """
        if not self.endpoint:
            raise ValueError('LLM API endpoint is not configured')
        
        prompt = self._build_prompt(original_message)
        request_payload = self._build_request_payload(prompt)
        headers = self._build_headers()
        
        try:
            response = requests.post(
                self.endpoint,
                json=request_payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            return self._extract_response(response.json())
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                'Cannot connect to LLM API. Please check your LLM_API_ENDPOINT configuration.'
            )
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f'LLM API error: {e.response.status_code} - {e.response.reason}')
    
    def _build_prompt(self, original_message: str) -> str:
        """Build the prompt for the LLM."""
        return f"""You are a professional workplace communication assistant. 
Transform the following message to be work-appropriate, professional, and well-formatted. 
Preserve the original intent but make it suitable for a workplace environment. 
Return ONLY the improved message without any additional commentary.

Original message: {original_message}

Improved message:"""
    
    def _build_request_payload(self, prompt: str) -> Dict[str, Any]:
        """Build the request payload based on API type."""
        if self.api_type == 'openai':
            return {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.7,
                'max_tokens': self.max_tokens
            }
        
        elif self.api_type == 'anthropic':
            return {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': self.max_tokens
            }
        
        else:
            # Generic API format
            return {
                'model': self.model,
                'prompt': prompt,
                'max_tokens': self.max_tokens
            }
    
    def _build_headers(self) -> Dict[str, str]:
        """Build request headers."""
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.api_key:
            # Support different auth header formats
            if self.api_type == 'anthropic':
                headers['x-api-key'] = self.api_key
                headers['anthropic-version'] = '2023-06-01'
            else:
                headers['Authorization'] = f'Bearer {self.api_key}'
        
        return headers
    
    def _extract_response(self, response_data: Dict[str, Any]) -> str:
        """Extract the response text from the API response."""
        improved_message = ''
        
        # Try OpenAI format
        if 'choices' in response_data and len(response_data['choices']) > 0:
            choice = response_data['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                improved_message = choice['message']['content'].strip()
        
        # Try Anthropic format
        elif 'content' in response_data and isinstance(response_data['content'], list):
            if len(response_data['content']) > 0 and 'text' in response_data['content'][0]:
                improved_message = response_data['content'][0]['text'].strip()
        
        # Try generic content field
        elif 'content' in response_data:
            if isinstance(response_data['content'], str):
                improved_message = response_data['content'].strip()
        
        # Try text field
        elif 'text' in response_data:
            improved_message = response_data['text'].strip()
        
        # Try direct string (if response_data is somehow already a string)
        elif isinstance(response_data, str):
            improved_message = response_data.strip()
        
        # Try result field
        elif 'result' in response_data:
            improved_message = response_data['result'].strip()
        
        if not improved_message:
            raise ValueError('Could not extract message from LLM response')
        
        return improved_message

