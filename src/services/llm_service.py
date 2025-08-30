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

        if not self.model_id or (not self.api_key and not self.base_url):
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model_id,
            "messages": messages
        }

        response = requests.post(url=self.base_url, headers=headers, json=data)

        if response.status_code != 200:

            return None

        response_json = response.json()

        if not response_json or not response_json.get("choices") or not response_json.get("choices")[0] or not response_json.get("choices")[0].get("message"):
            return None

        return response_json.get("choices")[0].get("message").get("content")

    @beartype
    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt
        }
