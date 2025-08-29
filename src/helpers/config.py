import os
import json
from .get_config_path import get_config_path

APP_NAME = "GitRoaster"
CONFIG_FILENAME = "config.json"

class Settings:
    def __init__(self):
        config_path = get_config_path()

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            config = json.load(f)

        self.ROAST_LLM_PROVIDER = config.get("ROAST_LLM_PROVIDER", "")
        self.ROAST_LLM_MODEL_ID = config.get("ROAST_LLM_MODEL_ID", "")
        self.ROAST_OPENAI_API_KEY = config.get("ROAST_OPENAI_API_KEY", "")
        self.ROAST_OPENAI_BASE_URL = config.get("ROAST_OPENAI_BASE_URL", "")
        self.ROAST_GROQ_API_KEY = config.get("ROAST_GROQ_API_KEY", "")
        self.ROAST_GITHUB_TOKEN = config.get("ROAST_GITHUB_TOKEN", "")

def get_settings():
    return Settings()