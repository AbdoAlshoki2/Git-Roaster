from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    SYSTEM_VERSION: str

    LLM_PROVIDER: str
    LLM_MODEL_ID: str

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

def get_settings():
    return Setting()