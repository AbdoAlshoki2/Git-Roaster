from pydantic import BaseModel
from .config import load_config

class Settings(BaseModel):
    ROAST_LLM_PROVIDER: str = ""
    ROAST_LLM_MODEL_ID: str = ""
    ROAST_DEFAULT_API_KEY: str = ""
    ROAST_OPENAI_API_KEY: str = ""
    ROAST_OPENAI_BASE_URL: str = ""
    ROAST_GROQ_API_KEY: str = ""
    ROAST_GITHUB_TOKEN: str = ""

def get_settings():
    config = load_config()
    return Settings(**config)