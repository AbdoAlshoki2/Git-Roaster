from llms.providers.OpenAIProvider import OpenAIProvider
from llms.providers.GroqProvider import GroqProvider
from models.enums.LLMEnum import LLMProviderEnum

class LLMProviderFactory:
    @staticmethod
    def get_provider(config):
        if config.LLM_PROVIDER == LLMProviderEnum.OPENAI.value:
            return OpenAIProvider(
                api_key= config.OPENAI_API_KEY,
                base_url= config.OPENAI_BASE_URL
            )
        elif config.LLM_PROVIDER == LLMProviderEnum.GROQ.value:
            return GroqProvider(
                api_key= config.GROQ_API_KEY,
            )
