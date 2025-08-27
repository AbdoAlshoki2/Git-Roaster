from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):

    ROAST_LLM_PROVIDER: str = ""
    ROAST_LLM_MODEL_ID: str = ""

    ROAST_OPENAI_API_KEY: str = ""
    ROAST_OPENAI_BASE_URL: str = ""
    ROAST_GROQ_API_KEY: str = ""

    ROAST_GITHUB_TOKEN: str = ""

    class Config:
        env_file = ENV_PATH

def get_settings():
    return Settings()