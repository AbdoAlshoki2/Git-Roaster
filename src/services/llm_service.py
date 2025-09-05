import requests
from beartype import beartype
from models.enums.LLMEnum import LLMProviderEnum, LLMURLEnum

class LLMService:
    @beartype
    def __init__(self, config):
        self.config = config
        self.provider = config.ROAST_LLM_PROVIDER
        self.model_id = None
        self.api_key = None
        self.base_url = None
        self.set_provider(self.provider)

    @beartype
    def set_provider(self, provider: str):
        self.provider = provider
        self.api_key = self.config.ROAST_DEFAULT_API_KEY
        
        if provider == LLMProviderEnum.OPENAI.value:
            self.base_url = LLMURLEnum.OPENAI.value if not self.config.ROAST_OPENAI_BASE_URL else self.config.ROAST_OPENAI_BASE_URL
        elif provider == LLMProviderEnum.GROQ.value:
            self.base_url = LLMURLEnum.GROQ.value
        else:
            self.api_key = None
            self.base_url = None

    @beartype
    def set_model(self, model_id: str):
        self.model_id = model_id

    @beartype
    def generate_text(self, messages: list):

        if not self.model_id:
            raise ValueError("Model ID is not set")
            
        if not self.base_url:
            raise ValueError(f"Base URL is not set for provider {self.provider}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model_id,
            "messages": messages
        }

        try:
            response = requests.post(url=self.base_url, headers=headers, json=data, timeout=45)
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out. The API might be overloaded.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Failed to connect to the API. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error: {str(e)}")

        if response.status_code != 200:
            error_msg = f"API request failed with status {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f": {error_detail.get('error', {}).get('message', 'Unknown error')}"
            except:
                error_msg += f": {response.text}"
            raise ConnectionError(error_msg)

        response_json = response.json()

        if not response_json or not response_json.get("choices") or not response_json.get("choices")[0] or not response_json.get("choices")[0].get("message"):
            raise ConnectionError("Failed to get a response from the LLM service. Check your API key and network.")

        return response_json.get("choices")[0].get("message").get("content")

    @beartype
    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt
        }
