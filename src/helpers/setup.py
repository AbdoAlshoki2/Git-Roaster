import getpass

import os
import json
from .get_config_path import get_config_path


def setup_config():
    """Interactive setup for Git-Roaster configuration"""
    config_path = get_config_path()

    github_token = ""
    provider = ""
    openai_key = ""
    openai_base_url = ""
    llm_model_id = ""
    groq_key = ""
    
    print("🔧 Git-Roaster Setup")
    github_token = getpass.getpass("GitHub Token (read the readme for more info about tool setup): ").strip() or github_token
    
    print("LLM Provider(The llm provider that will be used to generate the review):")
    print("1. OpenAI")
    print("2. GroqAPI")
    choice = input("Select (1 or 2) default is GroqAPI: ").strip() or "2"
    
    if choice == "1":
        provider = "OPENAI"
        openai_key = getpass.getpass("OpenAI API Key (read the readme for more info about tool setup): ").strip() or openai_key
        openai_base_url = getpass.getpass("OpenAI Base URL (read the readme for more info about tool setup): ").strip() or openai_base_url
        llm_model_id = input("Model (default: gpt-4o-mini): ").strip() or "gpt-4o-mini"
        
    else:
        provider = "GROQ"
        groq_key = getpass.getpass("Groq API Key (read the readme for more info about tool setup): ").strip() or groq_key
        llm_model_id = input("Model (default: llama3-70b-8192): ").strip() or "llama3-70b-8192"
    
    config_dict = {
        "ROAST_GITHUB_TOKEN": github_token,
        "ROAST_LLM_PROVIDER": provider,
        "ROAST_LLM_MODEL_ID": llm_model_id,
        "ROAST_OPENAI_API_KEY": openai_key,
        "ROAST_OPENAI_BASE_URL": openai_base_url,
        "ROAST_GROQ_API_KEY": groq_key
    }
    with open(config_path, "w") as f:
        json.dump(config_dict, f, indent=2)
    print("✅ Setup complete!")
    print("Note: you can change the setup anytime by running the command `roast setup`.")

def check_and_setup():
    """Check if config.json exists in app dir, setup if not"""
    config_path = get_config_path()
    if not os.path.exists(config_path):
        print("⚠️ Configuration missing")
        setup_config()
