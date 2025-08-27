from llms.providers.OpenAIProvider import OpenAIProvider
from llms.providers.GroqProvider import GroqProvider
from models.enums.LLMEnum import LLMProviderEnum

class LLMProviderFactory:
    @staticmethod
    def get_provider(config):
        if config.ROAST_LLM_PROVIDER == LLMProviderEnum.OPENAI.value:
            return OpenAIProvider(
                api_key= config.ROAST_OPENAI_API_KEY,
                base_url= config.ROAST_OPENAI_BASE_URL
            )
        elif config.ROAST_LLM_PROVIDER == LLMProviderEnum.GROQ.value:
            return GroqProvider(
                api_key= config.ROAST_GROQ_API_KEY,
            )
