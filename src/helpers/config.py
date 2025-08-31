from typer import get_app_dir
import os
import json

APP_NAME = "GitRoaster"

def get_config_path():
    config_dir = get_app_dir(APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

def load_config():
    config_path = get_config_path()
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config):
    """Saves the config dictionary or Pydantic model to the file."""
    if not isinstance(config, dict):
        config = config.model_dump()
    with open(get_config_path(), 'w') as f:
        json.dump(config, f, indent=2)