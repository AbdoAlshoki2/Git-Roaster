import os
from .config import get_config_path, load_config

class Settings:
    def __init__(self):
        config_path = get_config_path()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        config = load_config()

        self.ROAST_LLM_PROVIDER = config.get("ROAST_LLM_PROVIDER", "")
        self.ROAST_LLM_MODEL_ID = config.get("ROAST_LLM_MODEL_ID", "")
        self.ROAST_DEFAULT_API_KEY = config.get("ROAST_DEFAULT_API_KEY", "")
        self.ROAST_OPENAI_API_KEY = config.get("ROAST_OPENAI_API_KEY", "")
        self.ROAST_OPENAI_BASE_URL = config.get("ROAST_OPENAI_BASE_URL", "")
        self.ROAST_GROQ_API_KEY = config.get("ROAST_GROQ_API_KEY", "")
        self.ROAST_GITHUB_TOKEN = config.get("ROAST_GITHUB_TOKEN", "")

def get_settings():
    return Settings()