import getpass
import os
import json
from typing import Union
from .config import get_config_path, load_config, save_config

def get_or_create_config():
    """Loads config if it exists, otherwise creates a default structure. Ensures all keys are present."""
    default_config = {
        "ROAST_GITHUB_TOKEN": "",
        "ROAST_LLM_PROVIDER": "GROQ",
        "ROAST_LLM_MODEL_ID": "llama3-70b-8192",
        "ROAST_DEFAULT_API_KEY": "",
        "ROAST_OPENAI_API_KEY": "",
        "ROAST_OPENAI_BASE_URL": "",
        "ROAST_GROQ_API_KEY": ""
    }
    try:
        existing_config = load_config()
        default_config.update(existing_config)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return default_config

def update_github_token(config, value: Union[bool, str] = True):
    """Updates the GitHub token."""
    if value is True:
        current = config.get("ROAST_GITHUB_TOKEN", "")
        value = getpass.getpass(f"GitHub Token [{'*' * len(current) if current else 'Not set'}]: ").strip() or current
    config["ROAST_GITHUB_TOKEN"] = value
    print("✅ GitHub Token updated.")
    return config

def update_llm_provider(config, value: Union[bool, str] = True):
    """Updates the LLM provider."""
    if value is True:
        current = config.get("ROAST_LLM_PROVIDER", "GROQ")
        print(f"\nSelect LLM Provider (current: {current}):")
        print("1. OpenAI")
        print("2. Groq")
        choice = input("Select (1 or 2): ").strip()
        value = {"1": "OPENAI", "2": "GROQ"}.get(choice, current)
    
    value = str(value).upper()
    config["ROAST_LLM_PROVIDER"] = value
    if value == "OPENAI":
        config["ROAST_DEFAULT_API_KEY"] = config.get("ROAST_OPENAI_API_KEY", "")
    elif value == "GROQ":
        config["ROAST_DEFAULT_API_KEY"] = config.get("ROAST_GROQ_API_KEY", "")
    print(f"✅ LLM Provider set to {value}.")
    return config

def update_api_key(config, value: Union[bool, str] = True):
    """Updates the API key for the active provider."""
    provider = config.get("ROAST_LLM_PROVIDER", "GROQ")
    key_name = f"ROAST_{provider}_API_KEY"
    
    if value is True:
        current = config.get(key_name, "")
        value = getpass.getpass(f"{provider} API Key [{'*' * len(current) if current else 'Not set'}]: ").strip() or current

    config[key_name] = value
    config["ROAST_DEFAULT_API_KEY"] = value
    print(f"✅ {provider} API Key updated.")
    return config

def update_model_id(config, value: Union[bool, str] = True):
    """Updates the LLM Model ID."""
    if value is True:
        provider = config.get("ROAST_LLM_PROVIDER", "GROQ")
        default = "gpt-4o-mini" if provider == "OPENAI" else "llama3-70b-8192"
        current = config.get("ROAST_LLM_MODEL_ID", default)
        value = input(f"Model ID [{current}]: ").strip() or current
    
    config["ROAST_LLM_MODEL_ID"] = value
    print(f"✅ Model ID set to {value}.")
    return config

def update_base_url(config, value: Union[bool, str] = True):
    """Updates the OpenAI Base URL."""
    if config.get("ROAST_LLM_PROVIDER") != "OPENAI":
        if isinstance(value, str) or value is True:
             print("⚠️ Base URL is only applicable for the OpenAI provider.")
        return config

    if value is True:
        current = config.get("ROAST_OPENAI_BASE_URL", "")
        value = input(f"OpenAI Base URL [{current if current else 'e.g., https://api.openai.com/v1'}]: ").strip() or current

    if value and isinstance(value, str):
        if not value.endswith("/chat/completions"):
            value = value.rstrip('/') + "/chat/completions"

    config["ROAST_OPENAI_BASE_URL"] = value
    print(f"✅ OpenAI Base URL updated.")
    return config

def setup_config():
    """Runs the full, interactive setup process for all keys."""
    config = get_or_create_config()
    config = update_github_token(config)
    config = update_llm_provider(config)
    config = update_api_key(config)
    config = update_model_id(config)
    if config["ROAST_LLM_PROVIDER"] == "OPENAI":
        config = update_base_url(config)
    save_config(config)
    print("\n✅ Full configuration complete!")

def ensure_config_exists():
    """Checks for config and runs setup if missing."""
    if not os.path.exists(get_config_path()):
        config = get_or_create_config()
        save_config(config)